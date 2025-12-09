from flask import Flask, render_template, request
import json

with open("config.json","r", encoding="utf-8") as file:
    data = json.load(file)
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        title = request.form['title']
        SSID = request.form['ssid-title']
        PASSWORD = request.form['password-title']
        hource = request.form['hource-title']
        minuts = request.form['minuts-title']
        email = request.form['email-title']
        data["language"] = title
        data["hourc"] = hource
        data["minut"] = minuts
        data["email"] = email
        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(data, file)
            exit()
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)