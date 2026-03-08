from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.screening import router as screening_router
from app.api.chat_filter import router as chat_router
from app.api.compare import router as compare_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(screening_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(compare_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Resume Screening API Running"}