from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    auth_routes,
    hackathon_routes,
    participant_routes,
    team_routes,
    task_routes,
    submission_routes,
    evaluation_routes,
)


app = FastAPI(title="Hackathon Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(hackathon_routes.router)
app.include_router(participant_routes.router)
app.include_router(team_routes.router)
app.include_router(task_routes.router)
app.include_router(submission_routes.router)
app.include_router(evaluation_routes.router)


@app.get("/")
def read_root():
    return {"message": "Hackathon Management System API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
