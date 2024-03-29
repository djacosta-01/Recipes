import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
from urllib import urlencode
import json

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SearchFormHandler(webapp2.RequestHandler):
    def get(self):
        info = the_jinja_env.get_template('templates/form.html')
        self.response.write(info.render())

class RecipeDisplayHandler(webapp2.RequestHandler):
    def post(self):
        welcome_template = the_jinja_env.get_template('templates/recipe.html')
        query = self.request.get("query")
        base_url = "http://www.recipepuppy.com/api/?"
        params = { 'q': query }
        response = urlfetch.fetch(base_url + urlencode(params)).content
        results = json.loads(response)
        self.response.write(welcome_template.render({
         "results": results
        }))

app = webapp2.WSGIApplication([
    ('/', SearchFormHandler),
    ('/recipe', RecipeDisplayHandler)
], debug=True)
