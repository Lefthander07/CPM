import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from jinja2 import Template
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from cpm import ProjectNetwork
from cpm import Node
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
app = FastAPI()

origins = [
    "http://127.0.0.1:5001",  # Разрешите этот источник
    "http://localhost:5001",   # Или этот
    # Добавьте другие источники, если необходимо
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешите все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешите все заголовки
)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Activity(BaseModel):
    activity_number: str
    duration: float
    predecessors: List[str]


@app.post("/calculate_critical_path")
async def calculate_critical_path(activities: List[Activity]):

    total_duration = 0
    project = ProjectNetwork()

    for act in activities:
        predecessors = []
        if len(act.predecessors) != 0 and act.predecessors[0] != '':
            for predecessor in act.predecessors:
                predecessors.append(int(predecessor))
        node = Node(int(act.activity_number), act.duration, predecessors)
        project.add_node(node)


    project.calculate_early_start_and_finish()
    project.calculate_late_start_and_finish()
    cp = list(project.find_all_paths(0))
    cp,time = project.find_critical_paths(0)
    for i in range(len(cp)):
        cp[i] = cp[i][1:-1]
    return {"cp": cp, "time":time}


@app.get("/")
async def root():
    return FileResponse("../templates/index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5001, log_level="info")