# EV Blog Automation Suite

An automated blog publishing system designed for EV-related content. This system automatically generates, formats, and publishes blog posts with images to WordPress, using data from Google Sheets.

## Features

- Automated blog post generation using LLM (Gemma)
- Google Sheets integration for content management
- Automatic image search and download
- WordPress integration for automated publishing
- Web interface for easy management
- AdSense integration
- Automatic image placement and formatting

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Google Sheets API credentials
- WordPress site with REST API access
- Ollama installed for LLM integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/harshafau/Full-Blog-Automation.git
cd Full-Blog-Automation
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Install all required Python packages
- Set up ChromeDriver
- Configure SSL certificates
- Create necessary directories

## Configuration

1. Set up Google Sheets API:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Sheets API
   - Create credentials (Service Account)
   - Download the credentials JSON file
   - Rename it to `credentials.json` and place it in the root directory

2. Set up WordPress:
   - Enable REST API
   - Generate an application password for authentication

## Usage

1. Start the web interface:
```bash
python3 run_web_interface.py
```

2. Access the web interface at `http://localhost:8000` (or the port shown in the console)

3. Enter your credentials in the web interface:
   - Google Sheet ID
   - WordPress URL
   - WordPress Username
   - WordPress Application Password
   - Number of Images per post (default: 3)
   - Article Length in words (default: 1000)

4. Click "Generate" to start the blog automation process

## Google Sheets Format

Your Google Sheet should have the following columns:
- Topic name
- Title
- Keywords
- Must have elements
- Context
- Status

## Directory Structure

```
.
├── config/
│   └── config.py
├── modules/
│   ├── content_processor.py
│   ├── google_sheets.py
│   ├── image_handler.py
│   ├── llm_integration.py
│   └── wordpress_integration.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── logs/
├── temp/
│   └── images/
├── credentials.json
├── requirements.txt
├── run_web_interface.py
└── setup.sh
```

## Troubleshooting

1. ChromeDriver Issues:
   - Make sure Chrome browser is installed
   - The setup script will automatically download the matching ChromeDriver version
   - If issues persist, manually download ChromeDriver matching your Chrome version

2. SSL Certificate Issues:
   - The setup script will automatically install SSL certificates
   - If issues persist, run: `/Applications/Python\ 3.*/Install\ Certificates.command`

3. WordPress Connection Issues:
   - Verify your WordPress site has REST API enabled
   - Check if your application password is correct
   - Ensure your WordPress URL is correct and includes http:// or https://

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.