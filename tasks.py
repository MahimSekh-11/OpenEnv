from typing import List, Dict, Any

def easy_grader(env) -> float:
    # Easy: Just needs correct category
    if env.assigned_category == "account":
        return 1.0
    return 0.0

def medium_grader(env) -> float:
    # Medium: Needs category and specific keyword in response
    score = 0.0
    if env.assigned_category == "billing":
        score += 0.4
    
    responses = [h["content"] for h in env.history if h["role"] == "agent" and h["content"].startswith("Response:")]
    if any("portal" in r.lower() for r in responses):
        score += 0.6
    return score

def hard_grader(env) -> float:
    # Hard: Needs multiple steps and specific details
    score = 0.0
    if env.assigned_category == "shipping":
        score += 0.2
    
    responses = [h["content"] for h in env.history if h["role"] == "agent" and h["content"].startswith("Response:")]
    full_text = " ".join(responses).lower()
    
    if "refund" in full_text:
        score += 0.3
    if "tracking" in full_text:
        score += 0.3
    if "address updated" in full_text:
        score += 0.2
    return score

TASKS = [
    {
        "name": "password_reset",
        "difficulty": "easy",
        "content": "I can't log in to my account. I think I forgot my password. Can you help?",
        "expected_category": "account",
        "required_keywords": ["reset link", "email"],
        "grader": easy_grader
    },
    {
        "name": "billing_update",
        "difficulty": "medium",
        "content": "I need to change my credit card on file. Where do I go to update my billing info?",
        "expected_category": "billing",
        "required_keywords": ["billing portal", "settings"],
        "grader": medium_grader
    },
    {
        "name": "complex_shipping_issue",
        "difficulty": "hard",
        "content": "My order #98765 is 3 days late. I want a refund for the shipping cost. Also, please update my default shipping address to 123 Main St for my next order.",
        "expected_category": "shipping",
        "required_keywords": ["refund", "tracking", "address updated"],
        "grader": hard_grader
    }
]
