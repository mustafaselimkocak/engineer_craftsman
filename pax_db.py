import math

import pandas as pd

PAX_CSV_PATH = "docs/PAXCostAnalysis.csv"


def _read_items():
    return pd.read_csv(
        PAX_CSV_PATH,
        dtype={"Category": str, "Description": str, "Size": str, "Code": str, "Price": float},
    )


pax_df = _read_items()

mapped_pairs = pd.read_csv("docs/mapped_pairs.csv", dtype={'id': str, 'replacedBy': str})

category_list = pax_df["Category"].dropna().unique().tolist()

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

    @staticmethod
    def add_new_item(category, description, code, price):

        """Add a new item without modifying any existing item."""
        global pax_df, category_list

        pax_df = _read_items()
        category_list = pax_df["Category"].dropna().unique().tolist()

        code = "" if pd.isna(code) else str(code).strip().replace(".", "")
        if not code:
            return "Code is required."
        if (pax_df["Code"] == code).any():
            return f"Article {code} already exists. No item was added."

        item_values = {}
        for column, value in (("Category", category), ("Description", description), ("Price", price)):
            if pd.isna(value) or (isinstance(value, str) and not value.strip()):
                continue
            if column == "Price":
                try:
                    value = float(value)
                except (TypeError, ValueError) as error:
                    raise ValueError("Price must be a valid number.") from error
                if not math.isfinite(value) or value < 0:
                    raise ValueError("Price must be a finite, non-negative number.")
            item_values[column] = value

        updated_df = pax_df.copy()
        matching_categories = updated_df["Category"].eq(item_values.get("Category")).fillna(False)
        matching_positions = [
            position for position, matches in enumerate(matching_categories) if matches
        ]
        insert_position = matching_positions[-1] + 1 if matching_positions else len(updated_df)
        new_item = pd.DataFrame([{"Code": code, **item_values}], columns=updated_df.columns)
        updated_df = new_item if updated_df.empty else pd.concat(
            [updated_df.iloc[:insert_position], new_item, updated_df.iloc[insert_position:]],
            ignore_index=True,
        )

        updated_df.to_csv(PAX_CSV_PATH, index=False)
        pax_df = updated_df
        category_list = pax_df["Category"].dropna().unique().tolist()
        return "Success"

    @staticmethod
    def get_category_price(category):
        """Read the first available price for a category from the current CSV."""
        items = _read_items()
        prices = items.loc[items["Category"] == category, "Price"].dropna()
        return float(prices.iloc[0]) if not prices.empty else 0.0

    @staticmethod
    def update_price(category, price):
        """Set the price of every item in a category using the latest CSV."""
        global pax_df, category_list

        if pd.isna(category) or not str(category).strip():
            return "Category is required."
        try:
            price = float(price)
        except (TypeError, ValueError) as error:
            raise ValueError("Price must be a valid number.") from error
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")

        updated_df = _read_items()
        matching_items = updated_df["Category"].eq(category).fillna(False)
        if not matching_items.any():
            return f"Category {category} not found. No prices were updated."

        updated_df.loc[matching_items, "Price"] = price
        updated_df.to_csv(PAX_CSV_PATH, index=False)
        pax_df = updated_df
        category_list = pax_df["Category"].dropna().unique().tolist()
        return "Success"
