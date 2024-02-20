# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.truecount import blueprint
from flask import render_template, request
from flask_login import login_required
from apps.truecount.places_api import PlacesAPI

@blueprint.route('/curatedata',  methods=['GET', 'POST'])
def curatedata():
    test_data = "Test Data"
    api = PlacesAPI()
    data = api.get_places('30.642786,76.854799', 1000)
    print(data)
    return render_template('truecount/collector.html', data=test_data)

