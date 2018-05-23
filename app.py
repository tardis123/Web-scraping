# Dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape

# Create instance of Flask app
app = Flask(__name__)

# Connect to Mongo and initialize client
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

# Declare the database and collection
db = client.surf_summary
collection = db.surf_summary 

# Remove current data
if collection.count() > 0:
    collection.remove({})

# Create route that renders index.html template
@app.route("/")
def index():
    # Retrieve data from Mongo database
    items = collection.find()
    # Render data
    return render_template("index.html", items = items)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape_it():
    # Retrieve scraped data
    surf_data = scrape.zip_lists()
    # Loop through list and insert data into Mongo database
    for row in surf_data:
        collection.insert_one({'location': row[0],
                            'water_temp': row[4],
                            'air_temp': row[5],
                            'smallest_waves': row[2],
                            'biggest_waves': row[3],
                            'url_link': row[1]
                            }) 
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)