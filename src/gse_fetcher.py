"""GSE Fetcher module for retrieving SRA IDs from GSE numbers."""

import requests
import xml.etree.ElementTree as ET
import time
import logging
from typing import List, Optional
from urllib.parse import urlencode

from .config import NCBI_ESEARCH_URL, NCBI_ELINK_URL, NCBI_REQUEST_DELAY


class GSEFetcher:
    """Class for fetching SRA IDs from GSE numbers using NCBI APIs."""
    
    def __init__(self):
        """Initialize the GSEFetcher."""
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'seq_downloader/2.0.0 (https://github.com/Gardiner-Lab/seq_Geo_Dowloader)'
        })
    
    def fetch_sra_ids(self, gse_number: str) -> List[str]:
        """
        Fetch SRA IDs associated with a GSE number.
        
        Args:
            gse_number: The GSE number (e.g., 'GSE123456')
            
        Returns:
            List of SRA IDs found for the GSE number
            
        Raises:
            Exception: If there's an error fetching the data
        """
        try:
            # Step 1: Search for the GSE in GEO database
            geo_ids = self._search_geo_database(gse_number)
            if not geo_ids:
                self.logger.warning(f"No GEO IDs found for {gse_number}")
                return []
            
            # Step 2: Link GEO IDs to SRA database
            sra_ids = self._link_geo_to_sra(geo_ids)
            if not sra_ids:
                self.logger.warning(f"No SRA IDs found for {gse_number}")
                return []
            
            self.logger.info(f"Found {len(sra_ids)} SRA IDs for {gse_number}")
            return sra_ids
            
        except Exception as e:
            self.logger.error(f"Error fetching SRA IDs for {gse_number}: {e}")
            raise Exception(f"Failed to fetch SRA IDs for {gse_number}: {str(e)}")
    
    def _search_geo_database(self, gse_number: str) -> List[str]:
        """
        Search for GSE number in GEO database.
        
        Args:
            gse_number: The GSE number to search for
            
        Returns:
            List of GEO database IDs
        """
        params = {
            'db': 'gds',
            'term': f'{gse_number}[Accession]',
            'retmode': 'xml',
            'retmax': 1000
        }
        
        url = f"{NCBI_ESEARCH_URL}?{urlencode(params)}"
        self.logger.debug(f"Searching GEO database: {url}")
        
        response = self._make_request(url)
        if not response:
            return []
        
        # Parse XML response
        try:
            root = ET.fromstring(response.text)
            id_list = root.find('.//IdList')
            if id_list is None:
                return []
            
            geo_ids = [id_elem.text for id_elem in id_list.findall('Id')]
            self.logger.debug(f"Found {len(geo_ids)} GEO IDs")
            return geo_ids
            
        except ET.ParseError as e:
            self.logger.error(f"Error parsing GEO search response: {e}")
            return []
    
    def _link_geo_to_sra(self, geo_ids: List[str]) -> List[str]:
        """
        Link GEO IDs to SRA database to get SRA IDs.
        
        Args:
            geo_ids: List of GEO database IDs
            
        Returns:
            List of SRA IDs
        """
        if not geo_ids:
            return []
        
        params = {
            'dbfrom': 'gds',
            'db': 'sra',
            'id': ','.join(geo_ids),
            'retmode': 'xml'
        }
        
        url = f"{NCBI_ELINK_URL}?{urlencode(params)}"
        self.logger.debug(f"Linking GEO to SRA: {url}")
        
        response = self._make_request(url)
        if not response:
            return []
        
        # Parse XML response
        try:
            root = ET.fromstring(response.text)
            sra_ids = []
            
            # Find all linked SRA IDs
            for linkset in root.findall('.//LinkSet'):
                link_set_db = linkset.find('.//LinkSetDb')
                if link_set_db is not None:
                    db_to = link_set_db.find('DbTo')
                    if db_to is not None and db_to.text == 'sra':
                        id_list = link_set_db.find('IdList')
                        if id_list is not None:
                            for id_elem in id_list.findall('Id'):
                                sra_ids.append(id_elem.text)
            
            # Convert numeric SRA IDs to SRR format if needed
            sra_accessions = self._convert_to_sra_accessions(sra_ids)
            self.logger.debug(f"Found {len(sra_accessions)} SRA accessions")
            return sra_accessions
            
        except ET.ParseError as e:
            self.logger.error(f"Error parsing SRA link response: {e}")
            return []
    
    def _convert_to_sra_accessions(self, sra_ids: List[str]) -> List[str]:
        """
        Convert numeric SRA IDs to SRA accession format (SRR, SRX, etc.).
        
        Args:
            sra_ids: List of numeric SRA IDs
            
        Returns:
            List of SRA accessions
        """
        if not sra_ids:
            return []
        
        # Use esummary to get accession numbers
        params = {
            'db': 'sra',
            'id': ','.join(sra_ids),
            'retmode': 'xml'
        }
        
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{urlencode(params)}"
        self.logger.debug(f"Converting SRA IDs to accessions: {url}")
        
        response = self._make_request(url)
        if not response:
            return []
        
        try:
            root = ET.fromstring(response.text)
            accessions = []
            
            for doc_sum in root.findall('.//DocSum'):
                # Look for Run accession in the summary
                for item in doc_sum.findall('.//Item'):
                    if item.get('Name') == 'Run':
                        run_text = item.text
                        if run_text and run_text.startswith('SRR'):
                            # Extract SRR IDs from the run text
                            import re
                            srr_matches = re.findall(r'SRR\d+', run_text)
                            accessions.extend(srr_matches)
            
            # Remove duplicates and return
            unique_accessions = list(set(accessions))
            self.logger.debug(f"Converted to {len(unique_accessions)} unique SRA accessions")
            return unique_accessions
            
        except ET.ParseError as e:
            self.logger.error(f"Error parsing SRA summary response: {e}")
            return []
    
    def _make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic and rate limiting.
        
        Args:
            url: URL to request
            max_retries: Maximum number of retry attempts
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(max_retries):
            try:
                # Rate limiting - NCBI recommends no more than 3 requests per second
                time.sleep(NCBI_REQUEST_DELAY)
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                return response
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    self.logger.error(f"All {max_retries} attempts failed for URL: {url}")
                    return None
                
                # Exponential backoff
                wait_time = (2 ** attempt) * NCBI_REQUEST_DELAY
                time.sleep(wait_time)
        
        return None