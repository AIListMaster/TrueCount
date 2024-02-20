# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
import hashlib
from apps import db


class Business(db.Model):
    __tablename__ = 'Business'

    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)

    def __init__(self, title, address):
        self.id = hashlib.md5(title.encode()).hexdigest()
        self.title = title
        self.address = address

    def create(self):
        new_business = Business(self.title, self.address)
        db.session.add(new_business)
        db.session.commit()

    def update(self):
        new_business = Business.query.filter_by(id=self)
        if new_business:
            self.title = new_business[0].title
            self.address = new_business[0].address
            db.session.commit()
            return True

    def __repr__(self):
        return str(self.id)