

/**
 * Keyword handler javascript
 *
 */
(function (keywordHandler, $, _,undefined) {



        keywordHandler.fetch = function(url,data)
        {
            var baseUrl="http://localhost:8080/"
            var query = decodeURIComponent($.param(data));
            var url = baseUrl + "?"+ query;

            $.getJSON(url,function(data){

              console.log(data);

            })

        }



}(window.keywordHandler = window.keywordHandler ||{},jQuery,_));
