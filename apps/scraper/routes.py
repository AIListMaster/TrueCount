# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import asyncio
from apps.scraper import blueprint
from apps.scraper.scraper import scraper
from flask import request, jsonify, make_response


@blueprint.route('/analyse', methods=['POST'])
def analyse():
    # search_term = request.form['search_term']
    search_term = None
    if request.is_json:
        content = request.get_json()
        search_term = content['search_term']
    if search_term:
        business = asyncio.run(scraper(text=search_term))
        if business:
            # Access the columns of the record
            columns = {
                'id': business.id,
                'title': business.title,
                'address': business.address,
            }
            return make_response(jsonify(columns), 200)
    return make_response(jsonify({"message": "No items found"}), 404)
