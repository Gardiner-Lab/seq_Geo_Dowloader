# RNA-seq Downloader Troubleshooting Guide

This guide provides solutions for common issues and detailed troubleshooting steps.

## 🚨 Quick Fixes

### Most Common Issues

1. **Run as Administrator** (Windows) - Fixes most permission issues
2. **Check Internet Connection** - Required for downloads and API calls
3. **Free Up Disk Space** - Each SRA file needs ~100-500MB
4. **Use Default Settings** - Press Enter to use recommended defaults
5. **Try Fewer Threads** - Reduce to 2-4 if experiencing connection issues

## 🔧 Detailed Troubleshooting

### GSE Number Issues

**Problem**: "GSE number not found" or "Invalid GSE format"

**Solutions**:
1. **Verify GSE exists**:
   - Visit https://www.ncbi.nlm.nih.gov/geo/
   - Search for your GSE number
   - Ensure it has associated SRA data

2. **Check GSE format**:
   ```
   ✓ Correct: GSE123456, GSE98765, GSE1
   ✗ Wrong: gse123456, GSE, 123456, GSE-123
   ```

3. **Alternative approaches**:
   - Use SRA accession list file instead
   - Find SRA accessions manually at https://www.ncbi.nlm.nih.gov/sra/
   - Check if dataset is publicly available

**Example fix**:
```bash
# Instead of GSE input, create sra_list.txt:
SRR1234567
SRR1234568
SRR1234569

# Then use file input method
```

### SRA Toolkit Installation Issues

**Problem**: "SRA Toolkit installation failed" or "fasterq-dump not found"

**Automatic fix attempts**:
1. **Run with elevated privileges**:
   ```bash
   # Windows: Right-click Command Prompt -> "Run as administrator"
   python seq_downloader.py
   
   # Linux/macOS: Use sudo if needed
   sudo python seq_downloader.py
   ```

2. **Check firewall/antivirus**:
   - Temporarily disable antivirus (Windows)
   - Allow Python through firewall
   - Check corporate firewall settings

**Manual installation**:
1. **Download SRA Toolkit**:
   - Go to: https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit
   - Choose your platform:
     - Windows: "Windows 64-bit" (.zip file)
     - Linux: "Ubuntu Linux 64-bit" (.tar.gz file)
     - macOS: "Mac OS X 64-bit" (.tar.gz file)
   - Extract to: `[project_folder]/tools/sratoolkit/`

2. **Verify installation**:
   ```bash
   # Windows
   tools\sratoolkit\bin\fasterq-dump.exe --help
   
   # Linux/macOS
   tools/sratoolkit/bin/fasterq-dump --help
   ```

3. **Expected directory structure**:
   ```
   tools/
   └── sratoolkit/
       └── bin/
           ├── fasterq-dump      # Linux/macOS
           ├── fasterq-dump.exe  # Windows
           ├── prefetch
           └── [other tools]
   ```

4. **Set executable permissions (Linux/macOS only)**:
   ```bash
   chmod +x tools/sratoolkit/bin/*
   ```

### Permission and Directory Issues

**Problem**: "Permission denied" or "Cannot create directory"

**Solutions**:
1. **Choose different output directory**:
   ```
   # Instead of C:\Program Files\... use:
   C:\Users\YourName\Documents\RNA_data
   ./my_downloads
   D:\RNA_Projects
   ```

2. **Check directory permissions**:
   - Right-click folder → Properties → Security
   - Ensure your user has "Full control"
   - Create directory manually first if needed

3. **Run with elevated privileges**:
   - **Windows**: Right-click Command Prompt → "Run as administrator"
   - **Linux/macOS**: Use `sudo` if needed for directory permissions
   - Navigate to project directory and run the tool

### Network and Download Issues

**Problem**: "Network error", "Connection timeout", or "Download failed"

**Immediate fixes**:
1. **Reduce thread count**:
   ```
   Enter number of threads (1-16, default: 6): 2
   ```

2. **Check internet stability**:
   - Test with: `ping google.com`
   - Use wired connection instead of WiFi
   - Close other network-intensive applications

3. **Retry mechanism**:
   - Tool automatically retries failed downloads
   - Wait for all retries to complete
   - Check final summary for success/failure counts

**Advanced network troubleshooting**:
1. **Corporate networks**:
   - Check proxy settings
   - Contact IT about NCBI access
   - Try from personal network

2. **Firewall issues**:
   - Allow Python through Windows Firewall
   - Check antivirus network protection
   - Temporarily disable VPN

3. **NCBI server issues**:
   - Try again later (servers may be busy)
   - Check NCBI status at https://www.ncbi.nlm.nih.gov/
   - Use SRA list file instead of GSE lookup

### File and Storage Issues

**Problem**: "Insufficient disk space" or "File already exists"

**Disk space solutions**:
1. **Check available space**:
   ```bash
   # Windows
   dir C:\ 
   
   # Linux/macOS
   df -h
   
   # Estimate needed space: ~100-500MB per SRA file
   # For 10 files: ~1-5GB needed
   ```

2. **Free up space**:
   - Delete temporary files
   - Empty recycle bin
   - Move large files to external storage
   - Use disk cleanup utility

3. **Choose different location**:
   - Use external drive: `E:\RNA_data`
   - Use network drive (if fast enough)
   - Use different partition with more space

**File conflict solutions**:
1. **Existing file options**:
   ```
   File already exists: SRR1234567.fastq
   1. Skip (recommended if file is complete)
   2. Overwrite (re-download)
   3. Rename (keep both versions)
   ```

