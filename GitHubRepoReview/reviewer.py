from tools import get_repo_tree, get_python_files
from agent import review_file

def run_review(owner, repo, max_files=5):
    tree = get_repo_tree(owner, repo)
    files = get_python_files(tree)

    # Simple prioritization
    files = sorted(files, key=lambda f: "service" in f or "core" in f, reverse=True)
    selected = files[:max_files]

    results = {}
    for f in selected:
        results[f] = review_file(owner, repo, f)

    return results
