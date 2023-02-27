# GNU AGPL v3 License
# Written by John Nunley
# Web Application Root

from flask import Flask, render_template, g, request

import atexit
import os

from . import apk_processor
from . import db

import enum

from apscheduler.schedulers.background import BackgroundScheduler

from .process_data import get_results, app_data

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16),
        DATABASE=os.path.join(app.instance_path, 'webapp.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Set up a task scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.extensions["scheduler"] = scheduler

    # The homepage, at /
    @app.route('/')
    def index():
        results = get_results()
        return render_template('homepage.html', results=results)

    # The search page, at /search
    @app.route('/search')
    def search():
        search = request.args.get('q')
        results = get_results(search)
        return render_template('search.html', results=results)

    # The app page, at /app/<id>
    @app.route('/app/<id>')
    def app_print(id):
        data = app_data(id)
        return render_template('app.html', data=data)
    
    return app
