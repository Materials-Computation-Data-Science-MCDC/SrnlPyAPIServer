from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import get_viscnet_model


# Define a Pydantic model for the input data
class ViscosityPredictionRequest(BaseModel):
    temperature: float
    composition: str


router = APIRouter()


@router.post("/viscnet/predict/")
async def predict_viscnet(prediction_request: ViscosityPredictionRequest, viscnet_model=Depends(get_viscnet_model)):
    viscosity = viscnet_model.predict(T=prediction_request.temperature,
                                      composition=prediction_request.composition)
    return {"log10_viscosity": viscosity}
