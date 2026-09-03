import requests


def get_terrain(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/elevation"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
    )

    try:

        response = requests.get(url, timeout=10)

        data = response.json()

        elevation = data["elevation"][0]

        return {
            "elevation": elevation
        }

    except Exception:

        return None