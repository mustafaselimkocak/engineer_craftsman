import streamlit as st
from scraper import Scraper
from price_calculator import PriceCalculator

# Title of the app
st.title("PAX Price Calculator")

scraper = Scraper()

price_calculator = PriceCalculator()

# test R79FBM

# Adding a text input box
pax_code = st.text_input("Enter your PAX Code:")

if st.button("Submit"):

    # Action to be performed when the button is clicked
    if pax_code:
        data = scraper.fetch_ikea_data(pax_code)
        results = scraper.write_data_to_table(pax_code, data)
        st.write(f"Item Codes and Quantities in {pax_code}")
        st.dataframe(results)
        price = price_calculator.calculate_prices(results)
        st.write(f"Price: {price} €")

    else:
        st.write("PAX not found")
