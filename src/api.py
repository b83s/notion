#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

from notion_api import appendToCurrentDayNotes, tasksDatabase, photoDatabase
from config import importedTagURL

from flask import Flask, request
app = Flask(__name__)


@app.route('/add_note')
def add_note():
    try:
        note = request.args.get('title')

        appendToCurrentDayNotes(note)

        return 'Succeceed in adding note', 200
    except Exception:
        return 'Failed in adding note', 500


@app.route('/add_task')
def add_task():
    try:
        task = request.args.get('title')
        url = request.args.get('url')

        collection = tasksDatabase().collection
        row = collection.add_row()
        row.name = task
        row.status = 'Inbox'
        row.url = url

        return 'Succeceed in adding task', 200
    except Exception:
        return 'Failed in adding task', 500


@app.route('/add_photo')
def add_photo():
    try:
        task = request.args.get('title')
        url = request.args.get('url')

        collection = tasksDatabase().collection
        row = collection.add_row()
        row.name = task
        row.status = 'Inbox'
        row.photo = url

        return 'Succeceed in adding photo', 200
    except Exception:
        return 'Failed in adding photo', 500


@app.route('/add_photojournal')
def add_photojournal():
    try:
        task = request.args.get('title')
        url = request.args.get('url')

        collection = photoDatabase().collection
        row = collection.add_row()
        row.name = task
        row.photo = url

        return 'Succeceed in adding photo', 200
    except Exception:
        return 'Failed in adding photo', 500

if __name__ == '__main__':
    app.run()
