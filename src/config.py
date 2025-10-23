"""Configuration constants for the seq_downloader application."""

APP_NAME = "seq_downloader"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "A tool for downloading sequencing data from SRA and GSE numbers"

# Default configuration values
DEFAULT_OUTPUT_DIR = "downloads"
DEFAULT_LOG_DIR = "logs"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 5
DEFAULT_TIMEOUT = 300

# SRA toolkit configuration
SRATOOLKIT_PATH = "tools/sratoolkit"
PREFETCH_EXECUTABLE = "prefetch"
FASTERQ_DUMP_EXECUTABLE = "fasterq-dump"

# NCBI API configuration
NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NCBI_ESEARCH_URL = f"{NCBI_BASE_URL}/esearch.fcgi"
NCBI_ELINK_URL = f"{NCBI_BASE_URL}/elink.fcgi"
NCBI_REQUEST_DELAY = 0.34  # NCBI recommends no more than 3 requests per second