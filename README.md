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
git clone <repository-url>
cd ev-blog-automation
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Run the setup script:
```bash
./setup.sh
```

Or manually install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory with the following variables:
```env
# WordPress Configuration
WORDPRESS_URL=your-wordpress-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-application-password

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
SPREADSHEET_ID=your-spreadsheet-id

# LLM Configuration
OLLAMA_URL=http://localhost:11434
MODEL_NAME=gemma3:latest
```

2. Set up Google Sheets API:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Sheets API
   - Create credentials (Service Account)
   - Download the credentials JSON file
   - Rename it to `credentials.json` and place it in the root directory

3. Set up WordPress:
   - Enable REST API
   - Generate an application password for authentication
   - Update the `.env` file with your credentials

## Usage

1. Start the web interface:
```bash
python3 run_web_interface.py
```

2. Access the web interface at `http://localhost:8000` (or the port shown in the console)

3. Enter your Google Sheet ID and WordPress credentials

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
├── .env
├── requirements.txt
├── run_web_interface.py
└── setup.sh
```

## Troubleshooting

1. ChromeDriver Issues:
   - Make sure Chrome browser is installed
   - The script will automatically download the matching ChromeDriver version
   - If issues persist, manually download ChromeDriver matching your Chrome version

2. SSL Certificate Issues:
   - Make sure your system's SSL certificates are up to date
   - For development, you can disable SSL verification (not recommended for production)

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