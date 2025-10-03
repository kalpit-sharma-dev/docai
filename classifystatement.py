import pdfplumber
import re
import pandas as pd

# --- CATEGORY DEFINITIONS ---
DEBIT_CATEGORIES = {
    "Investment": ["investment", "sip", "mutual fund", "fd through mobile", "zerodha", "coin"],
    "Shopping": ["shopping", "amazon", "myntra", "flipkart"],
    "Travel": ["travel", "uber", "ola", "flight", "indigo"],
    "Food": ["swiggy", "zomato", "restaurant", "blinkit", "zepto"],
    "EMI": ["emi"],
    "Utilities": ["electricity bill", "tata power", "uppcl"],
    "Maintenance": ["maintenance"],
    "Transfer": ["neft dr", "imps", "tpt", "ib funds transfer dr", "upi"],
    "Cash Withdrawal": ["atm", "cash withdrawal"],
    "Misc": ["pharmacy", "bookmyshow", "google play", "spotify", "youtube"]
}

CREDIT_CATEGORIES = {
    "Salary": ["salary"],
    "Refund/Reversal": ["reversal", "neft return"],
    "Transfer": ["neft cr", "ib funds transfer cr", "imps"],
    "Misc": ["refund", "credit"]
}

# --- PDF PATH ---
pdf_path = "1Acct Statement_1725_03102025_20.52.45_unlocked (2).pdf"

data = []
pattern = re.compile(
    r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+(\d{2}/\d{2}/\d{2})?\s*([\d,]+\.\d{2})?\s*([\d,]+\.\d{2})?\s*([\d,]+\.\d{2})"
)

# --- CATEGORY CLASSIFICATION FUNCTION ---
def classify_transaction(narration, debit, credit):
    narration_low = narration.lower()

    if debit != "0":  # debit transaction
        for category, keywords in DEBIT_CATEGORIES.items():
            if any(keyword in narration_low for keyword in keywords):
                return category
        return "Uncategorized Debit"

    elif credit != "0":  # credit transaction
        for category, keywords in CREDIT_CATEGORIES.items():
            if any(keyword in narration_low for keyword in keywords):
                return category
        return "Uncategorized Credit"

    return "Unknown"

# --- EXTRACT DATA ---
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split("\n"):
            match = pattern.search(line)
            if match:
                date = match.group(1)
                narration = match.group(2).strip()
                withdrawal = match.group(4) if match.group(4) else "0"
                deposit = match.group(5) if match.group(5) else "0"
                balance = match.group(6)

                category = classify_transaction(narration, withdrawal, deposit)

                data.append({
                    "Date": date,
                    "Narration": narration,
                    "Withdrawal": float(withdrawal.replace(",", "")) if withdrawal != "0" else 0.0,
                    "Deposit": float(deposit.replace(",", "")) if deposit != "0" else 0.0,
                    "Balance": float(balance.replace(",", "")),
                    "Category": category
                })

# --- CONVERT TO DATAFRAME ---
df = pd.DataFrame(data)

# --- AGGREGATED TOTALS ---
category_totals = df.groupby("Category")[["Withdrawal", "Deposit"]].sum().reset_index()

# --- SAVE CLEANED DATA ---
df.to_csv("classified_statement.csv", index=False)
category_totals.to_csv("category_summary.csv", index=False)

print("Sample Transactions:\n", df.head(10))
print("\nCategory Totals:\n", category_totals)
