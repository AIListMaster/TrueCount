# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
from apps import db
from apps.utils.utils import string_to_md5
from datetime import datetime


class Business(db.Model):
    __tablename__ = 'Business'

    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    created = db.Column(db.Date, default=datetime.utcnow)
    updated = db.Column(db.Date, default=datetime.utcnow)

    def __init__(self, title, address, image=None):
        self.id = string_to_md5(title)
        self.title = title
        self.address = address
        self.image = image

    def create(self):
        new_business = Business(self.title, self.address, self.image)
        db.session.add(new_business)
        db.session.commit()
        return new_business

    def update(self):
        new_business = Business.query.filter_by(id=self)
        if new_business:
            self.title = new_business[0].title
            self.address = new_business[0].address
            self.address = new_business[0].image
            db.session.commit()
            return True

    def __repr__(self):
        return str(self.id)
