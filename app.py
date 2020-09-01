from flask import Flask, Response, render_template, redirect
from flask_pymongo import PyMongo
# from bs4 import BeautifulSoup as bs
import scraper
import requests

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    # Run the scrape  function and save the results to a variable
    mars_data = scraper.scrape_all()

    # Update the Mongo database using update and upsert=True
    # mars_collection = mongo.db.mars
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
