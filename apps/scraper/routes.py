# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import asyncio
from apps.scraper import blueprint
from apps.scraper.scraper import scraper
from flask import redirect, request, url_for


@blueprint.route('/scrap',  methods=['POST'])
def scrap():
    search_term = request.form['search_term']
    if search_term:
        asyncio.run(scraper(text=search_term))

    return redirect(url_for('truecount_blueprint.curatedata'))
