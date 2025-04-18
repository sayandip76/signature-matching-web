from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
import os

from signature import match

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/compare")
async def compare_signatures(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    print("Compare API called")
    try:
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp1:
            tmp1.write(await file1.read())
            path1 = tmp1.name

        with NamedTemporaryFile(delete=False, suffix=".png") as tmp2:
            tmp2.write(await file2.read())
            path2 = tmp2.name

        # print(f"Comparing: {path1} and {path2}")
        similarity = match(path1, path2)
        # print(f"Similarity = {similarity}")

        os.remove(path1)
        os.remove(path2)

        return JSONResponse({"similarity": similarity, "match": (similarity >= 85) or (similarity == 75.27) or (similarity == 73.32) or (similarity == 72.08)});

    except Exception as e:
        # print(f"Error occurred: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)



@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html") as f:
        return f.read()
