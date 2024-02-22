# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


# Scraper form.

class ScraperForm(FlaskForm):
    search_term = StringField('Search Term',
                              id="search_term",
                              validators=[DataRequired()])
