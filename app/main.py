import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from jinja2 import Template
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
origins = [
    "http://localhost:5001",
    "http://127.0.0.1:5001",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Укажите, какие источники могут делать запросы
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)
app.mount("/static", StaticFiles(directory="static"), name="static")

class Activity(BaseModel):
    activity_number: str
    duration: float
    predecessors: List[str]

@app.post("/calculate_critical_path")
async def calculate_critical_path(activities: List[Activity]):
    critical_path = []
    total_duration = 0


    # Формируем ответ
    response_data = {
        "critical_path": critical_path,
        "total_duration": total_duration
    }

    return response_data

@app.get("/")
async def root():
    return FileResponse("../templates/index.html")



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5001, log_level="info")