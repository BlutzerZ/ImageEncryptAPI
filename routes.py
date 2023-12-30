from main import app
from pydantic import BaseModel

from helper import Affine, base64_to_cv2

Cipher = Affine(71,37,256)

class EncryptDecryptRequestResponse(BaseModel):
    base64: str
    token: str

@app.post("/image/encrypt")
def read_item(request: EncryptDecryptRequestResponse):
    cv2Image = base64_to_cv2(request.base64)
    base64Img = Cipher.encryption(cv2Image)

    return {"status": "success", "data": {
        "base64": base64Img,
    }}

@app.post("/image/decrypt")
def read_item(request: EncryptDecryptRequestResponse):
    cv2Image = base64_to_cv2(request.base64)
    base64Img = Cipher.decryption(cv2Image)

    return {"status": "success", "data": {
        "base64": base64Img,
    }}