from application import app
from application.auth import token_required

@app.route("/")
def index():
    return "Terga.ia project under GPL3 Licence see the git repo here : https://github.com/QuentinSchau/Terga.ia "

@app.route("/test")
@token_required
def test():
    return "Test"