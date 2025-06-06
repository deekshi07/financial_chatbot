import streamlit as st
from pdf_processor import extract_text_from_pdf, extract_financial_insights
from financial_api import fetch_financial_data
from chatbot import get_chatbot_response  # Import the function from chatbot.py

# Title of the application
st.title("📊 AI-Powered Financial Insights Chatbot")

# Radio button for mode selection
option = st.radio("Choose Mode:", ["📄 PDF Upload Mode", "🌐 Live Data Mode", "💬 Chatbot Mode"])

# PDF Upload Mode
if option == "📄 PDF Upload Mode":
    uploaded_file = st.file_uploader("Upload Earnings Report (PDF)", type=["pdf"])
    if uploaded_file:
        try:
            # Extract text from uploaded PDF
            extracted_text = extract_text_from_pdf(uploaded_file)
            
            # Display the extracted text in a text area
            st.subheader("Extracted Text from PDF:")
            st.text_area("Extracted Text", extracted_text, height=300)
            
            # Extract financial insights from the extracted text
            financial_insights = extract_financial_insights(extracted_text)
            
            # Display financial insights in a separate text area
            st.subheader("Financial Insights:")
            st.text_area("Financial Insights", financial_insights, height=300)
        
        except Exception as e:
            st.error(f"Error processing the PDF: {str(e)}")

# Live Data Mode
elif option == "🌐 Live Data Mode":
    company_symbol = st.text_input("Enter Company Symbol (e.g., AAPL, TSLA)")
    if st.button("Fetch Data"):
        if company_symbol:
            try:
                # Fetch financial data based on company symbol
                financial_data = fetch_financial_data(company_symbol)
                if "error" in financial_data:
                    st.error(financial_data["error"])
                else:
                    st.json(financial_data)
            except Exception as e:
                st.error(f"Error fetching financial data: {str(e)}")
        else:
            st.error("Please enter a valid company symbol.")

# Chatbot Mode
elif option == "💬 Chatbot Mode":
    user_query = st.text_input("Ask a financial question:")
    if st.button("Get Response"):
        if user_query:
            try:
                # Get response from the chatbot (calling function from chatbot.py)
                response = get_chatbot_response(user_query)
                
                # Display chatbot response
                st.text_area("Chatbot Response", response, height=200)
                
            except Exception as e:
                # If error occurs, show error message
                st.error(f"Error getting chatbot response: {str(e)}")
        else:
            st.error("Please enter a question to ask the chatbot.")
