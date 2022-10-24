from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import root_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


app.include_router(root_router)
