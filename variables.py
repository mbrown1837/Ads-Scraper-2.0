import os

# Define the path to your queries file
QUERIES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'queries.txt')

# Function to read queries from the file
def read_queries(file_path):
    with open(file_path, 'r') as file:
        queries = [line.strip() for line in file if line.strip()]
    return queries

# Read the queries from the file
SEARCH_QUERIES = read_queries(QUERIES_FILE_PATH)

# Print the queries to verify
for query in SEARCH_QUERIES:
    print(query)

# Example usage of the queries
for query in SEARCH_QUERIES:
    print(f"Performing search for: {query}")
    # Add your search logic here

# Other configuration variables
DEFAULT_TIMEOUT = 30  # Default timeout for page load in seconds
SLEEP_TIME = 2  # Time to sleep between actions in seconds
TIMEOUT_FOR_PAGE_LOAD = 60  # Page load timeout in seconds
HEADLESS = True  # Run browsers in headless mode
PROXIES = None  # Add proxy settings if needed

# Example function to demonstrate usage of configuration variables
def perform_search(query):
    print(f"Searching for: {query}")
    print(f"Timeout for page load: {TIMEOUT_FOR_PAGE_LOAD} seconds")
    print(f"Default timeout: {DEFAULT_TIMEOUT} seconds")
    print(f"Sleep time: {SLEEP_TIME} seconds")
    print(f"Headless mode: {HEADLESS}")
    print(f"Proxies: {PROXIES}")
    # Add your search implementation here

# Perform search for each query
for query in SEARCH_QUERIES:
    perform_search(query)
