#!/usr/bin/env python3
"""
RNA-seq Data Downloader

A user-friendly tool for downloading RNA-seq data from NCBI's SRA database.
Supports both GSE number input and SRA accession list files with automatic
SRA Toolkit installation and management.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.main_controller import MainController
from src.config import APP_NAME, APP_VERSION, APP_DESCRIPTION


def show_help():
    """Display comprehensive help information."""
    help_text = f"""
{APP_NAME} v{APP_VERSION}
{APP_DESCRIPTION}

USAGE:
    python seq_downloader.py [OPTIONS]

OPTIONS:
    -h, --help          Show this help message and exit
    --version           Show version information
    --examples          Show usage examples
    --formats           Show supported file formats
    --troubleshoot      Show troubleshooting guide

INTERACTIVE MODE:
    When run without arguments, the tool starts in interactive mode and guides
    you through the download process with prompts for:
    
    1. Input Method Selection:
       - GSE number (e.g., GSE123456) - automatically fetches SRA accessions
       - SRA list file - provide your own list of SRA accession IDs
    
    2. Download Configuration:
       - Output directory (where files will be saved)
       - Thread count (1-16, for parallel downloads)
       - File splitting options (for paired-end sequencing data)
    
    3. File Conflict Resolution:
       - Skip existing files
       - Overwrite existing files  
       - Rename to avoid conflicts

INPUT FORMATS:

    GSE Numbers:
        Format: GSE followed by digits (e.g., GSE123456, GSE98765)
        The tool automatically fetches associated SRA accessions from NCBI GEO
    
    SRA List Files:
        Supported formats: .txt, .csv, .tsv
        Content: One SRA accession per line
        Supported accession formats: SRR, ERR, DRR followed by digits
        
        Example file content:
            SRR1234567
            SRR1234568
            SRR1234569

FEATURES:
    ✓ Automatic SRA Toolkit installation and management
    ✓ Parallel downloads with progress tracking
    ✓ Intelligent handling of existing files
    ✓ Comprehensive error handling and recovery
    ✓ Detailed logging and reporting
    ✓ Network failure recovery with retry logic
    ✓ Disk space and permission checking

REQUIREMENTS:
    - Python 3.7 or higher
    - Internet connection
    - Windows, macOS, or Linux operating system
    - Sufficient disk space for downloaded files

For more detailed information, use:
    python seq_downloader.py --examples
    python seq_downloader.py --troubleshoot
"""
    print(help_text)


def show_examples():
    """Display usage examples."""
    examples_text = """
USAGE EXAMPLES:

1. Download data using a GSE number:
   
   $ python seq_downloader.py
   
   Choose input method:
   1. Enter GSE number
   2. Provide SRA list file
   Choice (1 or 2): 1
   
   Enter GSE number (e.g., GSE123456): GSE98765
   
   The tool will automatically:
   - Fetch SRA accessions associated with GSE98765
   - Show dataset information and sample count
   - Prompt for download options
   - Download all associated FASTQ files

2. Download data using an SRA list file:
   
   Create a file called 'my_sra_list.txt' with content:
   SRR1234567
   SRR1234568
   SRR1234569
   
   $ python seq_downloader.py
   
   Choose input method:
   1. Enter GSE number  
   2. Provide SRA list file
   Choice (1 or 2): 2
   
   Enter path to SRA list file: my_sra_list.txt

3. Typical workflow example:
   
   $ python seq_downloader.py
   
   Welcome to RNA-seq Downloader v1.0.0
   --------------------------------------------------
   Choose input method:
   1. Enter GSE number
   2. Provide SRA list file
   Choice (1 or 2): 1
   
   Enter GSE number (e.g., GSE123456): GSE98765
   
   Fetching SRA accessions for GSE98765...
   Found dataset: RNA-seq analysis of sample conditions
   Sample count: 12
   SRA accessions: 12
   
   Enter output directory (default: downloads): ./my_data
   Enter number of threads (1-16, default: 6): 4
   Split paired-end files? (y/n, default: y): y
   
   ============================================================
   DOWNLOAD PREVIEW
   ============================================================
   Dataset: RNA-seq analysis of sample conditions (GSE98765)
   ------------------------------------------------------------
   Total SRA accessions to download: 12
   
   Accessions:
     1. SRR1234567
     2. SRR1234568
     ...and 10 more
   ============================================================
   
   Proceed with download? (y/n): y
   
   Starting download of 12 SRA accessions
   [Progress tracking and download status displayed]

