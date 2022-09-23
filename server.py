import os
import constants
import logging
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request, redirect, url_for, abort, session


def create_app(testing=False):
    app = Flask(__name__)
    CORS(app)

    if __name__ != '__main__': 
        # Init logging, promethius, gunicorn things here...
        pass
        
    
    ### Error Handling Endpoints ###

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html', message=error.description.get('message', ''), title=error.description.get('title', 'Forbidden'))

    @app.errorhandler(401)
    def unauthorized(error):
        url_redirect = session.get('url_redirect', '/')
        session['message'] = error.description.get('message', '')
        return redirect(url_for('sign_in'))  # Need to find a way to pass the url_redirect into here
        # return render_template('sign-in.html', message=error.description['message'], url_redirect=url_redirect)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error.html', message=error.description.get('message', ''), title=error.description.get('title', '404'))


    ### MAIN ROUTES ###
    @app.route(constants.MAIN_HOME_URL)
    # @token_required
    def main_home():
        return redirect(f'/{get_user_default_app(session["username"])}')

    @app.route(constants.HOME_URL)
    # @token_required
    @app_access
    def home(app_name):
        if app_name in constants.APP_NAMES:
            return render_template('home.html', app_data=get_app_data(app_name))
        else:
            return abort(404, {'message': 'Page Not Found'})


    return app


# This is only for local debugging. The flask server (app.run()) is not suitable for production.
if __name__ == '__main__':
    prodigy_app = create_app(True)
    # prodigy_app.run(host='0.0.0.0', port=8080, debug=True)
    prodigy_app.run(host='0.0.0.0', port=8080)
