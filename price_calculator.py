from pax_db import PAXDatabase


class PriceCalculator:

    @staticmethod
    def calculate_prices(results):
        total_price = 0

        for index, row in results.iterrows():
            article_no = row['Article No']
            quantity = row['Quantity']
            article_price = PAXDatabase.get_price_by_article_no(article_no)
            article_price = article_price * quantity
            total_price = total_price + article_price

        print(f"Total price: {total_price}")
        return total_price
