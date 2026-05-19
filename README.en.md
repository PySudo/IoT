# IoT Project - English Documentation

## 📖 Overview

This is an IoT (Internet of Things) project that provides a comprehensive solution for managing smart devices with microcontroller support, REST API backend, and pin control functionality.

## 🏗️ Project Structure

```
IoT-main/
├── README.md           # Main documentation (language selector)
├── README.en.md        # English documentation
├── README.fa.md        # Persian documentation
├── setup.py            # Package setup configuration
│
├── example/            # Example implementations
│   └── core/
│       ├── buttons.py      # Button UI generation
│       ├── config.py       # Configuration
│       ├── database.py     # Database operations
│       └── functions.py    # Utility functions
│
├── main_api/           # REST API Server
│   └── core/
│       ├── config.py       # API configuration
│       ├── database.py     # Database models
│       └── functions.py    # API business logic
│
└── MicroController/    # Microcontroller firmware
    ├── main.py         # Main entry point
    └── functions.py    # Device functions
```

## ✨ Key Features

- **Microcontroller Support**: Connect and manage ESP8266/ESP32 or similar devices
- **REST API**: Full-featured API for device management
- **Pin Control**: Remote GPIO pin management
- **User Management**: Admin user system for security
- **Database Integration**: Data persistence for device states

## 🚀 Quick Start

### Installation

```bash
# Install the package
pip install -e .
```

### Configuration

1. **Microcontroller Setup** (`MicroController/main.py`):
```python
SSID = 'your-wifi-ssid'
Password = 'your-wifi-password'
API_URL = 'http://your-api-server'
API_KEY = 'your-api-key'
```

2. **API Server Setup**:
- Update configuration in `main_api/core/config.py`
- Set up database credentials

### Running the Project

**Start the API Server**:
```bash
python -m main_api
```

**Deploy to Microcontroller**:
- Upload `MicroController/main.py` and `functions.py` to your device using MicroPython

## 📚 Components

### 1. MicroController
- Connects to WiFi network
- Fetches pin configurations from API
- Manages GPIO pins in real-time
- Sends status updates back to server

### 2. Main API
- RESTful API endpoints for device management
- Admin authentication
- Pin configuration management
- Database backend for persistence

### 3. Example Module
- Sample button generation system
- Menu structure examples
- Administrative controls

## 🔧 Configuration

Key configuration parameters:

| Parameter | Location | Purpose |
|-----------|----------|---------|
| SSID | MicroController/main.py | WiFi network name |
| API_URL | MicroController/main.py | API server address |
| API_KEY | MicroController/main.py | Authentication key |

## 📱 API Endpoints

Common endpoints for device management:
- Pin configuration management
- Admin user management
- Device status queries
- Real-time pin control

## 🔐 Security

- API key-based authentication
- Admin role system
- Secure WiFi connection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

[← Back to Main README](README.md) | [Read in Persian](README.fa.md)
