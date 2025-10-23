"""Main controller for the seq_downloader application."""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List

from .config import DEFAULT_OUTPUT_DIR, DEFAULT_LOG_DIR
from .gse_fetcher import GSEFetcher
from .sra_downloader import SRADownloader


class MainController:
    """Main controller class for handling the interactive download process."""
    
    def __init__(self):
        """Initialize the MainController."""
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.log_dir = DEFAULT_LOG_DIR
        self.gse_fetcher = GSEFetcher()
        self.sra_downloader = None  # Will be initialized with user settings
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
        
        # Get download settings
        output_dir = self.get_output_directory()
        max_threads = self.get_thread_count()
        split_files = self.get_split_files_option()
        
        # Initialize downloader with settings
        self.sra_downloader = SRADownloader(output_dir=output_dir, max_threads=max_threads)
        
        # Start download
        print(f"\nStarting download to: {output_dir}")
        print(f"Using {max_threads} threads, split files: {split_files}")
        print("-" * 50)
        
        results = self.sra_downloader.download_sra_ids(sra_ids, split_files=split_files)
        
        # Check results
        successful = sum(1 for success in results.values() if success)
        if successful == len(sra_ids):
            print("\n✅ All downloads completed successfully!")
            return 0
        elif successful > 0:
            print(f"\n⚠️  Partial success: {successful}/{len(sra_ids)} downloads completed")
            return 1
        else:
            print("\n❌ All downloads failed")
            return 1
    
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
            
            # Get download settings
            output_dir = self.get_output_directory()
            max_threads = self.get_thread_count()
            split_files = self.get_split_files_option()
            
            # Initialize downloader with settings
            self.sra_downloader = SRADownloader(output_dir=output_dir, max_threads=max_threads)
            
            # Start download
            print(f"\nStarting download to: {output_dir}")
            print(f"Using {max_threads} threads, split files: {split_files}")
            print("-" * 50)
            
            results = self.sra_downloader.download_sra_ids(sra_ids, split_files=split_files)
            
            # Check results
            successful = sum(1 for success in results.values() if success)
            if successful == len(sra_ids):
                print("\n✅ All downloads completed successfully!")
                return 0
            elif successful > 0:
                print(f"\n⚠️  Partial success: {successful}/{len(sra_ids)} downloads completed")
                return 1
            else:
                print("\n❌ All downloads failed")
                return 1
            
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
    
    def get_thread_count(self) -> int:
        """Get the number of threads for parallel downloads."""
        print(f"\nThread count for parallel downloads (1-16, default: 4)")
        while True:
            user_input = input("Enter thread count or press Enter for default: ").strip()
            
            if not user_input:
                return 4
            
            try:
                thread_count = int(user_input)
                if 1 <= thread_count <= 16:
                    return thread_count
                else:
                    print("Please enter a number between 1 and 16.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_split_files_option(self) -> bool:
        """Get whether to split paired-end files."""
        print(f"\nSplit paired-end files? (recommended for most datasets)")
        while True:
            user_input = input("Split files (y/n, default: y): ").strip().lower()
            
            if not user_input or user_input in ['y', 'yes']:
                return True
            elif user_input in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")