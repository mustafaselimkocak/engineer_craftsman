import pandas as pd

pax_df = pd.read_csv("docs/PAXCostAnalysis.csv", dtype={'Description': str, 'Size': str, 'Code': str, 'Price': float})

mapped_pairs = pd.read_csv("docs/mapped_pairs.csv", dtype={'id': str, 'replacedBy': str})


class PAXDatabase:

    @staticmethod
    def get_description_by_article_no(article_no: str):

        if "." in article_no:
            article_no = article_no.replace(".", "")

        if article_no in pax_df['Code'].values:
            description = pax_df.loc[pax_df['Code'] == article_no, 'Description'].values[0]
            return description
        else:

            # Try finding article no in mapped_pairs DataFrame
            if article_no in mapped_pairs['id'].values:
                replaced_by_id = mapped_pairs.loc[mapped_pairs['id'] == article_no, 'replacedBy'].values[0]
                if replaced_by_id in pax_df['Code'].values:
                    description = pax_df.loc[pax_df['Code'] == replaced_by_id, 'Description'].values[0]
                    return description

            # If the article number is still not found
            PAXDatabase.add_article_no_to_not_found(article_no)
            return f"Article {article_no} not found."

    @staticmethod
    def get_price_by_article_no(article_no: str):

        if "." in article_no:
            article_no = article_no.replace(".", "")

        if article_no in pax_df['Code'].values:
            price = pax_df.loc[pax_df['Code'] == article_no, 'Price'].values[0]
            return price
        else:

            # Try finding article no in mapped_pairs DataFrame
            if article_no in mapped_pairs['id'].values:
                replaced_by_id = mapped_pairs.loc[mapped_pairs['id'] == article_no, 'replacedBy'].values[0]
                if replaced_by_id in pax_df['Code'].values:
                    price = pax_df.loc[pax_df['Code'] == replaced_by_id, 'Price'].values[0]
                    return price

            # If the article number is still not found
            PAXDatabase.add_article_no_to_not_found(article_no)
            return 0.0

    @staticmethod
    def add_article_no_to_not_found(article_no):
        with open('docs/not_found_articles.txt', 'a+') as file:
            file.seek(0)
            content = file.read()
            if article_no not in content:
                file.write(article_no + '\n')
            file.close()
