from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def root:
	return redirect(url_for("splash"))

@app.route("/splash")
def splash:
	return render_template("splash.html")

@app.route("/login", methods=["POST"])
def login:
	

@app.route("/profile")
def profile:

@app.route("/profile/edit", methods=["POST"])
def profedit:

@app.route("/connect")
def connect:

@app.route("/message")
def msg:
