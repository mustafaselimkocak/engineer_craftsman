import streamlit as st
from scraper import Scraper
from price_calculator import PriceCalculator


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
    page_title="Engineer Craftsman",
    page_icon="docs/logo.png",
    layout="wide"
)

# Title of the app
st.title("Engineer Craftsman PAX Price Calculator")

scraper = Scraper()

price_calculator = PriceCalculator()

# Adding a text input box
pax_code = st.text_input("Enter your PAX Code:")

if 'pax_code' not in st.session_state:
    st.session_state.pax_code = ''

if st.button("Enter"):

    # Action to be performed when the button is clicked
    if len(pax_code) == 6:
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

contact_us()
