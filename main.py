from fastapi import FastAPI , Request
from fastapi.templating import Jinja2Templates

app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.route('/')
def smth(request : Request):
    return templates.TemplateResponse("home.html" , {"request" : request})

