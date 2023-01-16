from typing import List
from fastapi import FastAPI, status
from src.projects.project_router import project_router
from src.app.config import db_settings
from src.auth.auth_router import user_router
from src.organization.org_router import org_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins: List = ["*", "http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(org_router)
app.include_router(project_router)


@app.get("/", status_code=status.HTTP_200_OK)
def root() -> dict:
    return {"message": "Welcome to the Mixer Project, I am Bolt.", "docs": "/docs"}
