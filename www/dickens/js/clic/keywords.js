

/**
 * Keyword handler javascript
 *
 */
(function (keywordHandler, $, _,undefined) {



        keywordHandler.processor = function(data)
        {

            var tmplMarkup = $('#tmpl-keywords').html();

                if(_.isEmpty(keyword)){

                        $('#keywords').html("<p>no keywords</p>");
                    }
                    else
                    {
                    var compiledTmpl = _.template(tmplMarkup, { keywords : data["keywords"] });

                    $('#keywords').html(compiledTmpl);

                  }



        }



}(window.keywordHandler = window.keywordHandler ||{},jQuery,_));
