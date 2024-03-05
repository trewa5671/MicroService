import os
import random
import requests
import uvicorn as uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    r_id = random.randint(1, 10000)
    r = requests.get(f"https://api.spoonacular.com/recipes/{r_id}/information", params={'apiKey': '3b8b919895eb46479932d5b1112bb274'})
    return r.json()

@app.get("/list/")
async def get_list(q: list | None = Query()):
    if not q:
        return[]
    recipe_list = []
    for id in q:
        r = requests.get(f"https://api.spoonacular.com/recipes/{id}/information", params={'apiKey': '3b8b919895eb46479932d5b1112bb274'})
        recipe_list.append(r.json())
    return recipe_list

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
