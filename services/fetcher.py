import requests

def fetch_uuid():
    try:
        response = requests.get(
            "https://httpbin.org/uuid",
            timeout=5
        )
        response.raise_for_status()
        return response.json()["uuid"]
    except requests.exceptions.Timeout:
        raise Exception("Timeout while fetching UUID")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected fetch error: {str(e)}")
