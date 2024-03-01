# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from apps.scraper.forms import ScraperForm
from apps.scraper.models import Business
from apps.utils.analyzer import SentimentAnalyzer


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
    item = []
    if business:
        item = business.serialize
    # reviews = []
    # for index, review in enumerate(business.reviews):
    #     analyzer = SentimentAnalyzer()
    #     reviews.append(analyzer.predict(review.review))

    return render_template('home/business.html', item=item, reviews=[])