2. **Check file integrity**:
   - Tool automatically checks file size
   - Files < 1KB are considered incomplete
   - Choose "Overwrite" for incomplete files

### Performance Issues

**Problem**: Slow downloads or system unresponsiveness

**Performance optimization**:
1. **Adjust thread count**:
   ```
   Slow internet: 1-2 threads
   Average internet: 4-6 threads  
   Fast internet: 8-12 threads
   Very fast internet: 12-16 threads
   ```

2. **System resources**:
   - Close other applications
   - Monitor CPU and memory usage
   - Use Task Manager to check resource usage

3. **Storage optimization**:
   - Use SSD instead of HDD for output directory
   - Ensure output drive isn't nearly full
   - Avoid network drives for output

### Input File Issues

**Problem**: "Invalid SRA accession" or "Cannot read file"

**File format fixes**:
1. **Check accession format**:
   ```
   ✓ Correct: SRR1234567, ERR1234567, DRR1234567
   ✗ Wrong: srr1234567, SRA1234567, RR1234567
   ```

2. **File encoding**:
   - Save file as UTF-8 encoding
   - Avoid special characters
   - Use plain text editor (Notepad, not Word)

3. **File content example**:
   ```
   # This is a comment
   SRR1234567
   SRR1234568
   
   # Empty lines are OK
   SRR1234569
   ```

4. **CSV/TSV files**:
   ```csv
   accession,sample_name
   SRR1234567,Sample1
   SRR1234568,Sample2
   ```

## 🔍 Diagnostic Commands

### System Information
```bash
# Check Python version
python --version

# Check tool version
python seq_downloader.py --version

# Show system info
python -c "import sys; print(f'Python: {sys.version}'); print(f'Platform: {sys.platform}')"
```

### Test Installation
```bash
# Test with help command
python seq_downloader.py --help

# Test SRA Toolkit (after installation)
tools\sratoolkit\bin\fasterq-dump.exe --help
```

### Network Testing
```bash
# Test internet connection (all platforms)
ping google.com

# Test NCBI connection
ping eutils.ncbi.nlm.nih.gov

# Check network interface (Linux/macOS)
ifconfig

# Check network interface (Windows)
ipconfig

# Test download speed
# Use online speed test or download a small file
```

## 📋 Error Code Reference

### Exit Codes
- `0` - Success
- `1` - General error
- `130` - User cancelled (Ctrl+C)

### Common Error Messages

**"InputValidationError"**
- Cause: Invalid user input
- Fix: Check input format, use help prompts

**"GEOServiceError"**
- Cause: NCBI API issues
- Fix: Check internet, verify GSE number, try again later

**"PermissionError"**
- Cause: File/directory access denied
- Fix: Run as administrator, choose different directory

**"OSError: [Errno 28] No space left on device"**
- Cause: Insufficient disk space
- Fix: Free up space, choose different output directory

**"ConnectionError" or "TimeoutError"**
- Cause: Network issues
- Fix: Check internet, reduce threads, try again

## 🛠️ Advanced Troubleshooting

### Log Analysis

**Log file locations**:
```
logs/
├── seq_downloader.log              # Main log
├── 20241022_084254_seq_downloader.log  # Timestamped logs
└── [other session logs]
```

**Key log sections to check**:
1. **Startup errors**: Check first few lines
2. **API calls**: Look for "GEO service" entries
3. **Download errors**: Search for "ERROR" or "FAILED"
4. **Network issues**: Look for "timeout" or "connection"

### Manual Testing

**Test individual components**:
1. **Test GSE lookup**:
   ```python
   # Create test script
   from src.geo_service import GEOService
   geo = GEOService()
   result = geo.validate_gse_number("GSE123456")
   print(result)
   ```

2. **Test SRA Toolkit**:
   ```bash
   # Test fasterq-dump directly
   tools\sratoolkit\bin\fasterq-dump.exe --help
   ```

3. **Test file operations**:
   ```python
   # Test directory creation
   import os
   os.makedirs("test_output", exist_ok=True)
   print("Directory creation successful")
   ```

### Environment Issues

**Python environment problems**:
1. **Multiple Python versions**:
   ```bash
   # Check which Python is being used
   where python
   python --version
   ```

2. **Missing dependencies**:
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Virtual environment issues**:
   ```bash
   # Create fresh environment
   python -m venv fresh_env
   fresh_env\Scripts\activate
   pip install -r requirements.txt
   ```

## 📞 Getting Additional Help

### Before Seeking Help

1. **Try the quick fixes** listed at the top
2. **Check log files** for detailed error information
3. **Test with minimal example** (1-2 SRA accessions)
4. **Verify system requirements** (Python 3.7+, Windows, internet)

### Information to Provide

When reporting issues, include:
- **Error message** (exact text)
- **Log file contents** (from logs/ directory)
- **System information** (Python version, Windows version)
- **Steps to reproduce** the issue
- **Input data** (GSE number or sample SRA list)

### Self-Help Resources

1. **Built-in help**:
   ```bash
   python seq_downloader.py --help
   python seq_downloader.py --examples
   python seq_downloader.py --troubleshoot
   ```

2. **Online resources**:
   - NCBI SRA: https://www.ncbi.nlm.nih.gov/sra/
   - SRA Toolkit: https://github.com/ncbi/sra-tools
   - GEO Database: https://www.ncbi.nlm.nih.gov/geo/

3. **Test datasets**:
   - Small GSE: GSE1 (for testing GSE functionality)
   - Test SRA: SRR000001 (for testing file input)

---

**Remember**: Most issues can be resolved by running as administrator, checking internet connection, and using default settings. When in doubt, try the simplest approach first!