"""WSDL file management for offline operation."""

import os
import logging
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("wsdl-manager")

# Essential WSDL files needed for the onvif library
WSDL_FILES = {
    "analytics.wsdl": "https://www.onvif.org/ver20/analytics/wsdl/analytics.wsdl",
    "devicemgmt.wsdl": "https://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl",
    "media.wsdl": "https://www.onvif.org/ver10/media/wsdl/media.wsdl",
    "ptz.wsdl": "https://www.onvif.org/ver10/ptz/wsdl/ptz.wsdl",
    "events.wsdl": "https://www.onvif.org/ver10/events/wsdl/event.wsdl",
    "imaging.wsdl": "https://www.onvif.org/ver20/imaging/wsdl/imaging.wsdl",
}


def download_file(url, filepath):
    """Download a file from URL to the specified filepath."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)

        logger.info(f"Downloaded: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {str(e)}")
        return False


def ensure_wsdl_files(wsdl_dir):
    """Ensure all required WSDL files are available locally."""
    wsdl_path = Path(wsdl_dir)

    # Create directory if it doesn't exist
    os.makedirs(wsdl_path, exist_ok=True)

    # Download any missing files
    files_downloaded = False
    for filename, url in WSDL_FILES.items():
        filepath = wsdl_path / filename
        if not filepath.exists():
            logger.info(f"Downloading {filename}")
            success = download_file(url, filepath)
            files_downloaded = files_downloaded or success

    if files_downloaded:
        logger.info("Downloaded required files. Now ready for offline operation.")
    else:
        logger.info("All required files are already available locally.")

    return str(wsdl_path)


def clear_wsdl_files(wsdl_dir):
    """Delete all WSDL files to force a fresh download."""
    wsdl_path = Path(wsdl_dir)

    if wsdl_path.exists():
        for file in wsdl_path.glob("*.wsdl"):
            file.unlink()
            logger.info(f"Deleted: {file}")

        logger.info("WSDL files cleared. They will be re-downloaded on next run.")
    else:
        logger.info(f"WSDL directory does not exist: {wsdl_dir}")
