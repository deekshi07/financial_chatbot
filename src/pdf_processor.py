import fitz  # PyMuPDF
import re
from nltk.tokenize import sent_tokenize
from collections import Counter

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    Returns the combined text from all pages or a message if no readable text found.
    """
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = "\n".join([page.get_text("text") for page in doc])
    return text if text.strip() else "No readable text found in the PDF."

def extract_financial_insights(text):
    """
    Extracts financial terms and generates insights from the extracted text.
    Returns a summary with term frequency and sample finance-related sentences.
    """
    financial_terms = [
        "revenue", "earnings", "profit", "loss", "net income", "gross margin", 
        "EBITDA", "dividend", "expenses", "cost of goods sold", "assets", "liabilities",
        "equity", "return on investment", "cash flow", "balance sheet", "financial statement"
    ]
    
    text_lower = text.lower()
    sentences = sent_tokenize(text)
    
    # Find sentences containing financial terms (case-insensitive)
    finance_related_sentences = [sentence for sentence in sentences if any(term in sentence.lower() for term in financial_terms)]
    
    if not finance_related_sentences:
        return "No financial insights found in the document."
    
    # Count occurrences of financial terms using regex (word boundaries, case-insensitive)
    term_counts = Counter(re.findall(r'\b(?:' + '|'.join(financial_terms) + r')\b', text_lower))
    
    sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
    
    summary = "Financial Insights:\n"
    for term, count in sorted_terms:
        summary += f"{term.capitalize()}: {count} occurrences\n"
    
    summary += "\nSample Finance-Related Sentences:\n"
    summary += "\n".join(finance_related_sentences[:5])  # Show up to 5 sentences
    
    return summary

def get_financial_insights_from_pdf(uploaded_file):
    """
    Full pipeline: Extract text from PDF and get financial insights summary.
    """
    text = extract_text_from_pdf(uploaded_file)
    insights = extract_financial_insights(text)
    return insights
