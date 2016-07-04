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
    return render_template('index.html',
                           new_listings=new_listings,
                           int_listings=int_listings)


@app.route("/update-status", methods=['POST'])
def update_status():
    listing = db.session.query(Listing).get(request.form['id_num'])
    listing.status = request.form['status']
    db.session.commit()
    return make_response("Status Updated")

if __name__ == "__main__":
    app.run()
