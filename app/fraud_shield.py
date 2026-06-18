# app/fraud_shield.py

FRAUD_PATTERNS = [
    {
        "id": "guaranteed_returns",
        "name": "Guaranteed High Returns",
        "keywords": ["guaranteed", "assured", "fixed return", "100% safe", "no risk", "double money"],
        "risk_level": "CRITICAL",
        "explanation": "No legitimate investment guarantees high fixed returns. Even FDs and government bonds don't promise above 8.5%. Anyone promising 15–30% guaranteed returns is running a Ponzi scheme.",
        "action": "Do NOT invest. Report at cybercrime.gov.in or call 1930."
    },
    {
        "id": "whatsapp_tips",
        "name": "WhatsApp/Telegram Stock Tips",
        "keywords": ["whatsapp group", "telegram", "stock tip", "insider tip", "sure shot", "multibagger tip"],
        "risk_level": "HIGH",
        "explanation": "Stock tip groups on WhatsApp/Telegram are almost always pump-and-dump schemes. Operators buy a stock cheap, hype it in groups, then sell when price rises — leaving you with losses.",
        "action": "Leave the group. Never invest based on anonymous tips."
    },
    {
        "id": "fake_trading_app",
        "name": "Fake Trading App",
        "keywords": ["new app", "trading app", "showing profit", "can't withdraw", "withdrawal blocked", "withdrawal fee"],
        "risk_level": "CRITICAL",
        "explanation": "Fake trading apps show artificial profits to build trust, then block withdrawals. They ask for 'taxes' or 'fees' to release money — that money is also stolen.",
        "action": "Stop depositing immediately. Report to cybercrime.gov.in. Call 1930."
    },
    {
        "id": "loan_fraud",
        "name": "Fake Loan / Processing Fee Scam",
        "keywords": ["instant loan", "no documents", "processing fee", "advance fee", "loan approved"],
        "risk_level": "HIGH",
        "explanation": "Fake lenders approve loans instantly with no checks, then ask for 'processing fees' or 'insurance' upfront. Once paid, they disappear. Real banks never ask for upfront fees.",
        "action": "Never pay any fee before receiving a loan. Verify lender on RBI website."
    },
    {
        "id": "upi_scam",
        "name": "UPI / QR Code Scam",
        "keywords": ["scan qr", "receive money", "upi request", "collect request", "enter pin to receive"],
        "risk_level": "CRITICAL",
        "explanation": "You never need to enter your UPI PIN or scan a QR code to RECEIVE money. Scammers send 'collect requests' pretending to send you money — but it actually debits your account.",
        "action": "Never enter PIN for receiving money. Decline all unknown collect requests."
    },
    {
        "id": "fake_sebi_advisor",
        "name": "Unregistered Investment Advisor",
        "keywords": ["investment advisor", "portfolio manager", "sebi registered", "certified advisor", "wealth manager"],
        "risk_level": "MEDIUM",
        "explanation": "Anyone giving paid investment advice must be SEBI registered. Many fake advisors claim to be SEBI certified without actual registration.",
        "action": "Verify at sebi.gov.in → Intermediaries section before paying any advisor."
    },
    {
        "id": "ponzi_scheme",
        "name": "Ponzi / MLM Scheme",
        "keywords": ["refer and earn", "chain system", "pyramid", "network marketing", "downline", "recruit members"],
        "risk_level": "CRITICAL",
        "explanation": "Schemes that pay you mainly for recruiting others are Ponzi/MLM structures. Early members profit from later members' money. They always collapse, leaving most people with losses.",
        "action": "Do NOT join. Report to SEBI at scores.sebi.gov.in"
    },
    {
        "id": "fake_ipo",
        "name": "Fake IPO / Unlisted Shares",
        "keywords": ["upcoming ipo", "unlisted shares", "pre-ipo", "guaranteed listing gains"],
        "risk_level": "HIGH",
        "explanation": "Scammers sell fake 'pre-IPO' shares or unlisted shares that don't exist or are worthless. Legitimate IPOs only come through SEBI-registered brokers.",
        "action": "Only apply for IPOs through your registered broker or UPI-linked bank app."
    }
]

def scan_for_fraud(user_message: str) -> dict:
    message_lower = user_message.lower()
    detected = []

    for pattern in FRAUD_PATTERNS:
        for keyword in pattern["keywords"]:
            if keyword.lower() in message_lower:
                if pattern not in detected:
                    detected.append(pattern)
                break

    if not detected:
        return {"fraud_detected": False, "patterns": []}

    highest_risk = "MEDIUM"
    for p in detected:
        if p["risk_level"] == "CRITICAL":
            highest_risk = "CRITICAL"
            break
        elif p["risk_level"] == "HIGH":
            highest_risk = "HIGH"

    return {
        "fraud_detected": True,
        "highest_risk":   highest_risk,
        "patterns":       detected,
        "count":          len(detected)
    }


def get_fraud_warning_prompt(scan_result: dict, user_message: str) -> str:
    patterns = scan_result["patterns"]
    risk     = scan_result["highest_risk"]

    pattern_details = ""
    for p in patterns:
        pattern_details += f"""
⚠️ DETECTED: {p['name']} (Risk: {p['risk_level']})
- Why it's dangerous: {p['explanation']}
- What to do: {p['action']}
"""

    return f"""
FRAUD ALERT DETECTED in user's message.
Risk Level: {risk}

User said: "{user_message}"

Fraud patterns found:
{pattern_details}

IMPORTANT INSTRUCTIONS:
1. Start your response with a clear fraud warning
2. Explain WHY this is dangerous in simple language  
3. Tell them EXACTLY what to do (or not do)
4. Give them verification steps (SEBI/RBI website)
5. Be firm but not scary — educate, don't panic them
6. End with: Report fraud at cybercrime.gov.in or call helpline 1930
""".strip()


def format_fraud_response(scan_result: dict) -> str:
    risk_emoji = {
        "CRITICAL": "🚨",
        "HIGH":     "⚠️",
        "MEDIUM":   "🔔"
    }

    patterns = scan_result["patterns"]
    risk     = scan_result["highest_risk"]
    emoji    = risk_emoji.get(risk, "⚠️")

    lines = [
        f"{emoji} FRAUD SHIELD ALERT — Risk Level: {risk}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]

    for p in patterns:
        lines.append(f"\n🔍 {p['name']}")
        lines.append(f"   {p['explanation']}")
        lines.append(f"   ✅ Action: {p['action']}")

    lines.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📞 Report fraud: cybercrime.gov.in | Helpline: 1930")

    return "\n".join(lines)