from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def setup_middlewares(app: FastAPI):
    #Add CORS middleware
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
