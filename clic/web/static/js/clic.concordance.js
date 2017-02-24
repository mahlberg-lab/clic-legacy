;(function ( $, window, document, undefined ) {

    // Create the defaults once
    var pluginName = "concordanceResults",
        defaults = {
            concordanceEndpointUrl : "/api/concordances/",
            bookCountsEndpointUrl : "/exampleJson/bookcounts.json"
        };

    function escapeHtml (s) {
        // https://bugs.jquery.com/ticket/11773
        return (String(s)
            .replace(/&(?!\w+;)/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')); // "
    }

    function isWord (s) {
        return /\w/.test(s);
    }

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
        kwicTimeout: null,
        kwicTerms: {},
        kwicSpan: [{start:1}, {start:1}, {start:1}],

        init: function() {
            var that = this;

            // Column is an array of tokens, mark these up as words, only sort on word content
            function renderTokenArray( reverseSort, data, type, full, meta ) {
                var i, t, count = 0, out = "", span_class;

                if (type === 'display') {
                    for (i = 0 ; i < data.length; i++) {
                        t = data[reverseSort ? data.length - i - 1 : i];
                        if (isWord(t)) {
                            count++;
                            span_class = "w node-" + count;
                        } else {
                            span_class = ""
                        }

                        if (reverseSort) {
                            out = '<span class="' + span_class + '">' + escapeHtml(t) + "</span>" + out;
                        } else {
                            out = out + '<span class="' + span_class + '">' + escapeHtml(t) + "</span>";
                        }
                    }
                } else {
                    for (i = 0 ; i < data.length; i++) {
                        t = data[reverseSort ? data.length - i - 1 : i];
                        if (isWord(t)) {
                            count++;
                            out += t + ":";
                            if (count >= 3) {
                                return out;
                            }
                        }
                    }
                }

                return out;
            }
            renderForwardTokenArray = renderTokenArray.bind(null, false);
            renderReverseTokenArray = renderTokenArray.bind(null, true);

            // Column represents a fractional position
            function renderPosition( data, type, full, meta ) {
                var xVal;

                if (type !== 'display') {
                    return data[2];
                }

                xVal = (data[2] / data[3]) * 50; // word in book / total word count
                return '<a href="#" class="bookLink" title="Click to display concordance in book" target="_blank">'+
                       '<svg width="50px" height="15px" xmlns="http://www.w3.org/2000/svg">' +
                       '<rect x="0" y="4" width="50" height="7" fill="#ccc"/>' +
                       '<line x1="' + xVal + '" x2="' + xVal + '" y1="0" y2="15" stroke="black" stroke-width="2px"/>' +
                       '</svg></a>';
            }

            // Column shows a count
            function renderColumnCount( data, type, row, meta ) {
                return meta.row + meta.settings._iDisplayStart + 1;
            }

            // Kwicmatches are just true / false iff there's a match
            function renderKwicMatch( data, type, row, meta ) {
                return !!data;
            }

            that.processParameters(document.location.search);
            $("#searchedFor").html("Searched for <b>" + that.searchTerms + "</b> within <b>" + that.searchSpace + "</b>.");

            that.concordanceTable = $('#dataTableConcordance').DataTable({
                ajax: that.fetchData.bind(that),
                deferRender: true,
                columns: [
                    { data: "5", render: renderKwicMatch, visible: false, sortable: false, searchable: false },
                    { title: "", data: null, render: renderColumnCount, sortable: false, searchable: false },
                    { title: "Left", data: "0", render: renderReverseTokenArray, class: "contextLeft text-right" }, // Left
                    { title: "Node", data: "1", render: renderForwardTokenArray, class: "contextNode hilight" }, // Node
                    { title: "Right", data: "2", render: renderForwardTokenArray, class: "contextRight" }, // Right
                    { title: "Book", data: "3.1", searchable: false }, // Book
                    { title: "Ch.", data: "3.2", searchable: false }, // Chapter
                    { title: "Par.", data: "3.3", searchable: false }, // Paragraph
                    { title: "Sent.", data: "3.4", searchable: false }, // Sentence
                    { title: "In&nbsp;bk.", data: "4", render: renderPosition, searchable: false, orderData: [5, 9] }, // Book graph
                ],
                orderFixed: {
                    pre: [['0', 'desc']],
                },
                order: [[9, 'asc']],
                filter: true,
                sort: true,
                paginate: true,
                displayLength: 50,
                language: {
                    search: "Filter concordance:",
                },
                createdRow: function ( row, data, index ) {
                    that.updateKwicRow(row, data[5]);
                },
                //TODO: TableTools Copy CSV / Print / Toggle metadata?
                //TODO: Toggle metadata option?
            });

            // Generate URLs when needed, not every single time
            $('#dataTableConcordance').on('mouseenter click', 'a.bookLink', function (e) {
                var rowData = that.concordanceTable.row($(this).closest('tr')).data();

                $(this).attr('href', [
                    '/chapter',
                    rowData[3][0],
                    rowData[3][2],
                    rowData[3][5],
                    that.searchTerms,
                    '#concordance',
                ].join('/'));
            });

            noUiSlider.create($("#kwicGrouper .slider")[0], {
                start: [-5, 5],
                range: { min: -5, max: 5 },
                step: 1,
                pips: {
                    mode: 'steps',
                    density: 10,
                    filter: function (v, t) { return v === 0 ? 1 : 2 },
                    format: { to: function (v) { return (v > 0 ? 'R' : v < 0 ? 'L': '') + Math.abs(v) } },
                },
                format: {
                    to: function ( value ) { return value; },
                    from: function ( value ) { return value.replace('L', '-').replace('R', ''); },
                },
                connect: true
            });

            $("#kwicGrouper select").chosen({
                width: "100%;"
            });

            $("#kwicGrouper .action-openclose").on("click", function (e) {
                $('#kwicGrouper').toggleClass('in');
            });
            $("#kwicGrouper .action-clear").on("click", function (e) {
                that.kwicTerms = {};
                $("#kwicGrouper select").val([]).trigger("chosen:updated");

                that.kwicSpan = [{start:1}, {start:1}, {start:1}];
                $("#kwicGrouper .slider")[0].noUiSlider.set([-5, 5]);

                that.scheduleUpdateKwicGroup();
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

                    for (i = 0; i < coData.length; i++) {
                        // Add KWICGrouper match column, assume no KWICGrouper initially
                        coData[i].push("");
                    }

                    Pace.stop();
                    callback({ data: coData });

                    $("#kwicGrouper select").html(that.findConcordanceTypes(coData).map(function (t) {
                        return "<option>" + escapeHtml(t) + "</option>";
                    }).join("")).trigger("chosen:updated");

                    $("#kwicGrouper select").on("change", function (e) {
                        // Update terms object based on what's been selected, fill with position in list
                        that.kwicTerms = {};
                        ($('#kwicGrouper select').val() || []).map(function (t, i) {
                            that.kwicTerms[t.toLowerCase()] = i + 1;
                        });

                        that.scheduleUpdateKwicGroup();
                    });

                    $("#kwicGrouper .slider")[0].noUiSlider.on('update', function (values) {
                        // Values has 2 values, a min and max, which we treat to be 
                        // min and max span inclusive, viz.
                        //      [0]<---------------------->[1]
                        // -5 : -4 : -3 : -2 : -1 | 0 | 1 : 2 : 3 : 4 : 5

                        // Left
                        that.kwicSpan[0] = values[0] >= 0 ? {ignore: true} : {
                            start: 0 - Math.min(values[1], -1),
                            stop: 0 - values[0],
                            reverse: true,
                            prefix: 'l',
                        };

                        // Node: all or nothing, depending on if 0 was included
                        that.kwicSpan[1] = values[0] <= 0 && values[1] >= 0 ? { start: 1, prefix: 'n' } : {ignore: true};

                        // Right
                        that.kwicSpan[2] = values[1] <= 0 ? {ignore: true} : {
                            start: Math.max(values[0], 0),
                            stop: values[1],
                            prefix: 'r',
                        };

                        that.scheduleUpdateKwicGroup();
                    });

                    $('#plotTbody').html(that.processConcordancePlot(coData, that.processChapterMarkers(chData)));
                },
                function(e) { // failure
                    var message = "Sorry. Failed to load data. Please try again.";

                    console.log(e);
                    if (e.responseJSON && e.responseJSON.error) {
                        message = "Failed to load data: " + e.responseJSON.error;
                    }
                    $('#concordanceWrap').addClass('error').empty().append([
                        $('<p/>').text(message),
                        $('<a href="/concordances">Go back and try a different query</a>').on('click', function (e) {
                            e.preventDefault();
                            window.history.go(-1);
                        }),
                    ]);
                    Pace.stop()
                }
            );
        },

        scheduleUpdateKwicGroup: function () {
            // Try to batch updates a bit
            if (this.kwicTimeout) {
                window.clearTimeout(this.kwicTimeout);
            }
            this.kwicTimeout = window.setTimeout(this.updateKwicGroup.bind(this), 300);
        },

        updateKwicGroup: function () {
            var that = this,
                kwicTerms = this.kwicTerms,
                kwicSpan = this.kwicSpan,
                totalMatches = 0;

            // Check if list (tokens) contains any of the (terms) between (span.start) and (span.stop) inclusive
            // considering (tokens) in reverse if (span.reverse) is true
            function testList(tokens, span, terms) {
                var i, t, l = [], wordCount = 0;

                if (span.start === undefined) {
                    // Ignoring this row
                    return "";
                }

                for (i = 0; i < tokens.length; i++) {
                    t = tokens[span.reverse ? tokens.length - i - 1 : i];

                    if (!isWord(t)) {
                        continue;
                    }

                    wordCount++;
                    if (wordCount >= span.start && terms.hasOwnProperty(t.toLowerCase())) {
                        // Matching has started and matches a terms, return which match it is
                        return span.prefix + '-' + wordCount;
                    }
                    if (span.stop !== undefined && wordCount >= span.stop) {
                        // Finished matching now, give up.
                        break;
                    }
                }

                return "";
            }

            this.concordanceTable.rows().every(function () {
                var d = this.data(),
                    new_result = testList(d[0], kwicSpan[0], kwicTerms) ||
                                 testList(d[1], kwicSpan[1], kwicTerms) ||
                                 testList(d[2], kwicSpan[2], kwicTerms);

                if (new_result) {
                    totalMatches++;
                }

                if (d[5] !== new_result) {
                    // Concordance membership has changed, update table
                    d[5] = new_result;
                    that.updateKwicRow(this.node(), d[5]);

                    this.invalidate();
                }
            });

            $('#kwicGrouper .matchCount').text(totalMatches);
            this.concordanceTable.draw();
        },

        /* Modify row markup to reflect match status */
        updateKwicRow: function ( row, rowData ) {
            $(row).toggleClass('kwicMatch', !!rowData)
                  .attr('data-kwic-match', rowData);
        },

        findConcordanceTypes: function ( coData ) {
            var i, j, k, s, out = {};

            for (i = 0; i < coData.length; i++) { // Each concordance match
                for (j = 0; j < 3; j++) { // Left / node / right
                    for (k = 0; k < coData[i][j].length; k++) { // Word / non-word strings
                        s = coData[i][j][k];
                        if (isWord(s)) {
                            //TODO: Node is also stemmed when searched for: e.g. 'camel', 'camel's'. Replicate?
                            //TODO: Stop searching outside the span we can't select anyway? Or are we just hiding everything outside L/R5?
                            out[s.toLowerCase()] = true;
                        }
                    }
                }
            }
            return Object.keys(out);
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
