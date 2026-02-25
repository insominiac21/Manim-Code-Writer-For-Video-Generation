# FastAPI app entry point for MentorBoxAI
default_app_import = True
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.v1.endpoints import router as api_router

app = FastAPI(title="MentorBoxAI API", version="3.0.0")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.include_router(api_router)
