from flask import Flask, render_template
import os

app = Flask(__name__)

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")

@app.route("/")
def index():
	return render_template("test.html")


if __name__ == "__main__":
	app.run(debug=True)