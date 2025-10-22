# RNA-seq Downloader Usage Examples

This document provides detailed examples of how to use the RNA-seq Downloader in various scenarios.

## 📋 Table of Contents

- [Basic Examples](#basic-examples)
- [Advanced Usage](#advanced-usage)
- [File Format Examples](#file-format-examples)
- [Workflow Examples](#workflow-examples)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting Examples](#troubleshooting-examples)

## 🚀 Basic Examples

### Example 1: Download Complete Dataset by GSE Number

**Scenario**: You found an interesting RNA-seq study (GSE98765) and want to download all associated data.

**Steps**:
```bash
$ python seq_downloader.py

Welcome to RNA-seq Downloader v1.0.0
--------------------------------------------------
💡 Help: GSE numbers automatically fetch SRA accessions from NCBI GEO
   SRA list files let you specify exact accessions to download
   Type 'help' for more information or Ctrl+C to exit

Choose input method:
1. Enter GSE number (auto-fetch SRA accessions)
2. Provide SRA list file (specify exact accessions)
Choice (1 or 2): 1

💡 GSE Format: GSE followed by digits (e.g., GSE123456)
   Find GSE numbers at: https://www.ncbi.nlm.nih.gov/geo/
   Type 'help' for examples or 'back' to return to main menu

Enter GSE number (e.g., GSE123456): GSE98765

Fetching SRA accessions for GSE98765...
Found dataset: RNA-seq analysis of drug treatment effects in cancer cells
Sample count: 18
SRA accessions: 18

💡 Output Directory: Where downloaded FASTQ files will be saved
   Default: downloads (created automatically)
   Examples: ./my_data, C:\Users\Name\Downloads\RNA_data
   Type 'help' for more information

Enter output directory (default: downloads): ./cancer_study_data

💡 Thread Count: Number of parallel downloads (higher = faster)
   Range: 1-16 threads, Default: 6
   Recommendation: 4-8 threads for most systems
   Type 'help' for performance guidance

Enter number of threads (1-16, default: 6): 6

💡 File Splitting: For paired-end data (Read 1 and Read 2)
   Yes: Creates separate _1.fastq and _2.fastq files
   No: Creates single merged .fastq file
   Type 'help' for more details

Split paired-end files? (y/n, default: y): y

============================================================
DOWNLOAD PREVIEW
============================================================
Dataset: RNA-seq analysis of drug treatment effects in cancer cells (GSE98765)
------------------------------------------------------------
Total SRA accessions to download: 18

Accessions:
   1. SRR5123456
   2. SRR5123457
   3. SRR5123458
   ... and 15 more
============================================================

Download Configuration:
  Output directory: C:\Users\Name\Projects\cancer_study_data
  Thread count: 6
  Split files: True

Proceed with download? (y/n): y

Checking SRA Toolkit installation...
SRA Toolkit found and verified

Checking directory permissions and disk space...
✓ Directory permissions: OK
✓ Available disk space: 45.2 GB (estimated need: 3.6 GB)

Starting download of 18 SRA accessions
[████████████████████████████████████████] 100% (18/18) Complete

DOWNLOAD SUMMARY
================
✓ Successful downloads: 18
✗ Failed downloads: 0
📁 Output directory: C:\Users\Name\Projects\cancer_study_data
⏱️  Total time: 45 minutes 23 seconds
💾 Total size: 3.2 GB

All downloads completed successfully!
```

**Result**: 18 paired-end FASTQ files downloaded to `./cancer_study_data/`

### Example 2: Download Specific Samples Using SRA List

**Scenario**: You only need specific samples from a study, not the entire dataset.

**Step 1**: Create SRA list file (`my_samples.txt`):
```
# Control samples only
SRR5123456
SRR5123457
SRR5123458
# Treatment samples
SRR5123465
SRR5123466
SRR5123467
```

**Step 2**: Run the downloader:
```bash
$ python seq_downloader.py

Choose input method:
1. Enter GSE number (auto-fetch SRA accessions)
2. Provide SRA list file (specify exact accessions)
Choice (1 or 2): 2

💡 File Format: One SRA accession per line (SRR/ERR/DRR + digits)
   Supported: .txt, .csv, .tsv files
   Example: SRR1234567, ERR1234567, DRR1234567
   Type 'help' for file format examples or 'back' to return

Enter path to SRA list file: my_samples.txt

Loaded 6 SRA accessions from file

Enter output directory (default: downloads): ./selected_samples
Enter number of threads (1-16, default: 6): 4
Split paired-end files? (y/n, default: y): y

============================================================
DOWNLOAD PREVIEW
============================================================
Total SRA accessions to download: 6

Accessions:
   1. SRR5123456
   2. SRR5123457
   3. SRR5123458
   4. SRR5123465
   5. SRR5123466
   6. SRR5123467
============================================================

Proceed with download? (y/n): y

[Download proceeds...]
```

## 🔧 Advanced Usage

### Example 3: High-Performance Download Setup

**Scenario**: You have a fast internet connection and powerful computer, want maximum download speed.

```bash
$ python seq_downloader.py

# Choose GSE or file input as usual...

Enter output directory (default: downloads): D:\RNA_Data  # Use fast SSD drive
Enter number of threads (1-16, default: 6): 12           # High thread count
Split paired-end files? (y/n, default: y): y

# System will warn about high thread count:
Warning: Using 12 threads may impact system performance.
Continue with this thread count? (y/n): y

[Download with 12 parallel threads...]
```

**Performance tips**:
- Use SSD for output directory
- Close other network-intensive applications
- Monitor system resources during download
- Consider reducing threads if system becomes unresponsive

### Example 4: Conservative/Stable Download Setup

**Scenario**: You have a slower or unstable internet connection, prioritize reliability over speed.

```bash
$ python seq_downloader.py

# Choose input method...

Enter output directory (default: downloads): ./downloads
Enter number of threads (1-16, default: 6): 2            # Low thread count
Split paired-end files? (y/n, default: y): y

[Stable download with automatic retry on failures...]
```

**Stability benefits**:
- Fewer simultaneous connections
- Less likely to overwhelm network
- Better recovery from temporary connection issues
- Lower system resource usage

### Example 5: Handling File Conflicts

**Scenario**: You're re-running a download and some files already exist.

```bash
$ python seq_downloader.py

# ... setup as usual ...

Checking for existing files...

File already exists: SRR5123456_1.fastq
1. Skip (keep existing file)
2. Overwrite (re-download)  
3. Rename (keep both versions)
Choice (1-3): 1

File already exists: SRR5123457_1.fastq
1. Skip (keep existing file)
2. Overwrite (re-download)
3. Rename (keep both versions)
Choice (1-3): 2

File already exists: SRR5123458_1.fastq
1. Skip (keep existing file)
2. Overwrite (re-download)
3. Rename (keep both versions)
Choice (1-3): 3

Starting download of remaining files...
✓ Skipped: SRR5123456 (file exists)
⬇️ Re-downloading: SRR5123457 (overwrite)
📝 Renaming: SRR5123458 → SRR5123458_20241022_143022.fastq (keep both)
```

## 📁 File Format Examples

### SRA List File Formats

#### Plain Text Format (.txt)
```
# Project: Cancer drug response study
# Date: 2024-10-22
# Control samples
SRR5123456
SRR5123457
SRR5123458

# Treatment samples  
SRR5123465
SRR5123466
SRR5123467

# Note: Lines starting with # are comments
# Empty lines are ignored
```

#### CSV Format (.csv)
```csv
accession,sample_name,condition,replicate
SRR5123456,Control_1,Control,1
SRR5123457,Control_2,Control,2
SRR5123458,Control_3,Control,3
SRR5123465,Treatment_1,Drug_A,1
SRR5123466,Treatment_2,Drug_A,2
SRR5123467,Treatment_3,Drug_A,3
```

#### TSV Format (.tsv)
```tsv
accession	sample_name	condition	time_point	batch
SRR5123456	Ctrl_T0_1	Control	0h	Batch1
SRR5123457	Ctrl_T0_2	Control	0h	Batch1
SRR5123458	Ctrl_T24_1	Control	24h	Batch2
SRR5123465	Drug_T0_1	Treatment	0h	Batch1
SRR5123466	Drug_T24_1	Treatment	24h	Batch2
```

**Note**: Only the first column (accession) is used for downloads. Additional columns are for your reference.

## 🔄 Workflow Examples

### Example 6: Complete Research Workflow

**Step 1**: Find your dataset
```bash
# Visit https://www.ncbi.nlm.nih.gov/geo/
# Search: "breast cancer RNA-seq 2023"
# Found interesting study: GSE123456
```

**Step 2**: Get dataset information
```bash
$ python seq_downloader.py --examples  # Review examples first

$ python seq_downloader.py

Choose input method:
1. Enter GSE number (auto-fetch SRA accessions)
2. Provide SRA list file (specify exact accessions)
Choice (1 or 2): 1

Enter GSE number (e.g., GSE123456): GSE123456

Fetching SRA accessions for GSE123456...
Found dataset: Comprehensive transcriptome analysis of breast cancer subtypes
Sample count: 48
SRA accessions: 48
```

**Step 3**: Plan your download
```bash
# Large dataset - plan accordingly:
# 48 samples × ~200MB each = ~9.6GB total
# Choose appropriate output directory with enough space

Enter output directory (default: downloads): D:\Research\BreastCancer_GSE123456
Enter number of threads (1-16, default: 6): 8  # Fast download
Split paired-end files? (y/n, default: y): y   # Standard for RNA-seq
```

**Step 4**: Monitor and verify
```bash
# Download completes...
DOWNLOAD SUMMARY
================
✓ Successful downloads: 47
✗ Failed downloads: 1 (SRR7654321 - network timeout)
📁 Output directory: D:\Research\BreastCancer_GSE123456
⏱️  Total time: 2 hours 15 minutes
💾 Total size: 9.2 GB

# Retry failed download:
$ echo SRR7654321 > retry_list.txt
$ python seq_downloader.py
# Choose file input, use retry_list.txt
```

### Example 7: Batch Processing Multiple Studies

**Scenario**: Download data from multiple related studies.

**Create study list** (`studies_to_download.txt`):
```
# Study 1: Primary tumors
GSE123456

# Study 2: Metastatic samples  
GSE789012

# Study 3: Treatment response
GSE345678
```

**Download each study**:
```bash
# Study 1
$ python seq_downloader.py
# Input: GSE123456
# Output: ./Study1_Primary

# Study 2  
$ python seq_downloader.py
# Input: GSE789012
# Output: ./Study2_Metastatic

# Study 3
$ python seq_downloader.py  
# Input: GSE345678
# Output: ./Study3_Treatment
```

**Organize results**:
```
RNA_seq_Project/
├── Study1_Primary/
│   ├── SRR1111111_1.fastq
│   ├── SRR1111111_2.fastq
│   └── [more files...]
├── Study2_Metastatic/
│   ├── SRR2222222_1.fastq
│   ├── SRR2222222_2.fastq
│   └── [more files...]
└── Study3_Treatment/
    ├── SRR3333333_1.fastq
    ├── SRR3333333_2.fastq
    └── [more files...]
```

## ⚡ Performance Optimization

### Example 8: Optimizing for Different Scenarios

#### Fast Internet, Powerful Computer
```bash
# Configuration for maximum speed:
Thread count: 12-16
Output directory: SSD drive (D:\, E:\)
Network: Wired connection
Other apps: Closed during download
```

#### Slow/Unstable Internet
```bash
# Configuration for reliability:
Thread count: 1-2
Retry attempts: Automatic (built-in)
Network: Most stable available
Monitoring: Watch for connection drops
```

#### Limited Disk Space
```bash
# Download in batches:
# Batch 1: First 10 samples
# Linux/macOS:
echo -e "SRR1\nSRR2\n...\nSRR10" > batch1.txt
# Windows:
echo SRR1 > batch1.txt && echo SRR2 >> batch1.txt

python seq_downloader.py  # Use batch1.txt

# Process/compress/move files...

# Batch 2: Next 10 samples  
# Linux/macOS:
echo -e "SRR11\nSRR12\n...\nSRR20" > batch2.txt
# Windows:
echo SRR11 > batch2.txt && echo SRR12 >> batch2.txt

python seq_downloader.py  # Use batch2.txt
```

#### Shared/Corporate Network
```bash
# Configuration for network-friendly downloading:
Thread count: 2-4 (be considerate)
Timing: Off-peak hours
Monitoring: Watch network usage
Coordination: Inform IT if downloading large datasets
```

## 🔍 Troubleshooting Examples

### Example 9: Common Error Scenarios

#### GSE Not Found Error
```bash
$ python seq_downloader.py

Enter GSE number (e.g., GSE123456): GSE999999

Error: GSE number GSE999999 not found or has no associated data

# Solutions:
# 1. Verify GSE exists at https://www.ncbi.nlm.nih.gov/geo/
# 2. Check if GSE has SRA data (some only have microarray)
# 3. Try different GSE or use SRA list file
```

#### Network Timeout During Download
```bash
Starting download of 20 SRA accessions
[████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 60% (12/20)

ERROR: Download failed for SRR5555555 - Connection timeout
Retrying... (attempt 2/3)
ERROR: Download failed for SRR5555555 - Connection timeout  
Retrying... (attempt 3/3)
ERROR: Download failed for SRR5555555 - Connection timeout
Continuing with remaining downloads...

# The tool continues with other downloads
# Failed downloads are reported in final summary
# You can retry failed downloads separately
```

#### Permission Denied Error
```bash
Enter output directory (default: downloads): C:\Program Files\MyData

Error: No write permission for directory: C:\Program Files

# Solutions:
# 1. Choose different directory: C:\Users\YourName\Documents\RNA_data
# 2. Run as administrator
# 3. Use default directory: downloads
```

### Example 10: Recovery Scenarios

#### Interrupted Download Recovery
```bash
# Download was interrupted at 70% completion
# Restart the tool with same settings:

$ python seq_downloader.py

# Use same GSE/file and output directory
# Tool will detect existing files:

File already exists: SRR1111111_1.fastq
1. Skip (keep existing file)
2. Overwrite (re-download)
3. Rename (keep both versions)
Choice (1-3): 1  # Skip completed files

# Only remaining files will be downloaded
```

#### Partial File Recovery
```bash
# Some files downloaded but are incomplete/corrupted
# Tool automatically detects files < 1KB as incomplete

Checking existing files...
Found incomplete file: SRR2222222_1.fastq (0 bytes)
This file will be re-downloaded.

Found complete file: SRR3333333_1.fastq (150 MB)
File already exists. Choose action:
1. Skip (keep existing file)
2. Overwrite (re-download)
3. Rename (keep both versions)
Choice (1-3): 1  # Keep good files
```

## 📊 Output Examples

### Example File Structure After Download

#### Single-end Data
```
downloads/
├── SRR1234567.fastq          # Single-end sample 1
├── SRR1234568.fastq          # Single-end sample 2
└── SRR1234569.fastq          # Single-end sample 3
```

#### Paired-end Data (Split Files)
```
downloads/
├── SRR1234567_1.fastq        # Sample 1, Read 1
├── SRR1234567_2.fastq        # Sample 1, Read 2
├── SRR1234568_1.fastq        # Sample 2, Read 1
├── SRR1234568_2.fastq        # Sample 2, Read 2
├── SRR1234569_1.fastq        # Sample 3, Read 1
└── SRR1234569_2.fastq        # Sample 3, Read 2
```

#### Mixed Data Types
```
downloads/
├── SRR1111111.fastq          # Single-end sample
├── SRR2222222_1.fastq        # Paired-end sample, Read 1
├── SRR2222222_2.fastq        # Paired-end sample, Read 2
├── SRR3333333_1.fastq        # Another paired-end sample
└── SRR3333333_2.fastq
```

### Log File Examples

#### Successful Download Log
```
2024-10-22 14:30:15 - INFO - Starting RNA-seq Downloader v1.0.0
2024-10-22 14:30:16 - INFO - Checking SRA Toolkit installation...
2024-10-22 14:30:17 - INFO - SRA Toolkit found and verified
2024-10-22 14:30:18 - INFO - Fetching SRA accessions for GSE123456...
2024-10-22 14:30:22 - INFO - Found dataset: Example RNA-seq study
2024-10-22 14:30:22 - INFO - Sample count: 6
2024-10-22 14:30:22 - INFO - SRA accessions: 6
2024-10-22 14:30:45 - INFO - Starting download of 6 SRA accessions
2024-10-22 14:31:12 - INFO - ✓ Downloaded: SRR1234567 (125.3 MB, 27s)
2024-10-22 14:31:18 - INFO - ✓ Downloaded: SRR1234568 (98.7 MB, 33s)
2024-10-22 14:31:25 - INFO - ✓ Downloaded: SRR1234569 (156.2 MB, 40s)
2024-10-22 14:31:31 - INFO - ✓ Downloaded: SRR1234570 (142.8 MB, 46s)
2024-10-22 14:31:38 - INFO - ✓ Downloaded: SRR1234571 (134.5 MB, 53s)
2024-10-22 14:31:44 - INFO - ✓ Downloaded: SRR1234572 (167.1 MB, 59s)
2024-10-22 14:31:44 - INFO - All downloads completed successfully
2024-10-22 14:31:44 - INFO - Total time: 1 minute 29 seconds
2024-10-22 14:31:44 - INFO - Total size: 824.6 MB
```

---

These examples should help you understand how to use the RNA-seq Downloader effectively in various scenarios. Remember to always start with small test downloads to verify your setup before downloading large datasets!