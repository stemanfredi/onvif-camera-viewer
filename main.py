"""Main application for ONVIF camera viewer."""

import os
import argparse
import logging
import sys
from config import CAMERA_CONFIG, WSDL_DIR, LOG_LEVEL
from camera import CameraClient, print_profiles
from wsdl_manager import ensure_wsdl_files, clear_wsdl_files

# Configure logging
level = getattr(logging, LOG_LEVEL)
logging.basicConfig(
    level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("onvif-viewer")


def main():
    """Connect to camera and display profile information."""
    parser = argparse.ArgumentParser(description="ONVIF Camera Profile Viewer")
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Download required WSDL files for offline operation",
    )
    parser.add_argument("--refresh", action="store_true", help="Refresh WSDL files")
    parser.add_argument(
        "--direct-rtsp", action="store_true", help="Use direct RTSP URLs without ONVIF"
    )
    args = parser.parse_args()

    # Handle setup mode
    if args.setup:
        print("Setting up WSDL files for offline operation...")
        ensure_wsdl_files(WSDL_DIR)
        print("Setup complete. You can now run the application offline.")
        sys.exit(0)

    # Handle refresh mode
    if args.refresh:
        print("Refreshing WSDL files...")
        clear_wsdl_files(WSDL_DIR)
        ensure_wsdl_files(WSDL_DIR)
        print("WSDL files have been refreshed.")
        sys.exit(0)

    try:
        # Ensure WSDL directory exists for offline operation
        wsdl_dir = WSDL_DIR if os.path.exists(WSDL_DIR) else None

        # Create camera client
        client = CameraClient(
            CAMERA_CONFIG["ip"],
            CAMERA_CONFIG["port"],
            CAMERA_CONFIG["username"],
            CAMERA_CONFIG["password"],
            wsdl_dir=wsdl_dir,
        )

        # Force direct RTSP mode if requested
        if args.direct_rtsp:
            client.direct_rtsp = True

        # Get and display profiles
        profiles = client.get_profiles()
        print_profiles(profiles)

        # Get and display stream URIs
        for profile in profiles:
            uri = client.get_stream_uri(profile.token)
            print(f"RTSP URL: {uri.Uri}")

        # Show a note if using direct RTSP mode
        if client.direct_rtsp:
            print("\nNote: Using direct RTSP mode (ONVIF services not available)")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        print("\nTips:")
        print("  - Try direct RTSP mode: python main.py --direct-rtsp")
        print("  - If this is your first run, try: python main.py --setup")
        sys.exit(1)


if __name__ == "__main__":
    main()
