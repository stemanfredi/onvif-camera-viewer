"""ONVIF camera client using the ONVIFCamera library directly."""

import os
import logging
from pathlib import Path
from onvif import ONVIFCamera

# Configure logging
logger = logging.getLogger("onvif-camera")


class CameraClient:
    """Simple ONVIF camera client with fallback for direct RTSP."""

    def __init__(self, ip, port, username, password, wsdl_dir=None):
        """Initialize ONVIF camera connection.

        Args:
            ip: Camera IP address
            port: Camera port
            username: Login username
            password: Login password
            wsdl_dir: Optional directory with WSDL files for offline operation
        """
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.direct_rtsp = False

        try:
            logger.info(f"Connecting to camera at {ip}:{port}")

            # Create camera instance with wsdl_dir if specified
            if wsdl_dir and os.path.exists(wsdl_dir):
                self.cam = ONVIFCamera(ip, port, username, password, wsdl_dir=wsdl_dir)
            else:
                self.cam = ONVIFCamera(ip, port, username, password)

            # Get media service
            self.media_service = self.cam.create_media_service()
            logger.info("Successfully connected to camera")

        except Exception as e:
            logger.error(f"Failed to connect to camera: {str(e)}")
            self.direct_rtsp = True
            logger.info("Switching to direct RTSP mode")

    def get_profiles(self):
        """Get camera profiles.

        Returns:
            List of camera profiles or simulated profiles if in direct RTSP mode
        """
        if self.direct_rtsp:
            # Return simulated profiles when in direct RTSP mode
            return [
                type(
                    "Profile",
                    (),
                    {
                        "Name": "Main Stream",
                        "token": "Profile_1",
                        "VideoSourceConfiguration": type(
                            "VSC", (), {"SourceToken": "channel1"}
                        ),
                        "VideoEncoderConfiguration": type(
                            "VEC",
                            (),
                            {
                                "Encoding": "H264",
                                "Resolution": type(
                                    "Res", (), {"Width": 1920, "Height": 1080}
                                ),
                            },
                        ),
                    },
                ),
                type(
                    "Profile",
                    (),
                    {
                        "Name": "Sub Stream",
                        "token": "Profile_2",
                        "VideoSourceConfiguration": type(
                            "VSC", (), {"SourceToken": "channel1"}
                        ),
                        "VideoEncoderConfiguration": type(
                            "VEC",
                            (),
                            {
                                "Encoding": "H264",
                                "Resolution": type(
                                    "Res", (), {"Width": 640, "Height": 480}
                                ),
                            },
                        ),
                    },
                ),
            ]

        try:
            logger.info("Getting camera profiles")
            return self.media_service.GetProfiles()
        except Exception as e:
            logger.error(f"Error getting profiles: {str(e)}")
            # Switch to direct RTSP mode and return simulated profiles
            self.direct_rtsp = True
            return self.get_profiles()

    def get_stream_uri(self, profile_token):
        """Get stream URI for a profile.

        Args:
            profile_token: Profile token identifier

        Returns:
            Stream URI object
        """
        if self.direct_rtsp:
            # Use the known working RTSP pattern for your camera
            subtype = "0" if profile_token == "Profile_1" else "1"
            rtsp_url = f"rtsp://{self.username}:{self.password}@{self.ip}:554/cam/realmonitor?channel=1&subtype={subtype}&unicast=true&proto=Onvif"
            return type("StreamUri", (), {"Uri": rtsp_url})

        try:
            logger.info(f"Getting stream URI for profile {profile_token}")
            return self.media_service.GetStreamUri(
                {
                    "StreamSetup": {
                        "Stream": "RTP-Unicast",
                        "Transport": {"Protocol": "RTSP"},
                    },
                    "ProfileToken": profile_token,
                }
            )
        except Exception as e:
            logger.error(f"Error getting stream URI: {str(e)}")
            # Switch to direct RTSP and try again
            self.direct_rtsp = True
            return self.get_stream_uri(profile_token)


def print_profiles(profiles):
    """Print formatted profile information.

    Args:
        profiles: List of camera profiles
    """
    for profile in profiles:
        print(f"\nProfile Name: {profile.Name}")
        print(f"Profile Token: {profile.token}")

        if hasattr(profile, "VideoSourceConfiguration"):
            print(f"Video Source: {profile.VideoSourceConfiguration.SourceToken}")

        if hasattr(profile, "VideoEncoderConfiguration"):
            encoder = profile.VideoEncoderConfiguration
            print(f"Encoding: {encoder.Encoding}")
            if hasattr(encoder, "Resolution"):
                print(
                    f"Resolution: {encoder.Resolution.Width}x{encoder.Resolution.Height}"
                )
