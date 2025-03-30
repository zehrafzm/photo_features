# server.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import mimetypes
from conversion import process_file

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://192.168.1.13:3000"] for stricter access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Output directory
OUTPUT_DIR = "processed_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/process/")
async def process_file_endpoint(
    file: UploadFile = File(...),
    lower_threshold: int = Form(...),
    upper_threshold: int = Form(...),
    is_black_background: bool = Form(...),
):
    # Save uploaded file
    input_path = os.path.join(OUTPUT_DIR, file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Process the file
    output_path = os.path.join(OUTPUT_DIR, f"processed_{file.filename}")
    process_file(
        input_path,
        output_path,
        lower_threshold,
        upper_threshold,
        is_black_background,
    )

    # Detect correct MIME type (e.g., video/mp4 or image/png)
    media_type, _ = mimetypes.guess_type(output_path)

    return FileResponse(output_path, media_type=media_type, filename=f"processed_{file.filename}")
