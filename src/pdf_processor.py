import fitz  # PyMuPDF
import re
from nltk.tokenize import sent_tokenize
from collections import Counter

# You may need to install NLTK if it's not already installed
# pip install nltk

# Function to extract text from the PDF file
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file and provides financial insights."""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = "\n".join([page.get_text("text") for page in doc])
    return text if text.strip() else "No readable text found in the PDF."

# Function to extract financial insights from the extracted text
def extract_financial_insights(text):
    """Extracts financial terms and generates insights from the text."""
    # Define financial keywords to search for
    financial_terms = [
        "revenue", "earnings", "profit", "loss", "net income", "gross margin", 
        "EBITDA", "dividend", "expenses", "cost of goods sold", "assets", "liabilities",
        "equity", "return on investment", "cash flow", "balance sheet", "financial statement"
    ]
    
    # Convert the text to lowercase and tokenize it into sentences
    text_lower = text.lower()
    sentences = sent_tokenize(text)
    
    # Find sentences containing financial terms
    finance_related_sentences = [sentence for sentence in sentences if any(term in sentence for term in financial_terms)]
    
    # If no sentences found with financial terms, return an appropriate message
    if not finance_related_sentences:
        return "No financial insights found in the document."
    
    # Count the occurrences of financial terms in the document
    term_counts = Counter(re.findall(r'\b(?:' + '|'.join(financial_terms) + r')\b', text_lower))
    
    # Sort terms by frequency of occurrence
    sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Create a summary of the financial terms found
    summary = "Financial Insights:\n"
    for term, count in sorted_terms:
        summary += f"{term.capitalize()}: {count} occurrences\n"
    
    # Include some of the finance-related sentences for context
    summary += "\nSample Finance-Related Sentences:\n"
    summary += "\n".join(finance_related_sentences[:5])  # Show up to 5 sentences
    
    return summary

# Example usage
def get_financial_insights_from_pdf(uploaded_file):
    # Extract text from PDF
    text = extract_text_from_pdf(uploaded_file)
    
    # Get financial insights
    insights = extract_financial_insights(text)
    
    return insights
