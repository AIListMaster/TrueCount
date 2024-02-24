# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
import hashlib

def string_to_md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()