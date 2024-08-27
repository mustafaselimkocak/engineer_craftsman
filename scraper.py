import requests
import pandas as pd
from pax_db import PAXDatabase


class Scraper:

    def __init__(self):
        self.api_key = "5bf70f96-11aa-4773-a4dd-f67330b651ee"
        self.api_url = "https://api.dexf.ikea.com/vpc/v1/configurations/retailunit/DE/locale/de-DE/"

    def fetch_ikea_data(self, pax_code: str):
        headers = {
            'Dexf-Api-Key': self.api_key
        }

        url = self.api_url + pax_code

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    def write_data_to_table(self, pax_code, data):

        # Item no and quantity
        items = data.get('itemList', {}).get('item', [])
        item_quantities = [(item['itemNo'], item['quantity']) for item in items]

        df = pd.DataFrame(columns=["Description", "Article No", "Quantity"])

        # Write the results
        for item_no, quantity in item_quantities:
            description = PAXDatabase.get_description_by_article_no(article_no=item_no)
            df.loc[len(df)] = {'Description': description, 'Article No': item_no, 'Quantity': quantity}

        return df
