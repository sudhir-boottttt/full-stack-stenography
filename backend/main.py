from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from steganography import encode_image, decode_image
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/encode")
async def encode(image: UploadFile = File(...), message: str = Form(...)):
    img = Image.open(io.BytesIO(await image.read()))
    encoded_img = encode_image(img, message)

    buf = io.BytesIO()
    encoded_img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="image/png",
        headers={
            "Content-Disposition": "attachment; filename=encoded_image.png"
        }
    )

@app.post("/decode")
async def decode(image: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await image.read()))
    message = decode_image(img)
    return {"message": message}
