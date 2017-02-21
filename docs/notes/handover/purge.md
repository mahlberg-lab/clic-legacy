Purge
=====

The project had gone through a number of organic growth spurts when it was taken on by Carl and I. We decided that in order to speed development down the line some cleanup of what was being done would be carried out.

Initially the project directories were moved around and a layer or two of hierarchy was removed. The configuration files needed fixing to pick up these changes.

Then, although the project had implemented flask (an python MVC library), it was not using it correctly and was still relying on static files as its pages. I took those static files and converted them to flask templates. I created the prerequisite endpoints and controllers to route to those templates. I also broke out the AJAX endpoint and web endpoints using flask blueprints.

```
#index.py

app = Flask(__name__, static_url_path='')
app.register_blueprint(api, url_prefix='/api')
```

The final piece of work (documented in datatablesandfrontend.md more thouroughly) was to take the inline javascript in the various templates and turn it into javascript plugins that could be manaaged better. Whilst doing this I discovered that the concordance code was quite reliant on a race condition in order to function so changes were made to fix that.

After the purge Carl discovered that some things were not function due to configuration and code references referring to old paths. These were corrected.

Johan discovered that some files that were removed were part of the functioning of python (.egg files and \_\_init\_\_.py). These were replaced on an as needed basis.
