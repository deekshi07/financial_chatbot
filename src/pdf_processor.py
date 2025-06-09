import fitz  # PyMuPDF
import re
from nltk.tokenize import sent_tokenize
from collections import Counter

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = "\n".join([page.get_text("text") for page in doc])
    return text if text.strip() else "No readable text found in the PDF."

def extract_financial_insights(text):
    """Extracts financial terms and generates structured financial insights."""
    financial_terms = [
        "revenue", "earnings", "profit", "loss", "net income", "gross margin",
        "ebitda", "dividend", "expenses", "cost of goods sold", "assets", "liabilities",
        "equity", "return on investment", "cash flow", "balance sheet", "financial statement",
        "loan", "interest rate", "mortgage", "credit", "debit", "capital", "investment",
        "bond", "stock", "shareholder", "portfolio", "yield", "bankruptcy", "tax", "audit",
        "forex", "inflation", "deflation", "budget", "fund", "deposit", "withdrawal",
        "cash", "liquidity", "collateral", "diversification"
    ]

    text_lower = text.lower()
    sentences = sent_tokenize(text)

    # Find sentences that contain financial terms
    finance_sentences = [s for s in sentences if any(term in s.lower() for term in financial_terms)]

    if not finance_sentences:
        return "No financial insights found in the document."

    # Count financial term occurrences
    pattern = r'\b(?:' + '|'.join(re.escape(term) for term in financial_terms) + r')\b'
    term_counts = Counter(re.findall(pattern, text_lower, flags=re.IGNORECASE))
    sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)

    # Limit to top 5 terms and 3 example sentences
    top_terms = sorted_terms[:5]
    example_sentences = finance_sentences[:3]

    # Build structured insights as a dict (you can convert to JSON or display nicely in Streamlit)
    insights = {
        "Top Financial Terms": [{ "term": term.capitalize(), "count": count} for term, count in top_terms],
        "Example Sentences": [sentence.strip() for sentence in example_sentences]
    }

    # Format nicely as a string for display
    formatted = "=== Financial Insights ===\n\nTop Financial Terms:\n"
    for item in insights["Top Financial Terms"]:
        formatted += f" • {item['term']}: {item['count']} occurrences\n"

    formatted += "\nExample Sentences:\n"
    for i, sentence in enumerate(insights["Example Sentences"], 1):
        formatted += f" {i}. {sentence}\n"

    return formatted

def get_financial_insights_from_pdf(uploaded_file):
    text = extract_text_from_pdf(uploaded_file)
    insights = extract_financial_insights(text)
    return insights
