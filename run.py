from dotenv import load_dotenv
load_dotenv()

from app import create_app
from prometheus_client import generate_latest
from flask import Response


app = create_app()
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)