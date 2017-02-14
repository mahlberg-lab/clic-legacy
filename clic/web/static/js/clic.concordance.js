;(function ( $, window, document, undefined ) {

    // Create the defaults once
    var pluginName = "concordanceResults",
        defaults = {
            concordanceEndpointUrl : "/api/concordances/",
            bookCountsEndpointUrl : "/exampleJson/bookcounts.json"
        };

    // The actual plugin constructor
    function Plugin( element, options ) {
        this.element = element;

        // jQuery has an extend method that merges the
        // contents of two or more objects, storing the
        // result in the first object. The first object
        // is generally empty because we don't want to alter
        // the default options for future instances of the plugin
        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;

        this.init();
    }

    Plugin.prototype = {

        searchTerms: "",
        searchSpace: "",
        totalNumberOfHits: 0,

        init: function() {
            var that = this;

            function renderTokenArray( data, type, full, meta ) {
                //TODO: Generate HTML for nodes
                return data.join("");
            }

            function renderPosition( data, type, full, meta ) {
                var xVal;

                if (type === 'sort') {
                    return data[2];
                }

                xVal = (data[2] / data[3]) * 50; // word in book / total word count
                return '<svg width="50px" height="15px" xmlns="http://www.w3.org/2000/svg">' +
                       '<rect x="0" y="4" width="50" height="7" fill="#ccc"/>' +
                       '<line x1="' + xVal + '" x2="' + xVal + '" y1="0" y2="15" stroke="black" stroke-width="2px"/>' +
                       '</svg>';
            }

            that.processParameters(document.location.search);

            $('#dataTableConcordance').dataTable({
                /*TODO:
                var chapterViewUrl = '/chapter/' + data.concordances[x][3][0] + '/' + data.concordances[x][3][2] + '/' + data.concordances[x][3][5] + '/' + this.searchTerms + '/#concordance';
                content += '<tr class="clickable_row" data-url="' + chapterViewUrl + '">';
                */

                ajax: that.fetchData.bind(that),
                columns: [
                    //TODO: Counter column?
                    { title: "Left", data: "0", render: renderTokenArray, class: "text-right" }, // Left //TODO: Custom sort
                    { title: "Node", data: "1", render: renderTokenArray, class: "hilight" }, // Node //TODO: Custom sort
                    { title: "Right", data: "2", render: renderTokenArray }, // Right //TODO: Custom sort
                    { title: "Book", data: "3.1" }, // Book
                    { title: "Ch.", data: "3.2" }, // Chapter
                    { title: "Par.", data: "3.3" }, // Paragraph
                    { title: "Sent.", data: "3.4" }, // Sentence
                    { title: "In&nbsp;bk.", data: "4", render: renderPosition }, // Book graph TODO: Custom sort
                ],
                filter: true,
                sort: true, //TODO: What should the default sorting be?
                paginate: true,
                language: {
                    search: "Filter concordance:" //TODO: Actually limit it to concordance?
                },
                //TODO: TableTools Copy CSV / Print / Toggle metadata?
                //TODO: Toggle metadata option?
            });
        },

        fetchData: function ( data, callback, settings ) {
            var that = this;

            $.when(
                $.ajax({
                    url: that.options.bookCountsEndpointUrl,
                    type: 'GET',
                    dataType: 'json'}),
                $.ajax({
                    url: that.options.concordanceEndpointUrl + document.location.search,
                    type: 'GET',
                    dataType: 'json'})
            ).then(
                function(chaptersResponse, concordancesResponse) { // success
                    var chData = chaptersResponse[0];
                    var coData = concordancesResponse[0].concordances.slice(1);

                    $("#searchedFor").html("Searched for <b>" + that.searchTerms + "</b> within <b>" + that.searchSpace + "</b>.");

                    Pace.stop();
                    callback({ data: coData });

                    $('#plotTbody').html(that.processConcordancePlot(coData, that.processChapterMarkers(chData)));
                },
                function(e) { // failure
                    console.log(e);
                    alert("Sorry. Failed to load data. Please try again.");
                    Pace.stop()
                }
            );
        },

        processParameters: function( params ) {
            var searchTerms = params.slice(params.indexOf("terms=") + 6);
            this.searchTerms = decodeURIComponent(searchTerms.slice(0, searchTerms.indexOf("&")).replace(/\+/g, ' '));

            var testIdxMod = params.slice(params.indexOf("testIdxMod=") + 11);

            switch(testIdxMod) {
                case "quote":
                    this.searchSpace = "quotes";
                    break;

                case "non-quote":
                    this.searchSpace = "non-quotes";
                    break;

                case "longsus":
                    this.searchSpace = "long suspensions";
                    break;

                case "shortsus":
                    this.searchSpace = "short suspensions";
                    break;

                default:
                    this.searchSpace = "whole text";
                    break;
            }
        },

        processChapterMarkers: function( data ) {
            chapterDataArray = [];
            for (var x = 0; x < data[1].length; x++) {

                // Per book chapter SVG shading
                var bookTitle = data[1][x][1];
                var chapters = data[1][x][3]; // chapter data
                var total = (data[1][x][2][0] / 1000);// <total words in book> / <length of SVG (constant) >

                var xVal = '';
                var wVal = '';
                var svg = '';

                for (var i = 1; i < chapters.length; i = i + 2) {
                    xVal = chapters[i] / total;
                    wVal = (chapters[i + 1] - chapters[i]) / total; //width
                    svg += '<rect x="' + xVal + '" y="0" width="' + wVal + '" height="27" fill="#bbb"/>';
                }

                chapterDataArray.push({
                    booktitle: bookTitle,
                    svgMarkup: svg
                });
            }

            return chapterDataArray;
        },

        processConcordancePlot: function( data, chapterDataArray ) {
            // Add unique book titles to array
            var uniqueBookTitles = [];
            for (var x = 0; x < data.length; x++) {
                var bookTitle = data[x][3][1];
                if (uniqueBookTitles.indexOf(bookTitle) < 0) {
                    uniqueBookTitles.push(bookTitle);
                }
            }
            uniqueBookTitles.sort();

            var plotContent = '';
            for (var i = 0; i < uniqueBookTitles.length; i++) {

                // loop out line values
                var lines = '';
                var lineCount = 0; // no of occurrences of word
                for (var x = 0; x < data.length; x++) {
                    // if this is the book title we want
                    if (data[x][3][1] == uniqueBookTitles[i]) {
                        // calculate line values
                        var totalWordCountInBook = data[x][4][3];
                        var adjustedTotalWordCountInBook = totalWordCountInBook / 1000;
                        var wordInBook = data[x][4][2];
                        var xVal = wordInBook / adjustedTotalWordCountInBook;

                        // line here
                        lines += '<line x1="' + xVal + '" x2="' + xVal + '" y1="0" y2="27" stroke="#468847" stroke-width="3px"/>';
                        lineCount++;
                    }

                }
                plotContent += '<tr>';
                plotContent += '<td class="book">' + uniqueBookTitles[i] + '</td><td>'+lineCount+'</td>';
                plotContent += '<td class="plot">';
                plotContent += '<svg width="100%" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 27" preserveAspectRatio="none">';

                plotContent += '<rect x="0" y="0" width="1000" height="27" fill="#ccc"/>';

                // Add chapter shading to SVG
                var thisSvgMarkup = $.grep(chapterDataArray, function (e) { return e.booktitle == uniqueBookTitles[i]; }); // lookup
                if (typeof thisSvgMarkup[0] != "undefined") {
                    plotContent += thisSvgMarkup[0].svgMarkup;
                }
                plotContent += lines + '</svg></td></tr>';
            }

            return plotContent;
        },
    };

    // A really lightweight plugin wrapper around the constructor,
    // preventing against multiple instantiations
    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName,
                new Plugin( this, options ));
            }
        });
    };

})( jQuery, window, document );
