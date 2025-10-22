# Seq_GEO_Downloader

A user-friendly tool for downloading RNA-seq data from NCBI's SRA database with automatic SRA Toolkit management and interactive guidance.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the downloader
python seq_downloader.py

# Get help
python seq_downloader.py --help
```

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Input Formats](#input-formats)
- [Examples](#examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Requirements](#requirements)

## ✨ Features

### Core Functionality
- **Interactive Interface**: Step-by-step guidance with helpful prompts
- **Dual Input Methods**: GSE numbers or SRA accession list files
- **Automatic Setup**: SRA Toolkit installation and verification
- **Parallel Downloads**: Configurable thread count (1-16 threads)
- **Progress Tracking**: Real-time download status and progress bars
- **Smart File Handling**: Existing file detection and conflict resolution
- **Comprehensive Logging**: Detailed logs and error reporting

### Advanced Features
- **Network Recovery**: Automatic retry with exponential backoff
- **Disk Space Checking**: Pre-download space validation
- **Permission Validation**: Directory access verification
- **File Integrity**: Size and format validation
- **Graceful Cancellation**: Clean exit at any point
- **Inline Help**: Context-sensitive help at every step

## 🔧 Installation

### Prerequisites
- **Python 3.7+** (Python 3.8+ recommended)
- **Operating System**: Windows, macOS, or Linux (64-bit recommended)
- **Internet connection** (for downloads and API access)
- **~2GB free disk space** (for SRA Toolkit and temporary files)

### Step-by-Step Installation

1. **Clone or download** this repository
2. **Navigate** to the project directory
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Verify installation**:
   ```bash
   python seq_downloader.py --version
   ```

### Alternative Installation Methods

**Using virtual environment (recommended):**
```bash
# Create virtual environment
python -m venv seq_downloader_env

# Activate virtual environment
# Windows:
seq_downloader_env\Scripts\activate
# Linux/macOS:
source seq_downloader_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Using conda:**
```bash
# Create conda environment
conda create -n seq_downloader python=3.8
conda activate seq_downloader

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Interactive Mode (Recommended)

Simply run the script and follow the prompts:

```bash
python seq_downloader.py
```

The tool will guide you through:
1. **Input method selection** (GSE or file)
2. **Data source specification** (GSE number or file path)
3. **Download configuration** (directory, threads, options)
4. **Preview and confirmation**
5. **Download execution** with progress tracking

### Command Line Help

```bash
# Show main help
python seq_downloader.py --help

# Show usage examples
python seq_downloader.py --examples

# Show file format specifications
python seq_downloader.py --formats

# Show troubleshooting guide
python seq_downloader.py --troubleshoot

# Show version information
python seq_downloader.py --version
```

### Inline Help

During interactive mode, type `help` at any prompt for context-specific guidance:

```
Enter GSE number (e.g., GSE123456): help
[Shows detailed GSE format help and examples]

Enter number of threads (1-16, default: 6): help
[Shows thread count performance guidance]
```

## 📁 Input Formats

### GSE Numbers

**Format**: `GSE` followed by digits

**Examples**:
- `GSE123456` - Standard format
- `GSE98765` - Another valid GSE
- `GSE1` - Short number also valid

**How it works**:
1. Tool queries NCBI GEO database
2. Fetches dataset metadata (title, description, sample count)
3. Retrieves all associated SRA accession numbers
4. Shows preview before downloading

**Find GSE numbers at**: https://www.ncbi.nlm.nih.gov/geo/

### SRA List Files

**Supported formats**: `.txt`, `.csv`, `.tsv`

**SRA accession format**: `(SRR|ERR|DRR)` + digits
- `SRR` - NCBI Sequence Read Archive
- `ERR` - EBI European Read Archive  
- `DRR` - DDBJ Read Archive

**Example files**:

**Plain text** (`sra_list.txt`):
```
# RNA-seq samples for project X
SRR1234567
SRR1234568
SRR1234569
```

**CSV format** (`sra_list.csv`):
```
accession,sample_name,condition
SRR1234567,Sample1,Control
SRR1234568,Sample2,Treatment
SRR1234569,Sample3,Control
```

**TSV format** (`sra_list.tsv`):
```
accession	sample_name	condition
SRR1234567	Sample1	Control
SRR1234568	Sample2	Treatment
SRR1234569	Sample3	Control
```

**File format notes**:
- Only the first column is used (accession column)
- Lines starting with `#` are comments
- Empty lines are ignored
- Duplicates are automatically removed
- Extra whitespace is trimmed

