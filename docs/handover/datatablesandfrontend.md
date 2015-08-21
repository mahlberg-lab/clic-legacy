Datatables and frontend
=======================

[Datatables](https://datatables.net) is used to show the data we get from our searches. It's a relatively complex piece of javascript that allows the bulk of tabular data manipulation to be handled on the frontend. It support all sorts of options but the one that probably needs looking at is the capability for it to use paginated data from the backend. Doing this would concievably increase the speed of the website quite drastically as we'd be limited to processing only a small amount of data at a time.

In terms of suitability for our purposes it fairly closely matches what we need to do (filtering, ordering etc.) but it has a few downsides. Mainly that to customise any of this you'll need to work with a fairly obtuse javascript API.

As part of the work toward making the search functionality work as a kwikgrouper pattern I was quite heavily considering having to rewrite the entirety of the datatables integration. It would need to be a series of javascript object/plugins/modules that would handle the integration between the multiple possible patterns that make up a kwikgrouper search and how that would interface with multiple instances of the datatables for that page. So that speed was high enough it would have been a pre-requisite of this work that the datatables used server side pagination - this obviously means a rewrite of the way we process and return data from the service classes (concordance.py, clusters.py etc.)

Custom jQuery plugins
=====================

In order to make the frontend code more managable, and as part of the big purge operation, all the inline script that comprised the concordance page was moved to a javascript plugin _clic.concordance.js_. This plugin handles the retrieval of two sets of ajax data, the initalisation of Datatables with this data and the rendering of the plot view. The work flow for the majority of this can be found in the prototype init function found on line 33

```
init: function() {
    var that = this;

    var params = location.search;
    this.processParameters(params);
    var concordanceUrl = this.options.concordanceEndpointUrl + params;

    $.when(
        $.ajax({
            url: that.options.bookCountsEndpointUrl,
            type: 'GET',
            dataType: 'json'}),
        $.ajax({
            url: concordanceUrl,
            type: 'GET',
            dataType: 'json'})
    ).then(

    ....
```

Loading Bar
===========

The loading bar is implemented using a javascript library called [Pace](http://github.hubspot.com/pace/docs/welcome/). Although it allows automation of the loading bars we take more careful control of it's running so that we can tie it closer to the code thats doing the processing. You can see this in the _clic.concordance.js_ file.

```
60 Pace.stop();
```

As per the pace documentation changing the theme is mostly as simple as calling a different css file in your document. The change to the rounded spinner (to remove any indication of a possible end to processing) was as simple as this.
