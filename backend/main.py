from typing import Union
from fastapi import FastAPI, Form
import yaml
import httpx
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Abilita tutte le origini per sviluppo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # In produzione, specifica i domini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open('config/credentials/credential.yml', 'r') as f:
     crd = yaml.safe_load(f)

USERNAME = crd['db']['username']
PASSWORD = crd['db']['password']

GITHUB_USERNAME = "Tommasobru"

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/my_web_site_DB"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Contatto(Base):
    __tablename__ = "contatti"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    richiesta = Column(String)

Base.metadata.create_all(bind=engine)

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

@app.post("/api/contatti")
async def ricevi_contatti(
    nome: str = Form(...),
    email: str = Form(...),
    richiesta: str = Form(...)
):
    db = SessionLocal()
    nuovo_contatto = Contatto(nome = nome, email = email, richiesta = richiesta)
    db.add(nuovo_contatto)
    db.commit()
    db.close()

    return {"message": "Messaggio ricevuto!"}
