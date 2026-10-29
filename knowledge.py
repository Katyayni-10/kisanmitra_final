"""Small built-in knowledge base so Saathi answers about government schemes from facts, not guesses.

IMPORTANT: scheme details change. Re-check each entry against the official website before the
exhibition (the `site` / `help` fields tell you where) and update anything that has changed.
"""

SCHEMES = [
    {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "who": "Farmer families who own cultivable land. Not for income-tax payers or higher-income government employees and pensioners.",
        "benefit": "Rs 6,000 per year, paid in three installments of Rs 2,000 straight into the bank account.",
        "documents": "Aadhaar, bank account linked with Aadhaar, land records, mobile number.",
        "how": "Register on pmkisan.gov.in, or at a Common Service Centre (CSC), or through the village patwari or agriculture officer. Complete e-KYC.",
        "help": "PM-KISAN helpline 155261.",
    },
    {
        "name": "Ayushman Bharat PM-JAY (health insurance)",
        "who": "Poor and vulnerable families listed in the government database. Senior citizens aged 70 and above can also get cover through the Ayushman Vay Vandana card.",
        "benefit": "Cashless hospital treatment up to Rs 5 lakh per family per year at listed government and private hospitals.",
        "documents": "Aadhaar, ration card or other ID, mobile number.",
        "how": "Check eligibility on mera.pmjay.gov.in or ask the Ayushman Mitra at a listed hospital or a CSC, then get the Ayushman card made.",
        "help": "Helpline 14555.",
    },
    {
        "name": "Atal Pension Yojana",
        "who": "People aged 18 to 40 with a savings bank account. Not for income-tax payers.",
        "benefit": "Fixed monthly pension of Rs 1,000 to Rs 5,000 after age 60, depending on the monthly amount chosen.",
        "documents": "Aadhaar, bank account, mobile number.",
        "how": "Apply at your bank branch or through net banking. The monthly amount is cut automatically from the bank account.",
        "help": "Ask your bank branch.",
    },
    {
        "name": "PM Ujjwala Yojana (free LPG gas connection)",
        "who": "Women from poor households (BPL) who do not have an LPG connection.",
        "benefit": "LPG gas connection with no connection fee. Ask the distributor about current extra benefits such as the first refill and stove.",
        "documents": "Aadhaar, ration card, bank passbook, passport-size photo, BPL proof.",
        "how": "Apply at the nearest LPG gas distributor or on pmuy.gov.in.",
        "help": "Ask the local LPG distributor.",
    },
    {
        "name": "Old age pension (Indira Gandhi National Old Age Pension Scheme)",
        "who": "Citizens aged 60 and above from poor (BPL) households.",
        "benefit": "Monthly pension paid by the central and state governments. The amount is different in each state.",
        "documents": "Age proof, BPL card or ration card, Aadhaar, bank account passbook, photo.",
        "how": "Apply at the gram panchayat, block office, or the state social welfare department or e-district portal.",
        "help": "Elder Line 14567.",
    },
    {
        "name": "PM Jan Dhan Yojana (zero-balance bank account)",
        "who": "Anyone who does not have a bank account.",
        "benefit": "Savings account with zero balance, a RuPay debit card with accident insurance, and a way to receive government money directly.",
        "documents": "Aadhaar, or another ID proof, and a photo.",
        "how": "Go to any bank branch or ask the Bank Mitra (bank agent) in the village.",
        "help": "Ask your bank branch.",
    },
    {
        "name": "PM Awas Yojana - Gramin (house for rural families)",
        "who": "Rural families without a pucca house, whose names are on the official government survey list.",
        "benefit": "Money to build a pucca house: about Rs 1.2 lakh in plain areas and Rs 1.3 lakh in hilly areas, plus support for a toilet and paid work days under MGNREGA.",
        "documents": "Aadhaar, job card, bank account passbook.",
        "how": "Contact the gram panchayat or block development office to check if your name is on the list.",
        "help": "Block development office.",
    },
    {
        "name": "PM Fasal Bima Yojana (crop insurance)",
        "who": "Farmers growing notified crops, including tenant farmers.",
        "benefit": "Money if the crop is damaged by drought, flood, hailstorm, pests or disease. Farmers pay a small premium: 2 percent for kharif food crops, 1.5 percent for rabi food crops, 5 percent for cash and horticulture crops.",
        "documents": "Aadhaar, bank passbook, land record or sowing certificate.",
        "how": "Apply through your bank, a CSC, or pmfby.gov.in before the last date of the season. Farmers with crop loans are usually covered through the bank. If the crop is damaged, report it within 72 hours.",
        "help": "Crop insurance helpline 14447.",
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "who": "Farmers, including tenant farmers and sharecroppers.",
        "benefit": "Easy farm loans at low interest, with extra interest relief for repaying on time.",
        "documents": "Aadhaar, land records, photo, bank details.",
        "how": "Apply at your bank branch or cooperative bank.",
        "help": "Ask your bank branch.",
    },
    {
        "name": "e-Shram card (for unorganised workers)",
        "who": "Workers aged 16 to 59 in the unorganised sector, such as farm labour, construction and domestic workers. Not for EPFO or ESIC members or income-tax payers.",
        "benefit": "e-Shram card with accident insurance: Rs 2 lakh for death or permanent disability and Rs 1 lakh for partial disability.",
        "documents": "Aadhaar, bank account, mobile number linked with Aadhaar.",
        "how": "Register free on eshram.gov.in or at a CSC.",
        "help": "e-Shram helpline 14434.",
    },
    {
        "name": "Ration card (National Food Security Act)",
        "who": "Poor households as identified by the state government.",
        "benefit": "Foodgrain from the ration shop: 5 kg per person per month for priority households and 35 kg per family for Antyodaya households, free of cost at present.",
        "documents": "Aadhaar of family members, address proof, passport-size photos. Other papers depend on the state.",
        "how": "Apply at the state food and civil supplies office, the state online portal, or a CSC.",
        "help": "State food department or local ration office.",
    },
    {
        "name": "Sukanya Samriddhi Yojana (savings for a girl child)",
        "who": "Parents or guardians of a girl child below 10 years.",
        "benefit": "Savings account with government-set interest, meant for the girl's education and marriage. Minimum Rs 250 and maximum Rs 1.5 lakh can be deposited per year.",
        "documents": "Girl's birth certificate, parent's ID and address proof.",
        "how": "Open the account at any post office or authorised bank.",
        "help": "Ask the post office.",
    },
]

