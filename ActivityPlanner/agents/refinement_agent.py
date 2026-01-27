# agents/refinement_agent.py

def refine_plan(plan, feedback):
    refined = {}

    for day, activities in plan.items():
        issues = feedback.get(day, [])
        new_activities = activities.copy()

        if "Too many activities" in issues:
            new_activities = new_activities[:3]

        if "Needs rest breaks" in issues:
            new_activities.insert(1, "Rest / Hotel downtime")

        refined[day] = new_activities

    return refined
