from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
import os

from flask import Flask, render_template, url_for, redirect, request
from werkzeug import secure_filename
import pandas as pd

from clic.web.api import api, fetchClusters, fetchKeywords
from clic.chapter_repository import ChapterRepository
from clic.kwicgrouper import KWICgrouper, concordance_for_line_by_line_file
from clic.web.forms import BOOKS, SUBSETS

app = Flask(__name__, static_url_path='')
app.register_blueprint(api, url_prefix='/api')

#TODO delete:
from flask_debugtoolbar import DebugToolbarExtension
app.debug = True
app.config["SECRET_KEY"] = "jadajajada"
toolbar = DebugToolbarExtension(app)

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
#==============================================================================
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


#==============================================================================
# KWICgrouper
#==============================================================================

@app.route('/patterns/', methods=["GET"])
def patterns():
    
    if not 'term' in request.args.keys():
        return render_template("patterns-form.html")
    
    else:
        
        # MAKE DRY
        book = request.args.get('book')
        subset = request.args.get('subset')
        term = request.args.get('term')
        local_args = dict(request.args)

        kwic_filter = {}
        for key,value in local_args.iteritems():
            if key == "subset" or key == "book" or key == "term":
                pass
            elif value[0]:
                # the values are in the first el of the list
                # 'L2': [u'a']
                values = value[0]
                values = values.split(",")
                values = [value.strip() for value in values]
                kwic_filter[key] = values
        
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
            concordance = concordance_for_line_by_line_file(os.path.join(BASE_DIR, filename), term)
            # should not be done here            
            if not concordance:
                return render_template("patterns-results.html", textframe="This term does not occur in the document you selected.")
            kwicgrouper = KWICgrouper(concordance)
            textframe = kwicgrouper.filter_textframe(kwic_filter)
            
            collocation_table = textframe.apply(pd.Series.value_counts, axis=0) 
            collocation_table["Sum"] = collocation_table.sum(axis=1)  
            collocation_table["Left Sum"] = collocation_table[["L5","L4","L3","L2","L1"]].sum(axis=1)  
            collocation_table["Right Sum"] = collocation_table[["R5","R4","R3","R2","R1"]].sum(axis=1)

            pd.set_option('display.max_colwidth', 1000)
            
            # replicate the index so that it is accessible from a row-level apply function
            # http://stackoverflow.com/questions/20035518/insert-a-link-inside-a-pandas-table
            collocation_table["collocate"] = collocation_table.index
            
            # function that can be applied
            def linkify(row, position, term=None, book=None, subset=None):
                """
                The purpose is to make links in the dataframe.to_html() output clickable.
                
                # http://stackoverflow.com/a/26614921
                """
                if pd.notnull(row[position]):
                    return """<a href="/patterns/?{0}={1}&term={2}&book={4}&subset={5}">{3}</a>""".format(position, 
                                                                                      row["collocate"], 
                                                                                      term,  
                                                                                      int(row[position]),
                                                                                      book,
                                                                                      subset
                                                                                     )
            
            # http://localhost:5000/patterns/?L5=&L4=&L3=&L2=&L1=&term=voice&R1=&R2=&R3=&R4=&R5=&subset=long_suspensions&book=BH
            
            def linkify_process(df, term):
                """
                """
                for itm in "L5 L4 L3 L2 L1 R1 R2 R3 R4 R5".split():
                    df[itm] = df.apply(linkify, args=([itm, term, book, subset]), axis=1)
                return df
            
            linkify_process(collocation_table, term)             
            del collocation_table["collocate"]
            
            return render_template("patterns-results.html", textframe=textframe.to_html(classes=["table", "table-striped", "table-hover", "dataTable", "no-footer", "uonDatatable"],
                                                                                        index=False),
                                   local_args=kwic_filter,
                                   collocation_table = collocation_table.fillna("").to_html(classes=["table", "table-striped", "table-hover", "dataTable", "no-footer", "uonDatatable"],
                                                                                            bold_rows=False,
                                                                                 ).replace("&lt;", "<").replace("&gt;", ">"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found.html'), 404

# TODO delete?
if __name__ == '__main__':
    app.run()
