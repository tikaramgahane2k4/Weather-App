from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Default city shown when geolocation isn't available or is denied
DEFAULT_CITY = "London"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = ""

    if request.method == "POST":
        # prefer lat/lon when provided (device geolocation)
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        if lat and lon:
            api_key = "fcf4718174b4b190a2bbc4d42da0c7c8"
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                city = weather_data.get("name", "")
            else:
                weather_data = {"error": "Location not found!"}
        else:
            # fallback to city name from the form
            city = request.form.get("city", "").strip()
            if city:
                api_key = "fcf4718174b4b190a2bbc4d42da0c7c8"
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                if response.status_code == 200:
                    weather_data = response.json()
                else:
                    weather_data = {"error": "City not found!"}

    # On GET we don't force a default; the client will try geolocation and POST back.
    return render_template("index.html", data=weather_data, city=city, default_city=DEFAULT_CITY)

if __name__ == "__main__":
    app.run(debug=True)

