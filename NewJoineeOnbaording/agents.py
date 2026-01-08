import random
from data import BUDDIES, SOFTWARES, CONFLUENCE_LINK


def profile_agent(profile):
    return {
        "employee_id": f"EMP{random.randint(1000,9999)}",
        "name": profile["name"],
        "role": profile["role"],
        "department": profile["department"]
    }


def it_access_agent(profile):
    email = f"{profile['name'].lower().replace(' ', '.')}@company.com"

    return {
        "email": email,
        "wifi_access": True,
        "email_access": True,
        "software_access": SOFTWARES[:3]
    }


def buddy_agent():
    return random.choice(BUDDIES)


def knowledge_agent():
    return {
        "confluence": CONFLUENCE_LINK,
        "documents": [
            "Employee Handbook",
            "Engineering Guidelines",
            "Security Policies"
        ]
    }
