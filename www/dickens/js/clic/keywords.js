

/**
 * Keyword handler javascript
 *
 */
(function (keywordHandler, $, _,undefined) {



        keywordHandler.fetch = function(url,data)
        {

            var query = decodeURIComponent($.param(data));
            var url = baseUrl + "?"+ query;

            $.getJSON(url,function(data){

                console.log(data);

                data["keywords"].each(function(keyword){

                    console.log(keyword[0]);
                })

                var tmplMarkup = $('#tmpl-keywords').html();

                if(_.isEmpty(keyword)){

                        $('#keywords').html("<p>no keywords</p>");
                    }
                    else
                    {
                    var compiledTmpl = _.template(tmplMarkup, { keywords : data["keywords"] });

                    $('#keywords').html(compiledTmpl);

                  }



            });


        }



}(window.keywordHandler = window.keywordHandler ||{},jQuery,_));
