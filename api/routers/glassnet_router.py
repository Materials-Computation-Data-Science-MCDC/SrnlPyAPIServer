from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np
import itertools

from ..dependencies import get_glassnet_model


# Define a Pydantic model for the input data

class Composition(BaseModel):
    composition: Dict[str, List[int]]


router = APIRouter()


@router.post("/v2/api/glassnet/predict/")
async def predict_glassnet(composition: Composition, glassnet_model=Depends(get_glassnet_model)):
    try:
        predictions = glassnet_model.predict(composition.composition)  # Access the model and make predictions
        return {"status": "success", "data": {"composition": composition.composition, "predictions": predictions}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/v2/api/glassnet/predict/multi")
async def predict_glassnet_multi(compositions: List[Composition], glassnet_model=Depends(get_glassnet_model)):
    try:
        all_predictions = []
        for composition in compositions:
            samples = list(generate_compositions(composition.composition))
            for i in range(0, len(samples), 100):
                chunk = samples[i:i + 100]
                predictions = [{"composition": sample, "predictions": glassnet_model.predict(sample)} for sample in chunk]
                all_predictions.extend(predictions)
        return {"status": "success", "data": all_predictions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def generate_compositions(base_composition: Dict[str, List[int]], max_compositions: int = 100):
    keys = list(base_composition.keys())
    ranges = [base_composition[key][1] - base_composition[key][0] + 1 for key in keys]

    # Calculate an approximate number of samples per dimension to not exceed max_compositions
    num_samples = int(max_compositions ** (1 / len(ranges)))

    value_ranges = [np.linspace(base_composition[key][0], base_composition[key][1], num_samples, dtype=int).tolist() for key in keys]

    seen_compositions = set()
    compositions_generated = 0

    for values in itertools.product(*value_ranges):
        if compositions_generated >= max_compositions:
            break

        composition = dict(zip(keys, values))
        composition_tuple = tuple(sorted(composition.items()))  # Convert the dict to a tuple of sorted items for uniqueness

        if composition_tuple not in seen_compositions:
            seen_compositions.add(composition_tuple)
            compositions_generated += 1
            yield composition
