"""Main controller for the seq_downloader application."""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List

from .config import DEFAULT_OUTPUT_DIR, DEFAULT_LOG_DIR
from .gse_fetcher import GSEFetcher


class MainController:
    """Main controller class for handling the interactive download process."""
    
    def __init__(self):
        """Initialize the MainController."""
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.log_dir = DEFAULT_LOG_DIR
        self.gse_fetcher = GSEFetcher()
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging configuration."""
        # Create logs directory if it doesn't exist
        Path(self.log_dir).mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Path(self.log_dir) / 'main.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run(self) -> int:
        """Run the interactive download process."""
        try:
            print("Welcome to seq_downloader!")
            print("This tool helps you download sequencing data from SRA and GSE numbers.")
            print()
            
            # Get download method choice
            choice = self.get_download_method()
            
            if choice == '1':
                return self.handle_sra_download()
            elif choice == '2':
                return self.handle_gse_download()
            else:
                print("Invalid choice. Exiting.")
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"An unexpected error occurred: {e}")
            return 1
    
    def get_download_method(self) -> str:
        """Get the user's choice for download method."""
        print("Choose download method:")
        print("1. Download from SRA ID(s)")
        print("2. Download from GSE number")
        print()
        
        while True:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                return choice
            print("Please enter 1 or 2.")
    
    def handle_sra_download(self) -> int:
        """Handle SRA ID download process."""
        print("\nSRA ID Download")
        print("Enter SRA IDs separated by commas (e.g., SRR123456, SRR789012)")
        
        sra_ids_input = input("SRA IDs: ").strip()
        if not sra_ids_input:
            print("No SRA IDs provided. Exiting.")
            return 1
        
        # Parse SRA IDs
        sra_ids = [sra_id.strip() for sra_id in sra_ids_input.split(',')]
        sra_ids = [sra_id for sra_id in sra_ids if sra_id]  # Remove empty strings
        
        if not sra_ids:
            print("No valid SRA IDs provided. Exiting.")
            return 1
        
        print(f"Will download {len(sra_ids)} SRA ID(s): {', '.join(sra_ids)}")
        
        # Get output directory
        output_dir = self.get_output_directory()
        
        # Simulate download process (replace with actual implementation)
        print(f"Starting download to: {output_dir}")
        for sra_id in sra_ids:
            print(f"Processing {sra_id}...")
            # TODO: Implement actual SRA download logic
        
        print("Download completed successfully!")
        return 0
    
    def handle_gse_download(self) -> int:
        """Handle GSE number download process."""
        print("\nGSE Number Download")
        print("Enter a GSE number (e.g., GSE123456)")
        
        gse_number = input("GSE Number: ").strip()
        if not gse_number:
            print("No GSE number provided. Exiting.")
            return 1
        
        # Validate GSE format
        if not gse_number.upper().startswith('GSE'):
            print("GSE number must start with 'GSE'. Exiting.")
            return 1
        
        print(f"Fetching SRA IDs for {gse_number}...")
        
        try:
            # Fetch SRA IDs from GSE number
            sra_ids = self.gse_fetcher.fetch_sra_ids(gse_number)
            
            if not sra_ids:
                print(f"No SRA IDs found for {gse_number}.")
                return 1
            
            print(f"Found {len(sra_ids)} SRA ID(s): {', '.join(sra_ids)}")
            
            # Get output directory
            output_dir = self.get_output_directory()
            
            # Simulate download process (replace with actual implementation)
            print(f"Starting download to: {output_dir}")
            for sra_id in sra_ids:
                print(f"Processing {sra_id}...")
                # TODO: Implement actual SRA download logic
            
            print("Download completed successfully!")
            return 0
            
        except Exception as e:
            self.logger.error(f"Error fetching SRA IDs for {gse_number}: {e}")
            print(f"Error fetching SRA IDs: {e}")
            return 1
    
    def get_output_directory(self) -> str:
        """Get the output directory from user or use default."""
        print(f"\nOutput directory (default: {self.output_dir})")
        user_output = input("Enter output directory or press Enter for default: ").strip()
        
        if user_output:
            output_dir = user_output
        else:
            output_dir = self.output_dir
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        return output_dir