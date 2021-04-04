import joblib
import os.path
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
model = joblib.load(model_path)


class TextInput(BaseModel):
    text: str


@app.post("/predict")
async def classify_text(text_input: TextInput):
    # TODO: Return the class proba
    prediction = str(model.predict([text_input.text])[0])

    return {"category": prediction}


@app.get("/health")
async def health():
    return "OK"
