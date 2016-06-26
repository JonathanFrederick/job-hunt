from app import db
from sqlalchemy.dialects.postgresql import JSON


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    company = db.Column(db.String())
    title = db.Column(db.String())

    def __init__(self, url, company, title):
        self.url = url
        self.company = company
        self.title = title

    def __repr__(self):
        return '{} : {}'.format(self.company, self.title)
