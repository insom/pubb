from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.ini')

@app.route("/")
def index():
    return "<p>Hi.</p>"

@app.route("/.well-known/webfinger")
def wf():
    return jsonify({
        "subject": "acct:%(USERNAME)s@%(HOSTNAME)s" % app.config,
        "links": [{'rel': 'self', 'type': 'application/activity+json',
                   'href': 'https://%(HOSTNAME)s/u/%(USERNAME)s' % app.config}],
        })

@app.route("/u/<username>")
def user(username):
    my_url = "https://%(HOSTNAME)s/u/%(USERNAME)s" % app.config
    return (jsonify({
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1",
  ],
  "id": my_url,
  "type": "Person",
  "following": "https://%(HOSTNAME)s/following" % app.config,
  "followers": "https://%(HOSTNAME)s/followers" % app.config,
  "inbox": "https://%(HOSTNAME)s/inbox" % app.config,
  "outbox": "https://%(HOSTNAME)s/outbox" % app.config,
  "preferredUsername": app.config["USERNAME"],
  "name": app.config["USERNAME"],
  "summary": "",
  "url": my_url,
  "manuallyApprovesFollowers": False,
  "discoverable": True,
  "indexable": False,
  "published": "2024-04-04T00:00:00Z",
  "memorial": False,
  "publicKey": {
    "id": my_url + "#main-key",
    "owner": my_url,
    "publicKeyPem": open("public.key", 'r').read(),
  },
  "icon": {
    "type": "Image",
    "mediaType": "image/jpeg",
    "url": app.config['ICON'],
  },
  }), 200, {'Content-type': 'application/activity+json'})
