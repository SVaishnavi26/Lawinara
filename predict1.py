import pandas as pd
import difflib
import random

# Load the case data
df = pd.read_excel("data/details.xlsx")  # Ensure this contains 'Case Description', 'Act & Section', 'Final Judgment'

# Convert the dataset into a dictionary for quick lookup
case_dict = {row["Case Description "]: (row["Act & Section"], row["Final Judgment"]) for _, row in df.iterrows()}

# List of random alternative judgments
random_judgments = [
    ("Section 13, Hindu Marriage Act", "Divorce granted due to irretrievable breakdown of marriage."),
    ("Section 10, Indian Divorce Act", "Christian couple granted divorce on the grounds of adultery and desertion."),
    ("Section 125, CrPC", "Muslim wife awarded ₹8,000 per month as maintenance after being abandoned by her husband."),
    ("Section 7, Guardian and Wards Act", "Father granted joint custody of the child after assessing the child's best interests."),
    ("Section 32, Special Marriage Act", "Divorce granted due to refusal to consummate the marriage."),
    ("Section 36, Parsi Marriage and Divorce Act", "Interim alimony of ₹20,000 per month granted to the wife."),
    ("Section 2, Muslim Women (Protection of Rights on Divorce) Act", "Wife granted lump sum maintenance under Islamic law."),
    ("Section 15, Hindu Adoption and Maintenance Act", "Adopted child given equal inheritance rights as a biological child."),
    ("Section 3, Indian Christian Marriage Act", "Marriage declared null and void due to fraud in obtaining consent."),
    ("Section 9, Hindu Marriage Act", "Restitution of conjugal rights denied due to proven domestic abuse."),
]



def predict_case(input_description):
    """Finds the closest matching case and returns Act & Section and Final Judgment."""
    # Get the closest match
    closest_match = difflib.get_close_matches(input_description, case_dict.keys(), n=1, cutoff=0.6)
    
    if closest_match:
        matched_case = closest_match[0]  # Best match found
        result = case_dict[matched_case]
        return {
            "Matched Case Description": matched_case,
            "Predicted Act & Section": result[0],
            "Predicted Judgment": result[1]
        }
    else:
        # Pick a random judgment from the list
        random_act_section, random_judgment = random.choice(random_judgments)
        return {
            "Matched Case Description": "No exact match found. Returning a random judgment.",
            "Predicted Act & Section": random_act_section,
            "Predicted Judgment": random_judgment
        }


