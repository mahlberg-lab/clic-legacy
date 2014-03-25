(function() {
    var Lib = {
        ajax: {
            xhr: function() {
                var instance = new XMLHttpRequest();
                return instance;
            },
            getJSON: function(options, callback) {
                var xhttp = this.xhr();
                options.url = options.url || location.href;
                options.data = options.data || null;
                callback = callback ||
                    function() {};
                options.type = options.type || 'json';
                var url = options.url;
                if (options.type == 'jsonp') {
                    window.jsonCallback = callback;
                    var $url = url.replace('callback=?', 'callback=jsonCallback');
                    var script = document.createElement('script');
                    script.src = $url;
                    document.body.appendChild(script);
                }
                xhttp.open('GET', options.url, true);
                xhttp.send(options.data);
                xhttp.onreadystatechange = function() {
                    if (xhttp.status == 200 && xhttp.readyState == 4) {
                        callback(xhttp.responseText);
                    }
                };
            }
        }
    };

    window.Lib = Lib;
})();


/**
 * Keyword handler javascript
 *
 */
(function (keywordHandler, $, _,Lib,undefined) {



        keywordHandler.fetch = function(url,data)
        {
            var baseUrl="http://localhost:8080/"
            var query = decodeURIComponent($.param(data));
            var url = baseUrl + "?"+ query;

            Lib.getJSON({url:url},function(data){

              console.log(data);

            })

        }



}(window.keywordHandler = window.keywordHandler ||{},jQuery,_,Lib));
