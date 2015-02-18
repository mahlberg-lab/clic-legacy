from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
from flask import Flask, render_template
from clic.web.api import api

app = Flask(__name__, static_url_path='')
app.register_blueprint(api, url_prefix='/api')

from clic.chapter_repository import ChapterRepository

'''
Application routes
'''
@app.route('/', methods=['GET'])
def index():
    return render_template("concordance-form.html")

@app.route('/concordances/', methods=['GET'])
def concordances():
    return render_template("concordance-results.html")

@app.route('/chapter/<book>/<int:number>/')
def chapterView(number, book):
    chapter_repository = ChapterRepository()
    chapter_raw = chapter_repository.get_chapter(number, book)
    return render_template("chapter-view.html", content=chapter_raw)