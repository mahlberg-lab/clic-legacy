from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
import os

from flask import Flask, render_template, url_for, redirect, request
from werkzeug import secure_filename

from clic.web.api import api, fetchClusters, fetchKeywords
from clic.chapter_repository import ChapterRepository
from forms import SubsetForm, BOOKS, SUBSETS

app = Flask(__name__, static_url_path='')
app.register_blueprint(api, url_prefix='/api')

#TODO delete:
# from flask_debugtoolbar import DebugToolbarExtension
# app.debug = True
# app.config["SECRET_KEY"] = "jadajajada"
# toolbar = DebugToolbarExtension(app)

'''
Application routes
'''

#==============================================================================
# Home, about, docs, 404
#==============================================================================
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('concordances')) # current home page. may change

@app.route('/about/', methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/documentation/', methods=['GET'])
def documentation():
    return render_template("documentation.html")

#==============================================================================
# Concordances
#========================================request.method == 'POST' and ======================================
@app.route('/concordances/', methods=['GET'])
def concordances():
    if 'terms' in request.args.keys(): # form was submitted
        return render_template("concordance-results.html")
    else:
        return render_template("concordance-form.html")

#==============================================================================
# Keywords
#==============================================================================
@app.route('/keywords/', methods=['GET'])
def keywords():
    if 'testIdxGroup' in request.args.keys(): # form was submitted

        # get parameters for redirecting to the concordance page
        IdxGroup = request.args.get('testIdxGroup')
        testCollection = request.args.get('testCollection')
        testIdxMod = request.args.get('testIdxMod')
        selectWords = "whole"

        args = request.args
        keywords_result = fetchKeywords(args)

        return render_template("keywords-results.html",
                               IdxGroup=IdxGroup,
                               testCollection=testCollection,
                               testIdxMod=testIdxMod,
                               selectWords=selectWords,
                               keywords=keywords_result)

    else:
        return render_template("keywords-form.html")

#==============================================================================
# Clusters
#==============================================================================
@app.route('/clusters/', methods=['GET'])
def clusters():
    if 'testIdxGroup' in request.args.keys(): # form was submitted

        IdxGroup = request.args.get('testIdxGroup')
        # FIXME this might not work when dealing with only a few books,
        # rather than an entire subcorpus, in that case better use:
        # collection = args.getlist('testCollection') ## args is a 
        ## multiDictionary: use .getlist() to access individual books
        testCollection = request.args.get('testCollection')
        testIdxMod = request.args.get('testIdxMod')
        selectWords = "whole"
        
        args = request.args
        clusters_result = fetchClusters(args)

        return render_template("clusters-results.html",
                               IdxGroup=IdxGroup,
                               testCollection=testCollection,
                               testIdxMod=testIdxMod,
                               selectWords=selectWords,
                               clusters=clusters_result)

    else:
        return render_template("clusters-form.html")

#==============================================================================
# Chapters
#==============================================================================
@app.route('/chapter/<book>/<int:number>/')
@app.route('/chapter/<book>/<int:number>/<int:word_index>/<search_term>/')
def chapterView(number, book, word_index=None, search_term=None):
    chapter_repository = ChapterRepository()

    if word_index is None:
        chapter, book_title = chapter_repository.get_chapter(number, book)
    else:
        chapter, book_title = chapter_repository.get_chapter_with_highlighted_search_term(number, book, word_index, search_term)

    return render_template("chapter-view.html", content=chapter, book_title=book_title)

#==============================================================================
# Subsets
#==============================================================================
@app.route('/subsets/', methods=["GET"])
def subsets():
    """
    This is a quick and dirty method to display the subsets in our db.
    It now uses GET parameters, but should probably use POST parameters 
    ideally. 
    The basic design for POST parameters was almost ready but there were a
    few issues.
    """    
    
    
    book = request.args.get('book')
    subset = request.args.get('subset')

    if book and subset:
        return redirect(url_for('subsets_display', 
                                book=book,
                                subset=subset))
        
    return render_template("subsets-form.html")


@app.route('/subsets/<book>/<subset>/', methods=["GET", "POST"])
def subsets_display(book=None, subset=None):
        
    if book and subset:
        # make sure they are not malicious names
        book = secure_filename(book)
        subset = secure_filename(subset)
        
        if book not in BOOKS:
            return redirect(url_for('page_not_found'))
            
        if subset not in SUBSETS:
            return redirect(url_for('page_not_found'))
            
        BASE_DIR = os.path.dirname(__file__)
        filename = "../textfiles/{0}/{1}_{0}.txt".format(subset, book)
        with open(os.path.join(BASE_DIR, filename), 'r') as the_file:
            result = the_file.readlines()
        
        return render_template("subsets-results.html", 
                               book=book, 
                               subset=subset, 
                               result=result,
                               )
    
    else:
        return redirect(url_for('subsets'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found.html'), 404

# TODO delete?
if __name__ == '__main__':
    app.run()