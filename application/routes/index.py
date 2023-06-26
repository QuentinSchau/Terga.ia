from flask import request

from application import app
from application.model.pytorchLightning.CallBacksLightning import CallBacksLightning


@app.route("/")
def index():
    return "Terga.ia project under GPL3 Licence see the git repo here : https://github.com/QuentinSchau/Terga.ia "

@app.route("/test")
def test():
    return "Test"