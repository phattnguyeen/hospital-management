from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hospital Management System"}

@app.get("/patients/{patient_id}")
def read_patient(patient_id: int):
    return {"patient_id": patient_id, "name": "John Doe"}

@app.post("/patients/")
def create_patient(name: str, age: int):
    return {"name": name, "age": age, "message": "Patient created successfully"}