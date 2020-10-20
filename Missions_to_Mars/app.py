# MongoDB and Flask Application

# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Flask Setup
app = Flask(__name__)

# PyMongo Connection Setup
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def home():
    mars = list(db.mars.find())
    print(mars)
    return render_template("index.html", mars = mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = scrape_mars.scrape()
    print("\n\n\n")
    
    db.mars_facts.insert_one(mars)
    return "Some scrapped data"

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)

