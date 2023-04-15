from apps.webroot import blueprint

from flask import request
from flask import current_app as app
from jinja2 import TemplateNotFound

from flask_login import (
    current_user
)

@blueprint.route('/webroot', methods=['GET', 'POST'])
def webrootAccess():
    return "You are in webroot"