from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as sm

#1. Open using integrated terminal
#2. python app.py

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
#mongo = PyMongo(app)

# Or set inline
mongo_database_name = "mars_app"
mongo = PyMongo(app, uri=f"mongodb://localhost:27017/{mongo_database_name}")

#root route
@app.route("/")
def index():
    mars_facts = mongo.db.mars_facts.find_one()
    return render_template("index.html", mars_facts=mars_facts)

@app.route("/scrape")
def scraper():
    mars_facts     = mongo.db.mars_facts
    mars_fact_data = sm.scrape()
    mars_facts.update_many({}, {"$set": mars_fact_data}, upsert=True) 
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True) 