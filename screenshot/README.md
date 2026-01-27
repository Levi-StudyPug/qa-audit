# URL Screenshot Tool

A Python script to automatically capture screenshots of a list of URLs.

## Features

- 📸 Full-page screenshots
- 🚀 Batch processing of multiple URLs
- 🎨 Customizable viewport size
- 📁 Automatic filename sanitization
- ⚡ Efficient browser reuse
- 🛡️ Error handling for failed captures

## Installation

### Quick Setup (Recommended)

Use the setup script to automatically create a virtual environment and install all dependencies:

**On Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```cmd
setup.bat
```

### Manual Setup

If you prefer to set up manually:

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
   - **Linux/Mac:** `source venv/bin/activate`
   - **Windows:** `venv\Scripts\activate.bat`

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

**Note:** Always activate the virtual environment before running the script!

## Usage

### Before Running

Make sure your virtual environment is activated:
- **Linux/Mac:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate.bat`

### Basic Usage

Edit the `urls` list in the script and run:

```bash
python url_screenshot.py
```

### Customize URLs

Open `url_screenshot.py` and modify the `urls` list in the `main()` function:

```python
urls = [
    'https://www.example.com',
    'https://www.github.com',
    'https://www.wikipedia.org',
    # Add your URLs here
]
```

### Advanced Usage

You can also use it as a module in your own scripts:

```python
import asyncio
from url_screenshot import take_screenshots_batch

urls = ['https://example.com', 'https://github.com']

asyncio.run(take_screenshots_batch(
    urls=urls,
    output_dir="my_screenshots",
    viewport_width=1920,
    viewport_height=1080
))
```

## Options

- `output_dir`: Directory where screenshots will be saved (default: "screenshots")
- `viewport_width`: Browser viewport width in pixels (default: 1920)
- `viewport_height`: Browser viewport height in pixels (default: 1080)

## Output

Screenshots are saved as PNG files in the specified output directory with sanitized filenames based on the URL.

Example: `https://www.example.com/page` → `www_example_com_page.png`

## Troubleshooting

- **Timeout errors**: Some sites take longer to load. The default timeout is 30 seconds.
- **Missing protocol**: URLs without `http://` or `https://` are automatically prefixed with `https://`
- **Browser not found**: Run `playwright install chromium` to install the browser
