from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.handlers.chat import chat_router

def create_app():
    app = FastAPI()
    
    # Configure templates and static files
    BASE_DIR = Path(__file__).parent.parent
    templates = Jinja2Templates(directory=BASE_DIR/"templates")
    app.mount("/static", StaticFiles(directory=BASE_DIR/"static"), name="static")
    
    # Root route
    @app.get("/")
    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    
    # API Routes
    app.include_router(chat_router, prefix="/api/v1")
    
    return app

app = create_app()