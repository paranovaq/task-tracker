from fastapi import FastAPI
from controllers.task_routes import router

app = FastAPI()
app.include_router(router)
