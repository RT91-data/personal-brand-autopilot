import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")
NOTEBOOKS_PATH = "learning-notes/ml-fundamentals"

def get_notebooks():
    """Fetch list of notebooks from GitHub repo."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{NOTEBOOKS_PATH}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    
    files = response.json()
    notebooks = []
    
    for file in files:
        if file["name"].endswith(".ipynb"):
            # Clean up the name for display
            display_name = file["name"].replace(".ipynb", "").replace("_", " ").title()
            # Remove leading number
            parts = display_name.split(" ", 1)
            if parts[0].isdigit():
                display_name = parts[1] if len(parts) > 1 else display_name
            
            notebooks.append({
                "display_name": display_name,
                "file_name": file["name"],
                "download_url": file["download_url"]
            })
    
    return notebooks

def get_notebook_content(download_url):
    """Fetch and extract content from a notebook."""
    response = requests.get(download_url)
    
    if response.status_code != 200:
        return None
    
    notebook = response.json()
    extracted = {
        "d365_analogy": "",
        "linkedin_post_idea": "",
        "concept": "",
        "how_it_works": ""
    }
    
    for cell in notebook.get("cells", []):
        if cell["cell_type"] == "markdown":
            source = "".join(cell["source"])
            
            if "## My D365 Analogy" in source or "## My D365 analogy" in source:
                extracted["d365_analogy"] = source
            elif "## LinkedIn Post Idea" in source or "## LinkedIn post idea" in source:
                extracted["linkedin_post_idea"] = source
            elif source.startswith("## ") and not any(x in source for x in ["How it", "Where it", "D365", "LinkedIn"]):
                extracted["concept"] = source
            elif "## How it actually works" in source:
                extracted["how_it_works"] = source
    
    return extracted