# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""

from apps.home import blueprint
from flask import render_template, request
from apps.scraper.forms import ScraperForm
from apps.scraper.models import Business, Reviews
from sqlalchemy import create_engine, Column, Integer, String, select, func


@blueprint.route('/')
def route_default():
    items = []
    scarper_form = ScraperForm(request.form)
    businesses = Business.query.limit(20).all()
    if businesses:
        items = [i.serialize for i in businesses]

    return render_template('home/index.html', form=scarper_form, items=items)


@blueprint.route('/business/<string:business_id>', methods=['GET'])
def route_business(business_id):
    business = Business.query.filter_by(id=business_id).first_or_404(description="Business not found")

    # Initialize vars
    overall_rating = 0

    # Calculate review.
    review_details = Reviews.query.with_entities(func.sum(Reviews.sentiment), func.count(Reviews.sentiment)).filter_by(
        business_id=business_id).all()

    # Extract review.
    if review_details[0]:
        sum, total = review_details[0]
        if sum and total:
            overall_rating = (sum / (total * 2)) * 100
            overall_rating = round(overall_rating, 2)

    item = []
    if business:
        item = business.serialize

    return render_template('home/business.html', item=item, overall_rating=overall_rating)
