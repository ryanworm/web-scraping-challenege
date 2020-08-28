from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraper

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scraper")
def scraper():

    # Run the scrape function and save the results to a variable
    mars_scraped_dict = scraper.scrape_info()

    # Update the Mongo database using update and upsert=True
    mars_collection = mongo.db.mars
    title_text.update({}, mars_scraped_dict, upsert=True)

    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
