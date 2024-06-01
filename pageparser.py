import logging
from playwright.sync_api import TimeoutError

class Parser:

    def __init__(self, page) -> None:
        self.page = page

    def get_element(self, css_selector, parent=None, many=False):
        try:
            if parent:
                result = parent.locator(css_selector)
                if result.count() > 0:
                    return result.all() if many else result.first
                return None
            else:
                result = self.page.locator(css_selector)
                if result.count() > 0:
                    return result.all() if many else result.first
                return None
        except TimeoutError:
            logging.error(f"TimeoutError: Element with selector '{css_selector}' not found.")
            return None

    def get_element_text(self, css_selector, parent=None):
        try:
            element = self.get_element(css_selector=css_selector, parent=parent)
            return element.text_content() if element is not None else None
        except TimeoutError:
            logging.error(f"TimeoutError: Text content for element with selector '{css_selector}' not found.")
            return None

    def get_text_of_locator(self, locator):
        try:
            return locator.text_content()
        except TimeoutError:
            logging.error("TimeoutError: Text content for locator not found.")
            return None

    def get_element_attribute(self, css_selector, value, parent=None):
        try:
            element = self.get_element(css_selector=css_selector, parent=parent)
            return element.get_attribute(value) if element is not None else None
        except TimeoutError:
            logging.error(f"TimeoutError: Attribute '{value}' for element with selector '{css_selector}' not found.")
            return None

    def get_hidden_element_text(self, css_selector, parent=None):
        js_code_with_parent = f''' (parent) => {{
                const child = parent.querySelector('{css_selector}');
                return child.textContent;}}'''

        js_code_with_page = f'''
                const child = document.querySelector('{css_selector}');
                return child.textContent;
                '''
        try:
            if parent:
                return str(parent.evaluate_handle(js_code_with_parent))
            else:
                return str(self.page.evaluate(js_code_with_page))
        except Exception as e:
            logging.error(f"Error: {e}")
            return None
