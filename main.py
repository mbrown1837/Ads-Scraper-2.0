from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
from time import sleep
from pageparser import Parser
import logging
from datacollector import DataCollector
from variables import DEFAULT_TIMEOUT, SLEEP_TIME, TIMEOUT_FOR_PAGE_LOAD, HEADLESS, PROXIES
from playwright_stealth import stealth_sync
import os

# Define the path to your queries file
QUERIES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'queries.txt')

# Function to read queries from the file
def read_queries(file_path):
    try:
        with open(file_path, 'r') as file:
            queries = [line.strip() for line in file if line.strip()]
        logging.info(f"Successfully read {len(queries)} queries from {file_path}")
        return queries
    except FileNotFoundError:
        logging.error(f"The file {file_path} was not found.")
        return []
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

# Read the queries from the file
SEARCH_QUERIES = read_queries(QUERIES_FILE_PATH)

DEFAULT_TIMEOUT = DEFAULT_TIMEOUT * 1000
TIMEOUT_FOR_PAGE_LOAD = TIMEOUT_FOR_PAGE_LOAD * 1000

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraping.log"),
        logging.StreamHandler()
    ]
)

class GoogleBot:

    base_url_for_search = "https://www.google.com/search?q={query}&cs=1&filter=0"

    def __init__(self, query):
        self.query = query

    def initialzing_objects(self, page):
        """To initialize our data collector and parser objects"""
        self.parser = Parser(page)
        self.data_collector = DataCollector(self.parser)

    def window_scroll_down(self, page):
        """This function is responsible for scrolling down the window"""
        logging.info("Scrolling down the window")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SLEEP_TIME)  # Adding a delay after scrolling

    def check_for_loader(self, page) -> bool:
        """It will check whether chrome is loading the results"""
        loader_element = self.parser.get_element(
            css_selector="[aria-label='Loading...']", parent=page)
        if loader_element is not None and loader_element.is_visible():
            logging.info("Chrome is loading the results")
            return True
        return False

    def scraping_data(self, keyword):
        """It will initialize scraping"""
        self.data_collector.main(keyword)

    def check_for_more_results(self, page):
        """This function will check for 'More results' button. And, if found, it will click on it"""
        more_results_element = self.parser.get_element(
            css_selector="a[aria-label='More results']", parent=page)
        if more_results_element is not None and more_results_element.is_visible():
            more_results_element.click(timeout=30000)
            logging.info("More results button found, and clicked")
            sleep(SLEEP_TIME)  # Adding a delay after clicking
        else:
            logging.warning("More results button could not find")
            if self.check_for_loader(page):
                logging.info("Chrome is loading the results")
                pass
            else:
                logging.info("No further results.")
                return 'break'

    def load_two_pages(self, page):
        """It will load only the first two pages of search results"""
        page_count = 0
        while page_count < 2:
            self.window_scroll_down(page)
            if self.check_for_more_results(page) == 'break':
                logging.warning("Breaking loading loop")
                break
            page_count += 1

    def run(self):
        logging.info(f"Starting the bot for query: {self.query}")

        with sync_playwright() as p:
            if PROXIES is not None:
                browser = p.chromium.launch(headless=HEADLESS, proxy=PROXIES)
            else:
                browser = p.chromium.launch(headless=HEADLESS)

            page = browser.new_page()
            stealth_sync(page)
            page.set_default_timeout(DEFAULT_TIMEOUT)

            self.initialzing_objects(page)

            formatted_url = self.base_url_for_search.format(query=self.query)
            logging.info(f"Opening results page for query: {self.query}")

            page.goto(url=formatted_url, timeout=TIMEOUT_FOR_PAGE_LOAD)
            logging.info("Page is loaded")

            self.load_two_pages(page)
            logging.info("Going to scrape the data")

            self.scraping_data(self.query)

            browser.close()

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(GoogleBot(query).run) for query in SEARCH_QUERIES]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
