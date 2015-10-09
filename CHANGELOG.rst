1.1.2
-----
* adds logo of the University of Birmingham (the new home of the CLiC project)
* adds Google analytics for the Birmingham server
* changes the contact in the about page to clic@contacts.bham.ac.uk

1.1.1
-----
* fixes a bug that deleted the Google Analytics javascript
* adds a licence to the code
* adds this changelog

1.1
---
* adds subsets as a way to navigate and explore quotes, suspensions, short suspensions, etc.
* boosts number of uwsgi processes
* adds a profiler
* activates 1-grams in keywords and clusters

1.0.6
-----
* moves clusters and keywords to jinja templates (speeds them up massively because
  there is less client side rendering)
* boosts number of uwsgi processes

1.0.5
-----
* adds AHRC logo

1.0.4
-----
* disables the 6-12 gram options
* enables indefinite caching
* swaps the loading bar for a spinning icon
* reduces the number of clusters that can be retrieved in one go to 3000
* makes clusters and keywords results clickable (this leads to a concordance,
  which in turn is clickable to lead to the text)

1.0.3
-----
* chapter view now highlights the search term
* removes jquery js to highlight the term (now it is done in the backend)
* adds initial settings management
* adds more tests

1.0.2
-----
* updates text displayed when concordance results table has no entries to '0 entries'
* refactors concordance view
* adds functional tests and unit tests
* starts working with jinja templates
* cleans up files
* initial, raw version of a chapter view (when clicking on a concordance line, the chapter is displayed)

1.0.1
-----
* adds total count of occurrences in concordance
* speeds up the concordance (for instance, by optimising xpath queries)
* fixes issues with non-alphabetic character rendering in the frontend concordance
