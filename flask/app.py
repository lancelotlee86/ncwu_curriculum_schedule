from flask import Flask

from func_with_database import func_getCrowdednessRateByPosition

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getCrowdednessRateByPosition/<position>")
def getCrowdednessRateByPosition(position):
    result = func_getCrowdednessRateByPosition(position)
    return str(result)

if __name__ == "__main__":
    app.run()
