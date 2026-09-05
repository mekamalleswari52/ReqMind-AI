from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, projects, documents, analysis, requirements
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReqMind AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(requirements.router, prefix="/api/requirements", tags=["requirements"])

@app.get("/")
async def root():
    return {"message": "ReqMind AI backend running"}
