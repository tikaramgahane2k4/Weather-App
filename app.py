from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        api_key = "fcf4718174b4b190a2bbc4d42da0c7c8" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            weather_data = {"error": "City not found!"}

    return render_template("index.html", data = weather_data)

if __name__ == "__main__":
    app.run(debug=True)

