# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.admin import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/index.html')


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#     try:
#
#         if not template.endswith('.html'):
#             template += '.html'
#
#         # Detect the current page
#         segment = get_segment(request)
#
#         # Serve the file (if exists) from app/templates/admin/FILE.html
#         return render_template("admin/" + template, segment=segment)
#
#     except TemplateNotFound:
#         return render_template('admin/page-404.html'), 404
#
#     except:
#         return render_template('admin/page-500.html'), 500
#
#
# # Helper - Extract current page name from request
# def get_segment(request):
#     try:
#
#         segment = request.path.split('/')[-1]
#
#         if segment == '':
#             segment = 'index'
#
#         return segment
#
#     except:
#         return None