SRA LIST FILE FORMATS:

Plain text (.txt):
    SRR1234567
    SRR1234568
    SRR1234569

CSV format (.csv):
    accession,sample_name,condition
    SRR1234567,Sample1,Control
    SRR1234568,Sample2,Treatment
    SRR1234569,Sample3,Control

TSV format (.tsv):
    accession	sample_name	condition
    SRR1234567	Sample1	Control
    SRR1234568	Sample2	Treatment
    SRR1234569	Sample3	Control

Note: For CSV/TSV files, only the first column (accession) is used.
      Lines starting with # are treated as comments and ignored.
"""
    print(examples_text)


def show_formats():
    """Display supported file formats and specifications."""
    formats_text = """
SUPPORTED FILE FORMATS:

INPUT FORMATS:

1. GSE Numbers:
   Format: GSE + digits
   Examples: GSE123456, GSE98765, GSE1234
   
   Valid:   GSE123456, GSE1, GSE999999
   Invalid: gse123456, GSE, 123456, GSE-123

2. SRA Accession Files:
   Extensions: .txt, .csv, .tsv
   
   SRA Accession Format: (SRR|ERR|DRR) + digits
   Examples: SRR1234567, ERR1234567, DRR1234567
   
   Valid:   SRR1234567, ERR999, DRR123456789
   Invalid: srr1234567, SRA1234567, RR1234567

FILE CONTENT EXAMPLES:

Plain Text File (sra_list.txt):
    # This is a comment line
    SRR1234567
    SRR1234568
    
    # Empty lines are ignored
    SRR1234569

CSV File (sra_list.csv):
    # Header line (optional)
    accession,sample_name,condition
    SRR1234567,Sample_1,Control
    SRR1234568,Sample_2,Treatment
    SRR1234569,Sample_3,Control

TSV File (sra_list.tsv):
    accession	sample_name	condition
    SRR1234567	Sample_1	Control
    SRR1234568	Sample_2	Treatment
    SRR1234569	Sample_3	Control

OUTPUT FORMATS:

Downloaded files will be in FASTQ format:
- Single-end: [accession].fastq
- Paired-end (split): [accession]_1.fastq, [accession]_2.fastq
- Paired-end (merged): [accession].fastq

File compression: Files may be compressed (.fastq.gz) depending on 
SRA Toolkit settings and available disk space.

DIRECTORY STRUCTURE:

Default output structure:
    downloads/
    ├── SRR1234567.fastq
    ├── SRR1234568_1.fastq
    ├── SRR1234568_2.fastq
    └── SRR1234569.fastq

Custom output directory:
    my_data/
    ├── SRR1234567.fastq
    ├── SRR1234568_1.fastq
    ├── SRR1234568_2.fastq
    └── SRR1234569.fastq
"""
    print(formats_text)


def show_troubleshooting():
    """Display troubleshooting guide."""
    troubleshooting_text = """
TROUBLESHOOTING GUIDE:

COMMON ISSUES AND SOLUTIONS:

1. "GSE number not found" Error:
   Problem: The GSE number doesn't exist or has no SRA data
   Solutions:
   - Verify the GSE number at https://www.ncbi.nlm.nih.gov/geo/
   - Check if the dataset has associated SRA data
   - Try using SRA accession list file instead
   - Ensure GSE format is correct (GSE + digits)

2. "SRA Toolkit installation failed" Error:
   Problem: Automatic toolkit installation encountered issues
   Solutions:
   - Check internet connection and firewall settings
   - Run as administrator (Windows)
   - Manually download from: https://github.com/ncbi/sra-tools/wiki
   - Extract to: tools/sratoolkit/ directory
   - Ensure fasterq-dump.exe is in bin/ subdirectory

3. "Permission denied" Error:
   Problem: No write access to output directory
   Solutions:
   - Choose a different output directory
   - Run as administrator (Windows)
   - Check folder permissions
   - Ensure parent directory exists

