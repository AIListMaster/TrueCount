# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""
import hashlib
import re


def string_to_md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def slugify(string):
    """
    Converts a string to a URL-friendly slug.

    Args:
        string (str): The string to convert.

    Returns:
        str: The slugified string.
    """

    # Convert the string to lowercase.
    string = string.lower()

    # Remove all non-alphanumeric characters.
    string = re.sub(r"[^\w\s-]", "", string)

    # Replace all spaces with hyphens.
    string = string.replace(" ", "-")

    # Remove any leading or trailing hyphens.
    string = string.strip("-")

    return str(string)
