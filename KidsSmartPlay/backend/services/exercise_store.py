from agents.curriculum_agent import generate_curriculum

EXERCISES = None

def load_exercises():
    global EXERCISES
    if EXERCISES is None:
        print("Generating exercises from LLM...")
        EXERCISES = generate_curriculum()
        print("Total exercises:", len(EXERCISES))
    return EXERCISES

