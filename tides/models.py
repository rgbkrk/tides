from pydantic import BaseModel, Field
from typing import List


class TideRequest(BaseModel):
    station: str = Field(
        ...,
        description="NOAA station ID",
        example="9414290",
    )
    range_hours: int = 24
    begin_date: str = "today"


# Define the Pydantic model for individual tide predictions
class TidePrediction(BaseModel):
    t: str = Field(
        ...,
        description="Time of the prediction",
        example="2021-07-01 00:00",
    )
    v: str  # Tide level in feet
    type: str  # Type of tide (High or Low)


class TideResponse(BaseModel):
    predictions: List[TidePrediction]
    station: str

    @classmethod
    def from_noaa_api(cls, station: str, response: dict) -> "TideResponse":
        # Parse the response JSON and return the tide data
        tide_data = cls(
            station=station,
            predictions=[
                TidePrediction(
                    t=prediction["t"], v=prediction["v"], type=prediction["type"]
                )
                for prediction in response["predictions"]
            ],
        )
        return tide_data
