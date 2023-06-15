from application import app

@app.route("/")
def index():
    return "Terga.ia project under GPL3 Licence see the git repo here : https://github.com/QuentinSchau/Terga.ia "