## 💡 Examples

### Example 1: Download Complete Dataset by GSE

```bash
$ python seq_downloader.py

Welcome to Seq Downloader v1.0.0
--------------------------------------------------
💡 Help: GSE numbers automatically fetch SRA accessions from NCBI GEO
   SRA list files let you specify exact accessions to download
   Type 'help' for more information or Ctrl+C to exit

Choose input method:
1. Enter GSE number
2. Provide SRA list file
Choice (1 or 2): 1

💡 GSE Format: GSE followed by digits (e.g., GSE123456)
   Find GSE numbers at: https://www.ncbi.nlm.nih.gov/geo/
   Type 'help' for examples or 'back' to return to main menu

Enter GSE number (e.g., GSE123456): GSE98765

Fetching SRA accessions for GSE98765...
Found dataset: Transcriptome analysis of treatment response
Sample count: 12
SRA accessions: 12

💡 Output Directory: Where downloaded FASTQ files will be saved
   Default: downloads (created automatically)
   Examples: ./my_data, C:\Users\Name\Downloads\RNA_data
   Type 'help' for more information

Enter output directory (default: downloads): ./rna_data

💡 Thread Count: Number of parallel downloads (higher = faster)
   Range: 1-16 threads, Default: 6
   Recommendation: 4-8 threads for most systems
   Type 'help' for performance guidance

Enter number of threads (1-16, default: 6): 4

💡 File Splitting: For paired-end data (Read 1 and Read 2)
   Yes: Creates separate _1.fastq and _2.fastq files
   No: Creates single merged .fastq file
   Type 'help' for more details

Split paired-end files? (y/n, default: y): y

============================================================
DOWNLOAD PREVIEW
============================================================
Dataset: Transcriptome analysis of treatment response (GSE98765)
------------------------------------------------------------
Total SRA accessions to download: 12

Accessions:
   1. SRR1234567
   2. SRR1234568
   3. SRR1234569
   ... and 9 more
============================================================

Proceed with download? (y/n): y

Starting download of 12 SRA accessions
[████████████████████████████████████████] 100% (12/12) Complete
```

### Example 2: Download Specific Accessions from File

Create `my_samples.txt`:
```
SRR1234567
SRR1234568
SRR1234569
```

Run the downloader:
```bash
$ python seq_downloader.py

Choose input method:
1. Enter GSE number
2. Provide SRA list file
Choice (1 or 2): 2

💡 File Format: One SRA accession per line (SRR/ERR/DRR + digits)
   Supported: .txt, .csv, .tsv files
   Example: SRR1234567, ERR1234567, DRR1234567
   Type 'help' for file format examples or 'back' to return

Enter path to SRA list file: my_samples.txt

Loaded 3 SRA accessions from file
[Continue with download configuration...]
```

## ⚙️ Configuration

### Default Settings

The tool uses sensible defaults that work for most users:

- **Output directory**: `downloads/`
- **Thread count**: `6`
- **File splitting**: `Yes` (recommended for paired-end data)
- **Retry attempts**: `3` per failed download
- **API rate limit**: `3 requests/second` (NCBI recommended)

### Customization Options

**During runtime**:
- Output directory path
- Thread count (1-16)
- File splitting preference
- File conflict resolution (skip/overwrite/rename)

**Configuration file** (`src/config.py`):
```python
# Modify these values to change defaults
DEFAULT_THREAD_COUNT = 6
DEFAULT_OUTPUT_DIR = "downloads"
API_RETRY_MAX_ATTEMPTS = 3
DOWNLOAD_TIMEOUT_SECONDS = 3600
```

### Performance Tuning

**For fast downloads**:
- Use 8-16 threads
- Ensure stable, fast internet connection
- Use SSD storage for output directory

**For system stability**:
- Use 2-4 threads
- Monitor system resources
- Use lower thread count on older hardware

