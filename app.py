from flask import Flask, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Listing


@app.route("/", methods=['GET'])
def index():
    new_listings = db.session.query(Listing) \
        .filter(Listing.status == "NEW") \
        .order_by(Listing.scraped_dt)
    int_listings = db.session.query(Listing) \
        .filter(Listing.status == "INTERESTED") \
        .order_by(Listing.scraped_dt)
    app_listings = db.session.query(Listing) \
        .filter(Listing.status == "APPLIED") \
        .order_by(Listing.scraped_dt)
    intv_listings = db.session.query(Listing) \
        .filter(Listing.status == "INTERVIEW") \
        .order_by(Listing.scraped_dt)
    off_listings = db.session.query(Listing) \
        .filter(Listing.status == "OFFER") \
        .order_by(Listing.scraped_dt)
    mbl_listings = db.session.query(Listing) \
        .filter(Listing.status == "LATER") \
        .order_by(Listing.scraped_dt)
    return render_template('index.html', listings={
                           "NEW": new_listings,
                           "INTERESTED": int_listings,
                           "APPLIED": app_listings,
                           "INTERVIEW": intv_listings,
                           "OFFER": off_listings,
                           "LATER": mbl_listings})


@app.route("/update-status", methods=['POST'])
def update_status():
    """
    A view that receives a listing to change the status of and
    return the datetime of the Listing to insertBefore
    """
    # Grab listing and new status
    listing = db.session.query(Listing).get(request.form['id_num'])
    status = request.form['status']
    # Grab new Listing list
    listings = db.session.query(Listing) \
        .filter(Listing.status == status) \
        .order_by(Listing.scraped_dt)
    # Set new status and commit change
    listing.status = status
    db.session.commit()
    # Find next listing in order by scraped datetime
    # Return as a string if it exists
    for l in listings:
        if(l.scraped_dt > listing.scraped_dt):
            return str(l.scraped_dt)
    return make_response("")

if __name__ == "__main__":
    app.run()
