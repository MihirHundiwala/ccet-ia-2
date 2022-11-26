from flask import Blueprint, render_template

Facts = Blueprint("Facts", __name__, static_folder="static",
                  template_folder="templates", static_url_path='/%s' % __name__)


@Facts.route('/facts')
def facts():
    return render_template('facts.html')