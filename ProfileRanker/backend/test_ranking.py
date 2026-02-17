import json
from app.agents.ranking_agent import rank_resumes

# Load sample data
with open("../sample_data/resumes.json", "r") as f:
    resumes = json.load(f)

# Run ranking
ranked = rank_resumes(resumes)

print("\n===== RANKING RESULTS =====\n")

for idx, candidate in enumerate(ranked, start=1):
    print(f"Rank {idx}: {candidate['name']}")
    print(f"Final Score: {candidate['final_score']}")
    print(f"Experience Years: {candidate['experience_years']}")
    print(f"Matched Skills: {candidate['skills']}")
    print(f"Innovation Signals: {candidate['innovation']}")
    print("-" * 50)
