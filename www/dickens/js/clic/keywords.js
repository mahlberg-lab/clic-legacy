

/**
 * Keyword handler javascript
 *
 */
(function (keywordHandler, $, _,undefined) {



        keywordHandler.fetch = function(url,data)
        {

            var query = decodeURIComponent($.param(data));
            var url = baseUrl + "?"+ query;

            $.ajax({
                  url: url,
                  data: data,
                  success: function(data){

                console.log(data);
              },
                error:function(xhr,error)
                {
                  console.debug(xhr); console.debug(error);
                }

              })


        }



}(window.keywordHandler = window.keywordHandler ||{},jQuery,_));
