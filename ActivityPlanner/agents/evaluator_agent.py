# agents/evaluator_agent.py

def evaluate_plan(plan, prefs):
    feedback = {}

    for day, activities in plan.items():
        issues = []

        if len(activities) > prefs["daily_activity_limit"]:
            issues.append("Too many activities")

        if prefs["kids"] == "Infants / Toddlers":
            issues.append("Needs rest breaks")

        feedback[day] = issues

    return feedback
