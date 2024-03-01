# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
from apps import db
from datetime import datetime


class Business(db.Model):
    __tablename__ = 'Business'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(20), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    reviews = db.relationship('Reviews', backref='Business', lazy=True)
    slug = db.Column(db.String(255), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, business_id, title, address=None, website=None, phone=None, category=None, image=None,
                 slug=None):
        self.business_id = business_id
        self.title = title
        self.address = address
        self.website = website
        self.phone = phone
        self.category = category
        self.image = image
        self.slug = slug

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'business_id': str(self.business_id),
            'title': str(self.title),
            'address': str(self.address),
            'website': str(self.website),
            'phone': str(self.phone),
            'category': str(self.category),
            'image': str(self.image),
            'slug': str(self.slug),
            'created': str(self.created.strftime('%B %d, %Y')),
            'updated': str(self.updated.strftime('%B %d, %Y')),
            'reviews': [i.serialize for i in self.reviews]
        }

    def create(self):
        business = Business(self.business_id, self.title, self.address, self.website, self.phone, self.category,
                            self.image, self.slug)
        db.session.add(business)
        db.session.commit()
        return business

    def update(self):
        business = Business.query.filter_by(business_id=self.business_id).first()
        if business:
            business.title = self.title
            business.address = self.address
            business.website = self.website
            business.phone = self.phone
            business.category = self.category
            business.image = self.image
            business.slug = self.slug
            db.session.commit()
            return business
        return False

    def exist(self):
        business = Business.query.filter_by(business_id=str(self.business_id)).first()
        return business is not None

    def __repr__(self):
        return str(self.id)


class Reviews(db.Model):
    __tablename__ = 'Reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column(db.String(100), nullable=False)
    contributor_name = db.Column(db.String(30), nullable=True)
    contributor_id = db.Column(db.String(100), nullable=True)
    contributor_pic = db.Column(db.String(255), nullable=True)
    review = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=False)
    rmap = db.Column(db.Integer, nullable=False)
    sentiment = db.Column(db.Integer, nullable=True)
    business_id = db.Column(db.Integer, db.ForeignKey('Business.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self,
                 review_id,
                 business_id,
                 rating, rmap,
                 sentiment=None,
                 contributor_name=None,
                 contributor_id=None,
                 contributor_pic=None,
                 review=None):
        self.review_id = review_id
        self.business_id = business_id
        self.contributor_name = contributor_name
        self.contributor_id = contributor_id
        self.contributor_pic = contributor_pic
        self.review = review
        self.rating = rating
        self.rmap = rmap
        self.sentiment = sentiment

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'review_id': str(self.review_id),
            'business_id': str(self.business_id),
            'contributor_name': str(self.contributor_name),
            'contributor_id': str(self.contributor_id),
            'contributor_pic': str(self.contributor_pic),
            'review': str(self.review),
            'rating': str(self.rating),
            'rmap': str(self.rmap),
            'sentiment': str(self.sentiment),
            'created': str(self.created.strftime('%B %d, %Y')),
            'updated': str(self.updated.strftime('%B %d, %Y'))
        }

    def create(self):
        review = Reviews(self.review_id,
                         self.business_id,
                         self.rating,
                         self.rmap,
                         self.sentiment,
                         self.contributor_name,
                         self.contributor_id,
                         self.contributor_pic,
                         self.review)
        db.session.add(review)
        db.session.commit()
        return review

    def update(self):
        review = Reviews.query.filter_by(review_id=self.review_id).first()
        if review is not None:
            review.contributor_name = self.contributor_name
            review.contributor_id = self.contributor_id
            review.contributor_pic = self.contributor_pic
            review.review = self.review
            review.rating = self.rating
            review.rmap = self.rmap
            review.sentiment = self.sentiment
            db.session.commit()
            return review
        return False

    def exist(self):
        review = Reviews.query.filter_by(review_id=self.review_id).first()
        return review is not None

    def __repr__(self):
        return str(self.id)
