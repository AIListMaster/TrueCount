# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from apps.scraper.forms import ScraperForm

@blueprint.route('/')
def route_default():
    scarper_form = ScraperForm(request.form)
    return render_template('home/index.html', form=scarper_form, test="From BE")