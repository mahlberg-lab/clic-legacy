XSLT
====

Much of the XSLT work was carried out inside the chapterView code as part of a transformer for the results returned but there is still a significant amount of xpath work inside ```concordance.py``` as well as the various endpoint processing files within the _web_ folder.

The xpath was badly optimised to start with and gradually it was improved though it's still not ideal as the speed of processing is vastly slower then the database retrieval.

Future work would be to reduce the amount of xpath queries that need to be carried out on a per page basis. Perhaps by introducing pagination to the result sets since you would only need to process the records you wanted to show to the user rather then all of them. Doing this would mean that you would not be limited to returning 1000 results at a time.
