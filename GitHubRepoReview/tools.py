import requests
import base64

GITHUB_API = "https://api.github.com"

def get_repo_tree(owner, repo, branch="main"):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()["tree"]

def get_python_files(tree):
    return [
        f["path"] for f in tree
        if f["path"].endswith(".py") and "test" not in f["path"].lower()
    ]

def read_github_file(owner, repo, path, branch="main"):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    res = requests.get(url)
    res.raise_for_status()
    content = res.json()["content"]
    decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
    return decoded[:4000]  # safety limit
