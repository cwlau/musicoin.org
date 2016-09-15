#!/usr/bin/env python

import webapp2
from config import LETS_ENCRYPT_RESPONSE

class LetsEncryptHandler(webapp2.RequestHandler):

    def get(self, challenge):
        self.response.headers['Content-Type'] = 'text/plain'
        responses = LETS_ENCRYPT_RESPONSE
        self.response.write(responses.get(challenge, ''))



app = webapp2.WSGIApplication([
    ('/.well-known/acme-challenge/([\w-]+)', LetsEncryptHandler),
], debug=False)

