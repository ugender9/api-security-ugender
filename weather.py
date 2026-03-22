import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env (kept out of source control)
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, timeout: float = 5.0) -> str:
    if not API_KEY:
        raise ValueError("API key not found. Set it in .env file or environment variables.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=timeout)

        # Rate limiting
        if response.status_code == 429:
            return "Error: Too many requests. Please try again later."

        # Other non-success statuses
        if response.status_code != 200:
            try:
                err = response.json()
                msg = err.get("message", "")
            except ValueError:
                msg = response.text
            return f"Error: Unable to fetch weather (Status Code: {response.status_code}) {msg}".strip()

        data = response.json()

        # Safe parsing
        temp = data.get("main", {}).get("temp")
        weather = data.get("weather", [{}])[0].get("description")

        if temp is None or weather is None:
            return "Error: Unexpected response format from weather API."

        return f"Temperature: {temp}°C, Condition: {weather}"

    except requests.exceptions.RequestException:
        return "Error: Network issue. Please check your connection."


if __name__ == "__main__":
    city = input("Enter city name: ")

    # Privacy: do not log or persist city/location without explicit consent.

    result = get_weather(city)
    print(result)
