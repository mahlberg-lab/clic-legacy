1.3.1
-----
* adds a DOI and a citable reference
* updates the docs 
* fixes issues in the KWICgrouper
* implements toggle for concordance view in User Annotation
* boosts export function of annotation to 10000 lines
* enable 1-gram keywords
* adds vodcast
* enables users to add each others tags
* disables the registration view
* updates docs of the User Annotation
 

1.3
---
* adds a user classification and annotation module that is only accessible for users with specific credentials
* allows users to create custom, user-specific tags and add these to subsets
* uses a postgreSQL database to store subsets, tags, notes, users, and roles
* documents the creation of tags, advanced filtering of subsets, phrases searches, and exporting
* allows for user-annotated csv-exports of up to 2000 rows
* adds advanced filtering to the subsets
  - including filtering on book name, abbreviation, user, text, etc.
  - using different filtering types as 'contains', 'not contains', 'in list', etc.
* adds a quick search box and documents its functionality
* enables sorting of subsets
* adds pagination
* enables user and role management
* hedges off the user annotation from the public site
* implements a different design to highlight that this module is not read-only

1.2
---
* adds a pattern module that allows advance concordance analysis (aka KWICgrouper)
* adds documentation next to the form
* enables sorting
* allows for a csv export
* generates a clickable collocation table
* adds a basic concordance for subsets executed in the background

1.1.3
-----
* populates Github releases page with our releases and allow users to download each release
* fixes bug that prevented the chapter view to load, before it was hard coded
* moves AHRC, UoB, and UoN logos up on large screens (and down on mobile devices)
* adds a tweet button to the about, documentation, news, and release pages
* renames the code repository
* redesigns corners from rounded to rectangular corners and moves loading icon up
* moves feedback widget into template block
* makes it possible to run debugging on the flask dev server
* adds news/blog page, a releases page, and a dropdown information menu for impact

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
