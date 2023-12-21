import json
import os
import pickle

from flask import Flask, Response, request, jsonify
from src.linkedin_api import Linkedin
import src.linkedin_api.settings as settings
from requests.cookies import create_cookie, cookiejar_from_dict


def make_app():
    app = Flask(__name__)

    # create un-authenticated client
    linkedin = Linkedin()

    # implement logic to read cookies on start
    print("Attempting to use cached cookies...")
    try:
        with open(settings.COOKIE_FILE_PATH, "rb") as f:
            cookies = pickle.load(f)
            if cookies:
                linkedin.client.set_cookies(cookies)
                print("Cookies were initialized from cache.")
    except FileNotFoundError:
        print("Cookie file not found. No cookies were set from cache.")

    @app.route('/linkedin/profile/<profile_vanity_id>')
    def index(profile_vanity_id):
        assert profile_vanity_id is not None
        profile = linkedin.get_profile(profile_vanity_id)
        return jsonify(profile)

    @app.route('/linkedin/cookies', methods=['POST'])
    def set_cookies():
        raw_cookies = request.json
        cookie_jar = cookiejar_from_dict({})
        for c in raw_cookies:
            if c["httpOnly"]:
                c['rest'] = {"HttpOnly": True}
            name = c["name"]
            value = c["value"]
            del c["name"]
            del c["value"]
            del c["httpOnly"]
            cookie_jar.set(name, value, **c)

        linkedin.client.set_cookies(cookie_jar)
        print('Cookies were successfully set.')
        return Response("", 200)

    return app


if __name__ == "__main__":
    webapp = make_app()
    webapp.run(port=8000)
