from fastapi import FastAPI, Path, HTTPException
import requests
from typing import Dict

app = FastAPI(
    title="AIS Seafreight API",
    description="Backend to fetch AIS data from MarineTraffic",
    version="0.1.0"
)

# Beispiel-API-Key (ersetzen!)
API_KEY = "your_marinetraffic_api_key"

@app.get("/vessels/{imo}/position")
def get_current_position(imo: int = Path(..., description="IMO number of the vessel")) -> Dict:
    try:
        url = f"https://services.marinetraffic.com/api/exportvesseltrack/v:2/{API_KEY}/timespan:60/protocol:jsono/imo:{imo}"
        response = requests.get(url)
        data = response.json()

        if not data:
            raise HTTPException(status_code=404, detail="No position data found")

        last_point = data[-1]  # Latest point

        return {
            "imo": imo,
            "latitude": last_point.get("LAT"),
            "longitude": last_point.get("LON"),
            "timestamp": last_point.get("TIMESTAMP")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vessels/{imo}/distance-to-port")
def get_distance_to_next_port(imo: int = Path(..., description="IMO number of the vessel")) -> Dict:
    try:
        # Simuliert: In echtem Fall müsstest du Hafenkoordinaten und ETA auslesen
        # Hier nehmen wir z. B. Hamburg als Zielhafen (lat, lon)
        target_port = {"name": "Hamburg", "lat": 53.5461, "lon": 9.9661}

        # Hole aktuelle Position
        pos = get_current_position(imo)

        from geopy.distance import geodesic
        distance = geodesic(
            (pos["latitude"], pos["longitude"]),
            (target_port["lat"], target_port["lon"])
        ).nautical

        return {
            "imo": imo,
            "from_position": {"lat": pos["latitude"], "lon": pos["longitude"]},
            "to_port": target_port,
            "distance_nm": round(distance, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))