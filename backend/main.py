from typing import Union
from fastapi import FastAPI
import yaml
import httpx
app = FastAPI()

GITHUB_USERNAME = "Tommasobru"



@app.get("/api/projects")
async def get_projects():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {"error": "Errore nel recupero delle repository"}

        repos = response.json()

        projects = [
            {
                "name": repo["name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "image": f"https://opengraph.githubassets.com/1/{GITHUB_USERNAME}/{repo['name']}"
            }
            for repo in repos
        ]

    return {"projects": projects}