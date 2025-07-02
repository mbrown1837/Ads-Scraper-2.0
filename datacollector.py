import logging
from datasaver import DataSaver

class DataCollector:

    def __init__(self, page_parser_obj) -> None:
        self.page_parser = page_parser_obj
        self.collected_data = []

    def paid_ads(self, keyword):
        """To get paid (Ad) results using updated selectors"""
        paid_ads_list = []
        
        # Updated selector for ad containers
        all_paid_ads = self.page_parser.get_element(
            css_selector='div[data-text-ad="1"]', many=True)
        
        if all_paid_ads is not None:
            logging.info(f"Found {len(all_paid_ads)} potential ad containers")
            for paid_ad in all_paid_ads:
                retries = 3
                while retries > 0:
                    try:
                        # Extract ad heading - updated selector
                        ad_heading = self.page_parser.get_element_text(
                            css_selector='div.CCgQ5.vCa9Yd.QfkTvb.N8QANc.Va3FIb.EE3Upf span', parent=paid_ad)
                        
                        # If primary selector fails, try alternative
                        if not ad_heading:
                            ad_heading = self.page_parser.get_element_text(
                                css_selector='div[role="heading"] span', parent=paid_ad)
                        
                        # Extract ad URL - updated selector 
                        ad_url = self.page_parser.get_element_attribute(
                            css_selector='a.sVXRqc', parent=paid_ad, value="href")
                        
                        # Extract meta description - updated selector
                        ad_meta_description = self.page_parser.get_element_text(
                            css_selector='div.Va3FIb.r025kc.lVm3ye div.p4wth', parent=paid_ad)
                        
                        # If primary description selector fails, try alternatives
                        if not ad_meta_description:
                            ad_meta_description = self.page_parser.get_element_text(
                                css_selector='div.p4wth', parent=paid_ad)
                        
                        # Verify this is actually a sponsored ad
                        sponsored_label = self.page_parser.get_element_text(
                            css_selector='span.U3A9Ac.qV8iec', parent=paid_ad)
                        
                        if sponsored_label and "sponsored" in sponsored_label.lower():
                            paid_ads_list.append({
                                "Keyword": keyword,
                                "Type": "Paid Ads",
                                "Heading": ad_heading if ad_heading else "N/A",
                                "Url": ad_url if ad_url else "N/A",
                                "Meta description": ad_meta_description if ad_meta_description else "N/A",
                                "Sponsored Label": sponsored_label if sponsored_label else "N/A"
                            })
                            logging.info(f"Successfully parsed ad: {ad_heading[:50]}...")
                        else:
                            logging.warning(f"Skipping element - no sponsored label found")
                        
                        break  # Exit the retry loop on success
                    except Exception as e:
                        logging.error(f"Error parsing paid ad: {e}")
                        retries -= 1
                        if retries == 0:
                            logging.error(f"Failed to parse paid ad after multiple retries: {e}")
        else:
            logging.warning("No ad containers found with selector: div[data-text-ad='1']")
            
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
