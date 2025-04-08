from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random, requests

app = FastAPI()

OTP_STORE = {}

class SMSRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    phone_number: str
    otp: str

def generate_otp():
    return str(random.randint(100000, 999999))

def send_sms_via_custom_api(phone: str, otp: str):
    # Ví dụ: Gửi tin nhắn qua API của FPT, VNPT hoặc bên thứ ba khác
    payload = {
        "to": phone,
        "message": f"Mã xác thực của bạn là: {otp}"
    }
    # Thay bằng URL API thực tế của bạn
    response = requests.post("https://sms-provider.vn/api/send", json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Gửi SMS thất bại")

@app.post("/send-otp")
def send_otp(data: SMSRequest):
    otp = generate_otp()
    OTP_STORE[data.phone_number] = otp
    send_sms_via_custom_api(data.phone_number, otp)
    return {"message": "OTP đã được gửi"}

@app.post("/verify-otp")
def verify_otp(data: OTPVerifyRequest):
    if OTP_STORE.get(data.phone_number) == data.otp:
        return {"verified": True}
    raise HTTPException(status_code=400, detail="OTP không đúng hoặc đã hết hạn")
