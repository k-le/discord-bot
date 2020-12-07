"""File contains methods that will ease the process of working
with HTTP requests and HTML code and files.
"""

import json
import requests

def save_html(html, path):
    """To save HTML code as a local file to avoid sending an HTTP request
    every time HTML code needs to be parsed.

    :parameter
    -----------
    html: :class:`Str`
        HTML-like object for writing to a file.
    path: :class:`Str`
        Local file path for saving.
    """

    with open(path, 'wb') as file:
        file.write(html)

def load_html(path):
    """To open a local file containing HTML code and
    avoid sending an HTTP request.

    :parameter
    -----------
    path: :class:`Str`
        Local file path that contains the text file.

    :return
    --------
    :class:`Str`
        The local file that contains HTML code.
    """

    with open(path, 'rb') as file:
        return file.read()

def check_isfile(file_path, search_url=''):
    """Checks if a file exists, writes a new file if one does not exist.

    Utilizes save_html() and load_html() to check if a local file exists.

    This method is meant to avoid re-writing the same lines of code for
    checking, writing, and loading local files that contain HTML code.

    :parameter
    -----------
    search_url: :class:`Str`
        URL/website to send an HTTP request and parse HTML data from.
    file_path: :class:`Str`
        Local file path for either saving or loading the text file.

    :return
    --------
    :class:`Str`
        HTML-like object.
    """

    if file_path.is_file():
        html = load_html(file_path)
        print('loaded')
    else:
        r = requests.get(search_url)
        html = r.content
        save_html(html, file_path)
        print('saved')

    return html








