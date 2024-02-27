# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
from apps import db
from datetime import datetime


class Business(db.Model):
    __tablename__ = 'Business'

    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(20), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    reviews = db.relationship('Reviews', backref='Business', lazy=True)
    created = db.Column(db.Date, default=datetime.utcnow())
    updated = db.Column(db.Date, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, id, title, address=None, website=None, phone=None, category=None, image=None):
        self.id = id
        self.title = title
        self.address = address
        self.website = website
        self.phone = phone
        self.category = category
        self.image = image

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self),
            'title': str(self.title),
            'address': str(self.address),
            'website': str(self.website),
            'phone': str(self.phone),
            'category': str(self.category),
            'image': str(self.image),
            'created': str(self.created.strftime('%B %d, %Y')),
            'updated': str(self.updated.strftime('%B %d, %Y')),
            'reviews': [i.serialize for i in self.reviews]
        }

    def create(self):
        business = Business(self.id, self.title, self.address, self.website, self.phone, self.category, self.image)
        db.session.add(business)
        db.session.commit()
        return business

    def update(self):
        business = Business.query.filter_by(id=self.id).first()
        if business:
            business.title = self.title
            business.address = self.address
            business.website = self.website
            business.phone = self.phone
            business.category = self.category
            business.image = self.image
            db.session.commit()
            return business
        return False

    def exist(self):
        business = Business.query.filter_by(id=str(self.id)).first()
        return business is not None

    def __repr__(self):
        return str(self.id)


class Reviews(db.Model):
    __tablename__ = 'Reviews'

    id = db.Column(db.String(100), primary_key=True)
    contributor_name = db.Column(db.String(30), nullable=True)
    contributor_id = db.Column(db.String(100), nullable=True)
    review = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=False)
    sentiment = db.Column(db.Integer, nullable=False)
    business_id = db.Column(db.String(100), db.ForeignKey('Business.id'), nullable=False)
    created = db.Column(db.Date, default=datetime.utcnow())
    updated = db.Column(db.Date, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, id, business_id, rating, sentiment, contributor_name=None, contributor_id=None, review=None):
        self.id = id
        self.business_id = business_id
        self.contributor_name = contributor_name
        self.contributor_id = contributor_id
        self.review = review
        self.rating = rating
        self.sentiment = sentiment

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'business_id': str(self.business_id),
            'contributor_name': str(self.contributor_name),
            'contributor_id': str(self.contributor_id),
            'review': str(self.review),
            'rating': str(self.rating),
            'sentiment': str(self.sentiment),
            'created': str(self.created.strftime('%B %d, %Y')),
            'updated': str(self.updated.strftime('%B %d, %Y'))
        }

    def create(self):
        review = Reviews(self.id, self.business_id, self.rating, self.sentiment, self.contributor_name,
                         self.contributor_id, self.review)
        db.session.add(review)
        db.session.commit()
        return review

    def update(self):
        review = Reviews.query.filter_by(id=self.id).first()
        if review is not None:
            review.contributor_name = self.contributor_name
            review.contributor_id = self.contributor_id
            review.review = self.review
            review.rating = self.rating
            review.sentiment = self.sentiment
            db.session.commit()
            return review
        return False

    def exist(self):
        review = Reviews.query.filter_by(id=self.id).first()
        return review is not None

    def __repr__(self):
        return str(self.id)
