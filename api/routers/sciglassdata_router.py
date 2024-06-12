import pandas as pd
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
from ..services.sci_glass import sci_glass_service

router = APIRouter()

# Define a Pydantic model for pagination
class PaginationParams(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 100
    properties: Optional[str] = None
# API to load and return glass data with pagination

@router.get("/v2/api/sciglass/data/")
async def get_sciglass_data(pagination: PaginationParams = Depends()):
    df = sci_glass_service.get_data()  # Load the data into a DataFrame

    # Check if DataFrame is empty
    if df.empty:
        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": 0,
            "data": {
                "elements": [],
                "properties": [],
                "metadata": []
            }
        }

    # Calculate pagination details
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page

    # Separate the DataFrame into elements, properties, and metadata
    elements_df = df["elements"].iloc[start:end]
    properties_df = df["property"].iloc[start:end]
    metadata_df = df["metadata"].iloc[start:end]

    # Replace NaN and infinite values with None
    elements_df = elements_df.replace([np.inf, -np.inf], np.nan).fillna(value=np.nan).replace({np.nan: None})
    properties_df = properties_df.replace([np.inf, -np.inf], np.nan).fillna(value=np.nan).replace({np.nan: None})
    metadata_df = metadata_df.replace([np.inf, -np.inf], np.nan).fillna(value=np.nan).replace({np.nan: None})


    # Convert the paginated data to dictionaries (suitable for JSON response)
    elements_data = elements_df.reset_index().to_dict(orient="records")
    properties_data = properties_df.reset_index().to_dict(orient="records")
    metadata_data = metadata_df.reset_index().to_dict(orient="records")

    # Return the paginated data in separate groups
    # Return the paginated data in separate groups under the 'data' key
    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": len(df),
        "data": {
            "elements": elements_data,
            "properties": properties_data,
            "metadata": metadata_data
        }
    }

# You can include more API endpoints or logic as needed
