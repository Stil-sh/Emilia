import requests
from typing import List, Optional

def fetch_artstation_arts(tags: str = "anime", page: int = 1) -> Optional[List[str]]:
    """Получает арты с ArtStation по тегам через API."""
    url = "https://www.artstation.com/projects.json"
    params = {"page": page, "q": tags}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        arts = []
        for project in data:
            for asset in project.get("assets", []):
                if "image_url" in asset:
                    arts.append(asset["image_url"].replace("small", "large"))  # HD качество
        return arts if arts else None
    
    except Exception as e:
        print(f"[ArtStation] Error: {e}")
        return None
