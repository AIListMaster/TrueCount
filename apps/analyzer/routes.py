# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
import asyncio
from apps.analyzer import blueprint
from flask import request, jsonify, make_response
from apps.utils.batch import batch_processing
from apps.scraper.models import Reviews


@blueprint.route('/batch')
def batch():
    reviews = Reviews.query.filter(Reviews.sentiment.is_(None)).all()

    # Specify the batch size
    batch_size = 5

    # Perform batch processing
    batch_processing(reviews, batch_size)

    return make_response(jsonify({"message": "No items found"}), 404)
