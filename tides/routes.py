from fastapi import APIRouter, HTTPException
import httpx
from datetime import datetime, timedelta

from tides.models import TideRequest, TideResponse

router = APIRouter()

# Define the NOAA API URL
NOAA_API_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"


@router.get("/api/tides")
async def get_tide_data(request: TideRequest) -> TideResponse:
    print("ok then", request)
    if request.begin_date == "today":
        begin_date = datetime.utcnow().strftime("%Y%m%d")
    else:
        begin_date = request.begin_date

    end_date = (
        datetime.strptime(begin_date, "%Y%m%d") + timedelta(hours=request.range_hours)
    ).strftime("%Y%m%d")

    station = request.station

    # Define the parameters for the NOAA API request
    params = {
        "begin_date": begin_date,
        "end_date": end_date,
        "station": station,
        "product": "predictions",
        "datum": "MLLW",
        "time_zone": "lst_ldt",
        "units": "english",
        "interval": "hilo",
        "format": "json",
        "application": "web_services",
    }

    # Make the request to the NOAA API
    async with httpx.AsyncClient() as client:
        response = await client.get(NOAA_API_URL, params=params)

    # Check for errors in the response
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return TideResponse.from_noaa_api(station, response.json())
