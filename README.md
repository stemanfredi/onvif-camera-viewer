# ONVIF Camera Viewer

A clean, modular Python client for accessing ONVIF camera profiles and RTSP streams with offline operation capability.

## Features

- Connect to ONVIF-compatible IP cameras
- Retrieve camera profiles and capabilities
- Display video source configuration details
- Generate RTSP streaming URLs
- Works offline after initial setup
- Clean error handling

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/onvif-camera-viewer.git
cd onvif-camera-viewer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

## Initial Setup

On first use, run the setup command to download required WSDL and XSD files:

```bash
python main.py --setup
```

This downloads all necessary files for offline operation.

## Usage

```bash
# Normal operation (works offline after setup)
python main.py

# Refresh WSDL files (requires internet connection)
python main.py --refresh
```

## Configuration

1. Copy the example configuration file to create your own configuration:

   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` with your camera's details:

   ```python
   CAMERA_CONFIG = {
       'ip': '192.168.1.60',        # Your camera's IP address
       'port': 80,                  # HTTP port (usually 80)
       'username': 'admin',         # Camera username
       'password': 'your-password'  # Camera password
   }
   ```

## Example Output

```
Device Information:
Manufacturer: ACME
Model: IP Camera
Firmware Version: 1.2.3
Serial Number: ABC123456

Profile Name: Profile_1
Profile Token: Profile_1
Video Source: VideoSourceToken_1
Encoding: H264
Resolution: 1920x1080
Bitrate: 4096 kbps
Framerate: 30 fps
RTSP URL: rtsp://192.168.1.60:554/profile1
```

## How It Works

1. The application downloads WSDL and XSD files on first run
2. These files are stored locally in the `wsdl` directory
3. Subsequent runs use the local files, enabling offline operation
4. The refresh option allows updating the files when needed

## Troubleshooting

1. **First Run**: If you get errors on first run, try `python main.py --setup`
2. **Connection Issues**: Verify camera IP address and credentials in `config.py`
3. **WSDL/XSD Issues**: If you see schema errors, try `python main.py --refresh`

## License

MIT