**For network reliability**:
- Use 1-2 threads on unstable connections
- Enable automatic retry (default)
- Monitor network usage

## 🔍 Troubleshooting

### Quick Diagnostics

```bash
# Show detailed troubleshooting guide
python seq_downloader.py --troubleshoot

# Check version and system info
python seq_downloader.py --version

# Test with minimal example
# Create test_file.txt with one SRA accession
echo SRR1234567 > test_file.txt
python seq_downloader.py
```

### Common Issues

**"GSE number not found"**
- Verify GSE exists at https://www.ncbi.nlm.nih.gov/geo/
- Check if dataset has associated SRA data
- Try using SRA list file instead

**"SRA Toolkit installation failed"**
- Check internet connection
- Run as administrator (Windows)
- Try manual installation (see troubleshooting guide)

**"Permission denied"**
- Choose different output directory
- Check folder permissions
- Run as administrator if necessary

**"Network error" or timeouts**
- Check internet connection
- Wait and retry (NCBI servers may be busy)
- Use fewer threads to reduce connection load

**"Insufficient disk space"**
- Free up disk space (estimate ~100-500MB per SRA file)
- Choose different output directory
- Download fewer files at once

### Log Files

Detailed logs are saved in the `logs/` directory:
- `seq_downloader.log` - Main application log
- Timestamped logs for each session
- Error details and stack traces
- Performance metrics

### Getting Help

1. **Built-in help**: Use `--help`, `--troubleshoot`, or type `help` during prompts
2. **Log analysis**: Check log files in `logs/` directory
3. **Test with small dataset**: Try 1-2 SRA accessions first
4. **Verify requirements**: Ensure Python 3.7+, Windows OS, internet connection

## 📂 Project Structure

```
seq-downloader/
├── seq_downloader.py          # Main entry point with CLI
├── requirements.txt           # Python dependencies
├── test_requirements.txt      # Testing dependencies
├── README.md                 # This documentation
├── 
├── src/                      # Source code package
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration and constants
│   ├── models.py             # Data models and classes
│   ├── input_handler.py      # User input and validation
│   ├── geo_service.py        # NCBI GEO API integration
│   ├── sra_toolkit_manager.py # SRA Toolkit management
│   ├── download_manager.py   # Download coordination
│   ├── file_manager.py       # File operations
│   ├── logger.py             # Logging and progress tracking
│   ├── error_handler.py      # Error handling and recovery
│   └── main_controller.py    # Main workflow orchestration
│
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_*.py             # Unit tests
│   ├── test_integration_*.py # Integration tests
│   └── README.md             # Testing documentation
│
├── logs/                     # Application logs (created automatically)
├── downloads/                # Default download directory (created automatically)
└── tools/                    # SRA Toolkit installation (created automatically)
    └── sratoolkit/           # SRA Toolkit binaries
```

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10+, macOS 10.12+, or Linux (Ubuntu 16.04+/CentOS 7+)
- **Architecture**: 64-bit recommended (32-bit supported on Windows/Linux)
- **Python**: 3.7 or higher (3.8+ recommended)
- **Memory**: 4GB RAM minimum, 8GB+ recommended
- **Storage**: 2GB for toolkit + space for downloaded files
- **Network**: Stable internet connection

### Python Dependencies
```
requests>=2.25.0      # HTTP requests for API calls
urllib3>=1.26.0       # URL handling and connection pooling
pathlib>=1.0.0        # Path manipulation (built-in Python 3.4+)
dataclasses>=0.6      # Data classes (built-in Python 3.7+)
```

### Optional Dependencies
```
pytest>=6.0.0         # For running tests
pytest-cov>=2.10.0    # For test coverage
```

### External Tools
- **SRA Toolkit**: Automatically downloaded and installed
- **fasterq-dump**: Part of SRA Toolkit, used for FASTQ conversion

## 📄 License

This project is provided as-is for educational and research purposes. Please ensure compliance with NCBI's terms of service when downloading data.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting guide: `python seq_downloader.py --troubleshoot`
2. Review log files in the `logs/` directory
3. Test with a small dataset first
4. Ensure all requirements are met

---


**Happy RNA-seq downloading! 🧬**