4. "Network error" or "API timeout" Error:
   Problem: Connection issues with NCBI servers
   Solutions:
   - Check internet connection
   - Wait and try again (servers may be busy)
   - Use SRA list file instead of GSE lookup
   - Check firewall/proxy settings

5. "Insufficient disk space" Error:
   Problem: Not enough space for downloads
   Solutions:
   - Free up disk space
   - Choose different output directory
   - Download fewer files at once
   - Check available space: each SRA file ~50-500MB

6. "Download failed" or "File corruption" Error:
   Problem: Individual download failures
   Solutions:
   - Retry the download (tool has automatic retry)
   - Check internet stability
   - Reduce thread count (use fewer parallel downloads)
   - Verify SRA accession exists at NCBI

7. "Invalid SRA accession" Error:
   Problem: Malformed accession IDs in list file
   Solutions:
   - Check accession format: SRR/ERR/DRR + digits
   - Remove extra spaces or characters
   - Verify accessions at https://www.ncbi.nlm.nih.gov/sra/
   - Check file encoding (use UTF-8)

PERFORMANCE OPTIMIZATION:

1. Slow Downloads:
   - Increase thread count (up to 16)
   - Check internet speed
   - Use wired connection instead of WiFi
   - Close other network-intensive applications

2. High Memory Usage:
   - Reduce thread count
   - Download fewer files simultaneously
   - Close other applications

3. System Responsiveness:
   - Reduce thread count to 2-4
   - Run during off-peak hours
   - Monitor system resources

GETTING HELP:

1. Check log files in the 'logs/' directory for detailed error information
2. Verify system requirements (Python 3.7+, Windows OS)
3. Test with a small dataset first (1-2 SRA accessions)
4. Ensure stable internet connection throughout download

MANUAL SRA TOOLKIT INSTALLATION:

If automatic installation fails:

1. Download from: https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit
2. Choose "Windows 64-bit" version
3. Extract to: [application_folder]/tools/sratoolkit/
4. Verify structure:
   tools/
   └── sratoolkit/
       └── bin/
           ├── fasterq-dump.exe
           ├── prefetch.exe
           └── [other tools]

5. Test installation:
   tools/sratoolkit/bin/fasterq-dump.exe --help

CONTACT AND RESOURCES:

- NCBI SRA: https://www.ncbi.nlm.nih.gov/sra/
- SRA Toolkit: https://github.com/ncbi/sra-tools
- GEO Database: https://www.ncbi.nlm.nih.gov/geo/
- File format help: Use --formats option
"""
    print(troubleshooting_text)


def show_version():
    """Display version information."""
    version_text = f"""
{APP_NAME} v{APP_VERSION}

{APP_DESCRIPTION}

Python version: {sys.version}
Platform: {sys.platform}

For help: python seq_downloader.py --help
For examples: python seq_downloader.py --examples
"""
    print(version_text)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=APP_DESCRIPTION,
        add_help=False  # We'll handle help ourselves
    )
    
    parser.add_argument('-h', '--help', action='store_true',
                       help='Show help message and exit')
    parser.add_argument('--version', action='store_true',
                       help='Show version information')
    parser.add_argument('--examples', action='store_true',
                       help='Show usage examples')
    parser.add_argument('--formats', action='store_true',
                       help='Show supported file formats')
    parser.add_argument('--troubleshoot', action='store_true',
                       help='Show troubleshooting guide')
    
    return parser.parse_args()


def main():
    """Main entry point for the RNA-seq downloader."""
    try:
        args = parse_arguments()
        
        # Handle command line options
        if args.help:
            show_help()
            return 0
        elif args.version:
            show_version()
            return 0
        elif args.examples:
            show_examples()
            return 0
        elif args.formats:
            show_formats()
            return 0
        elif args.troubleshoot:
            show_troubleshooting()
            return 0
        
        # Run interactive mode
        controller = MainController()
        exit_code = controller.run()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("\nFor troubleshooting help, run:")
        print("python seq_downloader.py --troubleshoot")
        sys.exit(1)


if __name__ == "__main__":
    main()