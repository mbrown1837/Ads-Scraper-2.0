import logging
from datasaver import DataSaver

class DataCollector:

    def __init__(self, page_parser_obj) -> None:
        self.page_parser = page_parser_obj
        self.collected_data = []

    def paid_ads(self, keyword):
        """To get paid (Ad) results"""
        paid_ads_list = []
        all_paid_ads = self.page_parser.get_element(
            css_selector='[class="uEierd"]', many=True)
        if all_paid_ads is not None:
            for paid_ad in all_paid_ads:
                retries = 3
                while retries > 0:
                    try:
                        ad_heading = self.page_parser.get_element_text(
                            css_selector='[class="sVXRqc"] div[role="heading"]', parent=paid_ad)
                        ad_url = self.page_parser.get_element_attribute(
                            css_selector='[class="sVXRqc"]', parent=paid_ad, value="href")
                        ad_meta_description = self.page_parser.get_element_text(
                            css_selector='[class="MUxGbd yDYNvb lyLwlc"]', parent=paid_ad)

                        paid_ads_list.append({
                            "Keyword": keyword,
                            "Type": "Paid Ads",
                            "Heading": ad_heading if ad_heading else "N/A",
                            "Url": ad_url if ad_url else "N/A",
                            "Meta description": ad_meta_description if ad_meta_description else "N/A"
                        })
                        break  # Exit the retry loop on success
                    except Exception as e:
                        logging.error(f"Error parsing paid ad: {e}")
                        retries -= 1
                        if retries == 0:
                            logging.error(f"Failed to parse paid ad after multiple retries: {e}")
        return paid_ads_list

    def main(self, keyword):
        logging.info(f"Collecting data for keyword: {keyword}")

        paid_ads_data = self.paid_ads(keyword)
        if not paid_ads_data:
            logging.warning("No paid ads found, retrying...")
            paid_ads_data = self.paid_ads(keyword)
        self.collected_data.extend(paid_ads_data)
        logging.info("Paid ads have been scraped")

        DataSaver.save_data(data=self.collected_data)

    def get_collected_data(self):
        """Returns the collected data as a string"""
        return str(self.collected_data)
