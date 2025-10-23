"""SRA Downloader module for downloading sequencing data using SRA toolkit."""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .config import (
    SRATOOLKIT_PATH, PREFETCH_EXECUTABLE, FASTERQ_DUMP_EXECUTABLE,
    DEFAULT_MAX_RETRIES, DEFAULT_RETRY_DELAY, DEFAULT_TIMEOUT
)


class SRADownloader:
    """Class for downloading SRA data using SRA toolkit."""
    
    def __init__(self, output_dir: str = "downloads", max_threads: int = 4):
        """
        Initialize the SRA downloader.
        
        Args:
            output_dir: Directory to save downloaded files
            max_threads: Maximum number of concurrent downloads
        """
        self.output_dir = Path(output_dir)
        self.max_threads = max_threads
        self.logger = logging.getLogger(__name__)
        self.lock = threading.Lock()
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up SRA toolkit paths
        self.sratoolkit_bin = Path(SRATOOLKIT_PATH) / "bin"
        self.prefetch_exe = self.sratoolkit_bin / f"{PREFETCH_EXECUTABLE}.exe"
        self.fasterq_dump_exe = self.sratoolkit_bin / f"{FASTERQ_DUMP_EXECUTABLE}.exe"
        
        # Verify SRA toolkit installation
        self._verify_sra_toolkit()
    
    def _verify_sra_toolkit(self):
        """Verify that SRA toolkit is properly installed."""
        if not self.sratoolkit_bin.exists():
            raise FileNotFoundError(f"SRA toolkit not found at {self.sratoolkit_bin}")
        
        if not self.prefetch_exe.exists():
            raise FileNotFoundError(f"prefetch.exe not found at {self.prefetch_exe}")
        
        if not self.fasterq_dump_exe.exists():
            raise FileNotFoundError(f"fasterq-dump.exe not found at {self.fasterq_dump_exe}")
        
        self.logger.info("SRA toolkit verified successfully")
    
    def download_sra_ids(self, sra_ids: List[str], split_files: bool = True) -> Dict[str, bool]:
        """
        Download multiple SRA IDs with parallel processing.
        
        Args:
            sra_ids: List of SRA IDs to download
            split_files: Whether to split paired-end files
            
        Returns:
            Dictionary mapping SRA ID to success status
        """
        results = {}
        
        if not sra_ids:
            self.logger.warning("No SRA IDs provided for download")
            return results
        
        self.logger.info(f"Starting download of {len(sra_ids)} SRA IDs with {self.max_threads} threads")
        
        # Use ThreadPoolExecutor for parallel downloads
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Submit all download tasks
            future_to_sra = {
                executor.submit(self._download_single_sra, sra_id, split_files): sra_id
                for sra_id in sra_ids
            }
            
            # Process completed downloads
            for future in as_completed(future_to_sra):
                sra_id = future_to_sra[future]
                try:
                    success = future.result()
                    results[sra_id] = success
                    
                    with self.lock:
                        if success:
                            self.logger.info(f"✓ Successfully downloaded {sra_id}")
                            print(f"✓ Successfully downloaded {sra_id}")
                        else:
                            self.logger.error(f"✗ Failed to download {sra_id}")
                            print(f"✗ Failed to download {sra_id}")
                            
                except Exception as e:
                    results[sra_id] = False
                    with self.lock:
                        self.logger.error(f"✗ Error downloading {sra_id}: {e}")
                        print(f"✗ Error downloading {sra_id}: {e}")
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        print(f"\nDownload Summary:")
        print(f"  Total: {total}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {total - successful}")
        
        return results
    
    def _download_single_sra(self, sra_id: str, split_files: bool = True) -> bool:
        """
        Download a single SRA ID.
        
        Args:
            sra_id: SRA ID to download
            split_files: Whether to split paired-end files
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Prefetch the SRA file
            if not self._prefetch_sra(sra_id):
                return False
            
            # Step 2: Convert to FASTQ using fasterq-dump
            if not self._convert_to_fastq(sra_id, split_files):
                return False
            
            # Step 3: Clean up SRA file (optional)
            self._cleanup_sra_file(sra_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading {sra_id}: {e}")
            return False
    
    def _prefetch_sra(self, sra_id: str, max_retries: int = DEFAULT_MAX_RETRIES) -> bool:
        """
        Prefetch SRA file using prefetch tool.
        
        Args:
            sra_id: SRA ID to prefetch
            max_retries: Maximum number of retry attempts
            
        Returns:
            True if successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                cmd = [
                    str(self.prefetch_exe),
                    sra_id,
                    "--output-directory", str(self.output_dir),
                    "--progress"
                ]
                
                with self.lock:
                    self.logger.debug(f"Prefetching {sra_id} (attempt {attempt + 1}/{max_retries})")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=DEFAULT_TIMEOUT,
                    cwd=str(self.output_dir)
                )
                
                if result.returncode == 0:
                    return True
                else:
                    with self.lock:
                        self.logger.warning(f"Prefetch attempt {attempt + 1} failed for {sra_id}: {result.stderr}")
                    
                    if attempt < max_retries - 1:
                        time.sleep(DEFAULT_RETRY_DELAY)
                    
            except subprocess.TimeoutExpired:
                with self.lock:
                    self.logger.warning(f"Prefetch timeout for {sra_id} (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(DEFAULT_RETRY_DELAY)
                    
            except Exception as e:
                with self.lock:
                    self.logger.error(f"Prefetch error for {sra_id} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(DEFAULT_RETRY_DELAY)
        
        return False
    
    def _convert_to_fastq(self, sra_id: str, split_files: bool = True, max_retries: int = DEFAULT_MAX_RETRIES) -> bool:
        """
        Convert SRA file to FASTQ using fasterq-dump.
        
        Args:
            sra_id: SRA ID to convert
            split_files: Whether to split paired-end files
            max_retries: Maximum number of retry attempts
            
        Returns:
            True if successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                cmd = [
                    str(self.fasterq_dump_exe),
                    sra_id,
                    "--outdir", str(self.output_dir),
                    "--progress"
                ]
                
                if split_files:
                    cmd.append("--split-files")
                
                with self.lock:
                    self.logger.debug(f"Converting {sra_id} to FASTQ (attempt {attempt + 1}/{max_retries})")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=DEFAULT_TIMEOUT,
                    cwd=str(self.output_dir)
                )
                
                if result.returncode == 0:
                    return True
                else:
                    with self.lock:
                        self.logger.warning(f"FASTQ conversion attempt {attempt + 1} failed for {sra_id}: {result.stderr}")
                    
                    if attempt < max_retries - 1:
                        time.sleep(DEFAULT_RETRY_DELAY)
                    
            except subprocess.TimeoutExpired:
                with self.lock:
                    self.logger.warning(f"FASTQ conversion timeout for {sra_id} (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(DEFAULT_RETRY_DELAY)
                    
            except Exception as e:
                with self.lock:
                    self.logger.error(f"FASTQ conversion error for {sra_id} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(DEFAULT_RETRY_DELAY)
        
        return False
    
    def _cleanup_sra_file(self, sra_id: str):
        """
        Clean up the downloaded SRA file to save space.
        
        Args:
            sra_id: SRA ID to clean up
        """
        try:
            # SRA files are typically stored in a subdirectory
            sra_file = self.output_dir / sra_id / f"{sra_id}.sra"
            if sra_file.exists():
                sra_file.unlink()
                self.logger.debug(f"Cleaned up SRA file for {sra_id}")
                
            # Also try to remove the directory if it's empty
            sra_dir = self.output_dir / sra_id
            if sra_dir.exists() and sra_dir.is_dir():
                try:
                    sra_dir.rmdir()  # Only removes if empty
                    self.logger.debug(f"Removed empty SRA directory for {sra_id}")
                except OSError:
                    pass  # Directory not empty, that's fine
                    
        except Exception as e:
            self.logger.debug(f"Could not clean up SRA file for {sra_id}: {e}")
    
    def get_download_status(self, sra_ids: List[str]) -> Dict[str, str]:
        """
        Check the download status of SRA IDs.
        
        Args:
            sra_ids: List of SRA IDs to check
            
        Returns:
            Dictionary mapping SRA ID to status ('downloaded', 'partial', 'missing')
        """
        status = {}
        
        for sra_id in sra_ids:
            # Check for FASTQ files
            fastq_files = list(self.output_dir.glob(f"{sra_id}*.fastq"))
            
            if fastq_files:
                status[sra_id] = 'downloaded'
            else:
                # Check for SRA file
                sra_file = self.output_dir / sra_id / f"{sra_id}.sra"
                if sra_file.exists():
                    status[sra_id] = 'partial'
                else:
                    status[sra_id] = 'missing'
        
        return status