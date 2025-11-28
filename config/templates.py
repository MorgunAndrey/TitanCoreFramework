# config/templates.py

from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory=os.path.join("app", "Views"))
