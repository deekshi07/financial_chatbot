import streamlit as st
from pdf_processor import extract_text_from_pdf, extract_financial_insights
from financial_api import fetch_financial_data
from chatbot import get_chatbot_response
import nltk
import traceback

# Safely ensure NLTK's 'punkt' is available
def setup_nltk():
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
    except Exception:
        st.error("❗ NLTK setup failed")
        st.text(traceback.format_exc())

setup_nltk()

# Define a set of financial keywords for filtering queries
financial_keywords = {
    "revenue", "earnings", "profit", "loss", "net income", "gross margin",
    "ebitda", "dividend", "expenses", "cost of goods sold", "assets", "liabilities",
    "equity", "return on investment", "cash flow", "balance sheet", "financial statement",
    "stock", "shares", "investment", "portfolio", "market", "finance", "financial", "funds"
}

def is_financial_query(query):
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in financial_keywords)

# Title of the application
st.title("📊 AI-Powered Financial Insights Chatbot")

# Radio button for mode selection
option = st.radio("Choose Mode:", ["📄 PDF Upload Mode", "🌐 Live Data Mode", "💬 Chatbot Mode"])

if option == "📄 PDF Upload Mode":
    uploaded_file = st.file_uploader("Upload Earnings Report (PDF)", type=["pdf"])
    if uploaded_file:
        try:
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.subheader("Extracted Text from PDF:")
            st.text_area("Extracted Text", extracted_text, height=300)

            financial_insights = extract_financial_insights(extracted_text)
            st.subheader("Financial Insights:")
            st.text_area("Financial Insights", financial_insights, height=300)

        except Exception as e:
            st.error(f"Error processing the PDF: {str(e)}")

elif option == "🌐 Live Data Mode":
    company_symbol = st.text_input("Enter Company Symbol (e.g., AAPL, TSLA)")
    if st.button("Fetch Data"):
        if company_symbol:
            try:
                financial_data = fetch_financial_data(company_symbol)
                if "error" in financial_data:
                    st.error(financial_data["error"])
                else:
                    st.json(financial_data)
            except Exception as e:
                st.error(f"Error fetching financial data: {str(e)}")
        else:
            st.error("Please enter a valid company symbol.")

elif option == "💬 Chatbot Mode":
    user_query = st.text_input("Ask a financial question:")
    if st.button("Get Response"):
        if user_query:
            if is_financial_query(user_query):
                try:
                    response = get_chatbot_response(user_query)
                    st.text_area("Chatbot Response", response, height=200)
                except Exception as e:
                    st.error(f"Error getting chatbot response: {str(e)}")
            else:
                st.warning("⚠️ Sorry, I can only answer financial related questions.")
        else:
            st.error("Please enter a question to ask the chatbot.")
