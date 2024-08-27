import pandas as pd

file_path = "PAXCostAnalysis.csv"
df = pd.read_csv(file_path, dtype={'Description': str, 'Size': str, 'Code': str, 'Price': float})


class PAXDatabase:

    @staticmethod
    def get_description_by_article_no(article_no: str):

        if "." in article_no:
            article_no = article_no.replace(".", "")

        if article_no in df['Code'].values:
            description = df.loc[df['Code'] == article_no, 'Description'].values[0]
            return description
        else:
            PAXDatabase.add_article_no_to_not_found(article_no)
            return f"Article {article_no} not found."

    @staticmethod
    def get_price_by_article_no(article_no: str):

        if "." in article_no:
            article_no = article_no.replace(".", "")

        if article_no in df['Code'].values:
            price = df.loc[df['Code'] == article_no, 'Price'].values[0]
            return price
        else:
            PAXDatabase.add_article_no_to_not_found(article_no)
            return 0.0

    @staticmethod
    def add_article_no_to_not_found(article_no):
        with open('not_found_articles.txt', 'a+') as file:
            file.seek(0)
            content = file.read()
            if article_no not in content:
                file.write(article_no + '\n')
            file.close()
