from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import router as api_router

app = FastAPI(title='SrnlPyServeAPI')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to your allowed methods
    allow_headers=["*"],  # Adjust this to your allowed headers
)


app.include_router(api_router)
