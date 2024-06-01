# Google Ads Scraper

This project is a web scraper that collects Google Ads data for specified search queries. It uses Playwright to navigate Google search results and extract relevant ad information. The scraper is designed to run concurrently for multiple queries, making the data collection process efficient.

## Features

- Scrapes Google Ads data for specified search queries.
- Uses Playwright for browser automation.
- Handles pagination (up to the first two pages).
- Implements error handling and retries.
- Saves collected data to a JSON file.
- Detailed logging for monitoring the scraping process.

## Prerequisites

- Python 3.7 or higher
- Node.js (required for Playwright)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/mbrown1837/Ads-Scraper-2.0.git
   cd Ads-Scraper-2.0

Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:
pip install -r requirements.txt
Install Playwright and its dependencies:
playwright install

Configuration

Add your search queries to the queries.txt file:
Create a file named queries.txt in the root directory and add your search queries, one per line:
keyword1
keyword2
keyword3
Adjust variables and settings in variables.py:
DEFAULT_TIMEOUT = 30  # Default timeout for page load in seconds
SLEEP_TIME = 2  # Time to sleep between actions in seconds
TIMEOUT_FOR_PAGE_LOAD = 60  # Page load timeout in seconds
HEADLESS = True  # Run browsers in headless mode
PROXIES = None  # Add proxy settings if needed

Running the Scraper

Activate the virtual environment:
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Run the scraper:
python main.py

File Structure

main.py: Main script to run the scraper.
datacollector.py: Contains the DataCollector class for collecting ads data.
pageparser.py: Contains the Parser class for extracting elements from the page.
datasaver.py: Contains the DataSaver class for saving data to a JSON file.
variables.py: Configuration variables.
queries.txt: File containing search queries.
requirements.txt: List of required Python packages.

Dependencies

playwright: Browser automation library.
playwright-stealth: Stealth plugin for Playwright.
concurrent.futures: For running multiple instances concurrently.
logging: For logging the scraping process.
