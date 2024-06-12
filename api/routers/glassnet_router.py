from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..dependencies import get_glassnet_model


# Define a Pydantic model for the input data

class Composition(BaseModel):
    composition: str


router = APIRouter()


@router.post("/api/glassnet/predict/")
async def predict_glassnet(composition: Composition, glassnet_model=Depends(get_glassnet_model)):
    try:
        predictions = glassnet_model.predict(composition.composition)  # Access the model and make predictions
        return {"status": "success", "data": predictions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
