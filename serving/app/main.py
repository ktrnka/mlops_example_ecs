import joblib
import os.path
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
model = joblib.load(model_path)


class TextInput(BaseModel):
    """Basic input to the classifier"""
    text: str


class ClassificationOutput(BaseModel):
    """Multiclass prediction output"""
    category: str
    probability: float


@app.post("/predict", response_model=ClassificationOutput)
async def classify_text(text_input: TextInput) -> ClassificationOutput:
    prediction = str(model.predict([text_input.text])[0])
    probability = float(max(model.predict_proba([text_input.text])[0]))

    response = ClassificationOutput(
        category=prediction,
        probability=probability
    )

    return response


@app.get("/health")
async def health():
    return "OK"
