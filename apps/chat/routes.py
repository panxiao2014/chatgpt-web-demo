from apps.chat import blueprint
from apps.chat.chatGptDavinci import chatResponseFromDavinci
from apps.chat.chatGptTurbo import chatResponseFromTurbo
from flask import render_template, request
from flask import current_app as app
from flask_login import login_required
from jinja2 import TemplateNotFound

from flask_login import (
    current_user
)

@blueprint.route('/userQuestion', methods=['GET', 'POST'])
@login_required
def userQuestion():
    currentUser = current_user.username
    formData = request.get_json()
    inputText = formData.get('inputText')
    app.logger.info("%s ask: %s" % (currentUser, inputText))

    #use text-davinci-003
    #return chatResponseFromDavinci(currentUser, inputText)

    #use gpt-3.5-turbo:
    return chatResponseFromTurbo(currentUser, inputText)