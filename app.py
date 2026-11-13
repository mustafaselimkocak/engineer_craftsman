import streamlit as st
import pax_db
from scraper import Scraper
from price_calculator import PriceCalculator
from pax_db import PAXDatabase


# import email_handler 
# whitespace for streamlit update !!!

def contact_us():
    # Title for the Contact Us section
    st.title("Contact Us")

    # Introduction
    st.write("""
    We'd love to hear from you! Whether you have a question about our services, pricing, or anything else, our team is ready to answer all your questions.
    You can reach out to us through the following ways:
    """)

    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    col1, col2, col3 = st.columns(3)

    col1.subheader('📧 Email Us')
    col1.write(
        "For any inquiries, you can email us at [engineercraftsman@gmail.com](mailto:engineercraftsman@gmail.com).")

    col2.subheader('📞 Call Us')
    engineer_craftsman_phone = "+491639171379"
    col2.write(f"You can also reach us by phone at {engineer_craftsman_phone}.")

    col3.subheader('💬 WhatsApp Us')
    message = "Hello, I would like to know more about your services."
    whatsapp_link = f"https://wa.me/{engineer_craftsman_phone}?text={message.replace(' ', '%20')}"
    col3.markdown(f"[Click here to chat with us on WhatsApp]({whatsapp_link})")

    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')


############################################################################################################

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
                st.success("Item saved.")
            else:
                st.error(result)

        except Exception as e:
            st.error("Item not saved.", e)

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
                st.success(f"Category {category_to_update} prices updated as {new_price}.")
            else:
                st.error(result)

        except Exception as e:
            st.error(f"Prices not updated: {e}")


st.write('')
st.write('')
st.write('')
st.write('')
st.write('')

## contact_us()
