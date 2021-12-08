from flask import Flask, render_template, redirect
import pymongo
import scrape_mars as sm

# create instance of Flask app
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars
facts = db.fact

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Return template and data
    return render_template("index.html", test="serving up some data")

# Route that will trigger the scrape function

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = sm.scrape_info()

    # Update the Mongo database using update and upsert=True
    #mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
