# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.truecount import blueprint
from flask import render_template, request
from flask_login import login_required
from apps.truecount.forms import ScraperForm


@blueprint.route('/curatedata', methods=['GET', 'POST'])
def curatedata():
    test_data = "Test Data"
    scarper_form = ScraperForm(request.form)
    return render_template('truecount/collector.html',
                           data=test_data
                           , form=scarper_form)
