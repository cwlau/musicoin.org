
"""
This script runs an integration test against a deployed instance of our app.
Replace HOST with the URL your project will be deployed to.
"""

import urllib2

# The circle.yml deploys to version 1, which maps to this URL
HOST = 'https://1-dot-berry-blue.appspot.com/'

# [START e2e]
response = urllib2.urlopen("{}/him.html".format(HOST))
html = response.read()

assert(html[:3] == "him")
# [END e2e]