SAFETY_TIPS = (
    "Never share your OTP, ATM PIN, UPI PIN, password or card number with anyone, even if they say they are from the bank, "
    "police or government. Banks never ask for OTP on the phone. Do not click unknown links or install apps sent on WhatsApp. "
    "If money was taken by fraud, call 1930 (National Cyber Crime helpline) immediately and tell your bank."
)

HELPLINES = [
    ("Emergency (police / fire / ambulance)", "112"),
    ("Ambulance (most states)", "108"),
    ("Elder Line (senior citizens)", "14567"),
    ("Ayushman Bharat", "14555"),
    ("Cyber fraud", "1930"),
    ("Women helpline", "181"),
    ("Child helpline", "1098"),
    ("Mental health (Tele-MANAS)", "14416"),
    ("PM-KISAN", "155261"),
    ("Crop insurance", "14447"),
]

EMERGENCY_BANNER = (
    "🚨 This may be an emergency. Call 108 (ambulance) or 112 right now, or go to the nearest hospital. "
    "यह आपातकाल हो सकता है। तुरंत 108 या 112 पर फोन करें।"
)

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "can't breathe", "cannot breathe", "not breathing", "difficulty breathing",
    "unconscious", "fainted", "snake bite", "snakebite", "severe bleeding", "heavy bleeding", "poison",
    "overdose", "stroke", "seizure", "accident", "suicide", "kill myself", "want to die",
    "सीने में दर्द", "सीने मे दर्द", "सांस नहीं", "साँस नहीं", "सांस लेने में तकलीफ", "बेहोश", "सांप ने काटा",
    "साँप ने काटा", "सांप काट", "खून बहुत", "जहर", "ज़हर", "दौरा", "दुर्घटना", "एक्सीडेंट", "आत्महत्या", "मरना चाहता", "मरना चाहती",
    "seene mein dard", "saans nahi", "behosh", "saanp ne kata", "zeher",
]


def kb_as_text() -> str:
    parts = []
    for s in SCHEMES:
        parts.append(
            f"SCHEME: {s['name']}\n"
            f"  Who can get it: {s['who']}\n"
            f"  Benefit: {s['benefit']}\n"
            f"  Documents: {s['documents']}\n"
            f"  How to apply: {s['how']}\n"
            f"  Help: {s['help']}"
        )
    parts.append(f"SAFETY TIPS (frauds and scams): {SAFETY_TIPS}")
    return "\n\n".join(parts)
