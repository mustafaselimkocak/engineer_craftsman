import streamlit as st
import os
import pax_db
from github_csv import GitHubCSV
from scraper import Scraper
from price_calculator import PriceCalculator
from pax_db import PAXDatabase


# import email_handler 
# whitespace for streamlit update !!!

st.set_page_config(
    page_title="PAX Price Calculator",
    page_icon="docs/logo.png",
    layout="wide"
)

st.markdown(
    """
    <style>
    [data-testid="stExpander"] summary p {
        font-size: 1.5rem;
        font-weight: 600;
        line-height: 1.3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the app
st.title("PAX Price Calculator")

# Secrets stay on the server; environment variables are also supported.
try:
    github_settings = dict(st.secrets.get("github", {}))
except FileNotFoundError:
    github_settings = {}

github_settings = {
    key: os.environ.get(key) or github_settings.get(key, "")
    for key in ("GITHUB_TOKEN", "GITHUB_REPOSITORY", "GITHUB_BRANCH")
}
try:
    pax_db.github_store = GitHubCSV(
        github_settings["GITHUB_TOKEN"],
        github_settings["GITHUB_REPOSITORY"],
        github_settings["GITHUB_BRANCH"],
    ) if any(github_settings.values()) else None
    pax_db.refresh_items()
except Exception as error:
    st.error(f"Could not load the price database: {error}")
    st.stop()

scraper = Scraper()

price_calculator = PriceCalculator()

# Adding a text input box
pax_code = st.text_input("Enter your PAX Code:")

if 'pax_code' not in st.session_state:
    st.session_state.pax_code = ''

if st.button("Enter"):

    # Action to be performed when the button is clicked
    if len(pax_code) <= 8:
        try:
            st.session_state.pax_code = pax_code

            data = scraper.fetch_ikea_data(pax_code)
            results = scraper.write_data_to_table(pax_code, data)
            st.write(f"Item Codes and Quantities in PAX Design with code: {pax_code}")
            results.index = range(1, len(results) + 1)
            st.dataframe(results)
            price = price_calculator.calculate_prices(results)
            price = round(price)
            st.write(f"THE COST:  {price} €")
            #st.write(f"THE COST:  {price} €  (incl. VAT)")

        except Exception as e:
            print(e)
            st.write("Not a correct PAX code. Please check your order!")
    else:
        st.write("Not a correct PAX code. Please check your order!")


st.write('')
st.write('')
st.write('')
st.write('')
st.write('')


item_column, category_column = st.columns(2)

with item_column.expander("Add an Item", expanded=False):

    with st.form("add_item_form"):
        category = st.selectbox("Category:", pax_db.category_list)
        description = st.text_input("Description:")
        code = st.text_input("Code:")
        price = st.text_input("Price:")
        save_item = st.form_submit_button("Save Item")

    if save_item:
        try:
            result = PAXDatabase.add_new_item(category, description, code, price)

            if result == "Success":
                st.success("Item saved to GitHub." if pax_db.github_store else "Item saved locally.")
            else:
                st.error(result)

        except Exception as e:
            st.error(f"Item not saved: {e}")

with category_column.expander("Update Category Price", expanded=False):

    category_to_update = st.selectbox("Category:", pax_db.category_list, key="category_to_update")
    old_price = PAXDatabase.get_category_price(category_to_update)
    old_price_display = st.empty()
    old_price_display.write(f"Old Price: {old_price}")

    new_price = st.text_input("New Price:")
    update_price = st.button("Update Price")

    if update_price:
        try:
            result = PAXDatabase.update_price(category_to_update, new_price)

            if result == "Success":
                old_price_display.write(f"Current Price: {new_price}")
                destination = "GitHub" if pax_db.github_store else "the local CSV"
                st.success(f"Category {category_to_update} prices updated to {new_price} in {destination}.")
            else:
                st.error(result)

        except Exception as e:
            st.error(f"Prices not updated: {e}")
