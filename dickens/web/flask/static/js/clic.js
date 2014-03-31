/**
 *  name: jsonHandler
 *  authors: Rein Shaun
 *  date: 28.03.2014
 *  description: handles json processing for the clic project
 */
(function (jsonHandler, $, _,undefined) {


		/**
		* name:processor
		* description public method to load the template
		* params: object data - (json data typically returned from clic.py end points and stored in appropriately named variable in document
		*		  string dataName name of json variable
		* 
		*/
        jsonHandler.processor = function(data,dataName)
        {

			
            getTemplate(data,dataName);


        }
		
		/**
		* name:getTemplate
		* description private method: compiles a template using the data provided.
		* params: data object - (json data typically returned from clic.py end points and stored in appropriately named variable in document
		*		  string dataName name of json variable
		* 
		*/
        getTemplate= function(data,dataName){

          var tmplMarkup = $('#tmpl-'+dataName).html();

              if(_.isEmpty(data)){

                      $('#'+dataName).html("<p> no "+dataName+"</p>");
                  }
                  else
                  {
                   
                   var templateData={dataItems:data[dataName]};	
                  
                   var compiledTmpl = _.template(tmplMarkup, templateData);
				  
                  $('#'+dataName).html(compiledTmpl);

                }

        }



}(window.jsonHandler = window.jsonHandler ||{},jQuery,_));