from datetime import datetime


def format_probability(prob: float) -> str:
    return f"{prob * 100:.1f}%"


def get_confidence_level(prob: float) -> str:
    if prob > 0.8 or prob < 0.2:
        return "High"
    elif prob > 0.6 or prob < 0.4:
        return "Medium"
    return "Low"


def get_risk_level(prob: float) -> str:
    if prob > 0.6:
        return "High Risk"
    elif prob > 0.3:
        return "Moderate"
    return "Low Risk"


def friendly_timestamp(dt: datetime) -> str:
    if not dt:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M")
