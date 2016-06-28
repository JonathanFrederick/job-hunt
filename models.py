from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    company = db.Column(db.String(32))
    title = db.Column(db.String(128))
    status = db.Column(db.String(10))

    def __init__(self, url, company, title):
        self.url = url
        self.company = company
        self.title = title
        self.status = "NEW"
        self.scraped_dt = datetime()

    def __repr__(self):
        return '{} : {}'.format(self.company, self.title)
