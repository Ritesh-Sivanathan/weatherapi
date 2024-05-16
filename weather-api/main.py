from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import python_weather
import asyncio
import os

location = 'Toronto'

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def get_weather():
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(location)
        return weather

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    weather = await get_weather()
    return templates.TemplateResponse("homepage.html", {"request": request, "weather": weather, "location": location})

if __name__ == '__main__':
    
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
