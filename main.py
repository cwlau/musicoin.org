#!/usr/bin/env python

import json
import logging
import os
import traceback
import webapp2
from webapp2_extras import routes

from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

from config import TOKEN



def slack_invite(email):

    url = "https://musicoin.slack.com/api/users.admin.invite?email=" \
        + email + "&token=" + TOKEN + "&set_active=true"

    try:
        urlfetch.set_default_fetch_deadline(30)

        result = urlfetch.fetch(
            url=url,
            payload={},
            method=urlfetch.GET,
            headers={'Accept': 'application/json'}
        )

    except:
        stacktrace = traceback.format_exc()
        logging.error("urlfetch URL failure \n\n%s", stacktrace)

        return


    logging.info(result.content)
    return result.content







class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/index.html')
        self.response.out.write(template.render(path, {}))

class HowItWorksHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/howItWorks.html')
        self.response.out.write(template.render(path, {}))

class MusiciansHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/musicians.html')
        self.response.out.write(template.render(path, {}))

class DevelopersHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/developers.html')
        self.response.out.write(template.render(path, {}))




class SlackInvitePageHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        logging.info("Opening Slack invite page")

        path = os.path.join(os.path.dirname(__file__), 'template/slack_invite.html')
        self.response.out.write(template.render(path, template_values))


class SlackInviteSuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email", "")
        if email == "":
            self.redirect("/join/")
            return

        template_values = {
            "email": email
        }

        path = os.path.join(os.path.dirname(__file__), 'template/slack_invited.html')
        self.response.out.write(template.render(path, template_values))


class SlackInviteActionHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write("Method GET not allowed")
        self.response.set_status(405)

    def post(self):

        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers["Content-Type"] = "application/json"

        email = self.request.get("email")
        if not email:
            self.response.write(json.dumps({"status": "error", "message": "PARAMETER_MISSING"}))
            return

        logging.info("email = " + email)

        try:
            invite_result = slack_invite(email)

            json_object = json.loads(invite_result)

            logging.info(json_object["ok"])
            logging.info(json_object["ok"] is True)

            if json_object["ok"] is True:
                self.response.write(json.dumps({
                    "status": "success",
                    "message": ""
                }))
                return

            else:
                self.response.write(json.dumps({
                    "status": "failed",
                    "message": json_object["error"]
                }))

        except:
            stacktrace = traceback.format_exc()
            logging.error("slack_invite failure \n\n%s", stacktrace)

            self.response.write(json.dumps({
                "status": "failed",
                "message": ""
            }))


class ReturnHomePageHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect("/")


class BlogRedirectHandler(webapp2.RequestHandler):

    def get(self):
        self.redirect("https://medium.com/@musicoin")




app = webapp2.WSGIApplication([
    # routes.DomainRoute(r'<:(slack\.hongcoin\.org|localhost)>', [
    routes.DomainRoute(r'<:(blog.musicoin.org)>', [
        webapp2.Route('/', BlogRedirectHandler),
        webapp2.Route('/.*', BlogRedirectHandler),
    ]),

    routes.DomainRoute(r'<:(musicoin.org|www.musicoin.org|localhost|layout2.musicoin-web.appspot.com)>', [
        webapp2.Route('/', HomePageHandler),
        webapp2.Route('/about', HowItWorksHandler),
        webapp2.Route('/musicians', MusiciansHandler),
        webapp2.Route('/developers', DevelopersHandler),
    ]),

    # Slack signup
    routes.DomainRoute(r'<:(slack.musicoin.org|slack.default.musicoin-web.appspot.com)>', [
        webapp2.Route('/', SlackInvitePageHandler),
        webapp2.Route('/join', SlackInvitePageHandler),
        webapp2.Route('/join/', SlackInvitePageHandler),
        webapp2.Route('/join/invited', SlackInviteSuccessPageHandler),
        webapp2.Route('/join/slack/invite', SlackInviteActionHandler),
    ]),

    # Slack signup for localhost
    routes.DomainRoute(r'<:(localhost)>', [
        webapp2.Route('/', HomePageHandler),
        webapp2.Route('/join', SlackInvitePageHandler),
        webapp2.Route('/join/', SlackInvitePageHandler),
        webapp2.Route('/join/invited', SlackInviteSuccessPageHandler),
        webapp2.Route('/join/slack/invite', SlackInviteActionHandler),
    ]),

    ('/', HomePageHandler),
    ('/.*', ReturnHomePageHandler),

])
