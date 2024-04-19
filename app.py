import time, json, base64, requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)
app.config.from_pyfile("config.ini")


@app.route("/")
def index():
    return "<p>Hi.</p>"


@app.route("/.well-known/webfinger")
def wf():
    return jsonify(
        {
            "subject": "acct:%(USERNAME)s@%(HOSTNAME)s" % app.config,
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": "https://%(HOSTNAME)s/u/%(USERNAME)s" % app.config,
                }
            ],
        }
    )


@app.route("/u/<username>")
def user(username):
    my_url = "https://%(HOSTNAME)s/u/%(USERNAME)s" % app.config
    return (
        jsonify(
            {
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
                    "publicKeyPem": open("public.key", "r").read(),
                },
                "icon": {
                    "type": "Image",
                    "mediaType": "image/jpeg",
                    "url": app.config["ICON"],
                },
            }
        ),
        200,
        {"Content-type": "application/activity+json"},
    )


@app.route("/following")
def following():
    my_url = "https://%(HOSTNAME)s/u/%(USERNAME)s" % app.config
    return (
        jsonify(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "https://%(HOSTNAME)s/following" % app.config,
                "type": "Collection",
                "totalItems": 0,
                "items": [],
            }
        ),
        200,
        {"Content-type": "application/activity+json"},
    )


@app.route("/followers")
def followers():
    my_url = "https://%(HOSTNAME)s/u/%(USERNAME)s" % app.config
    return (
        jsonify(
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "https://%(HOSTNAME)s/followers" % app.config,
                "type": "Collection",
                "totalItems": 0,
                "items": [],
            }
        ),
        200,
        {"Content-type": "application/activity+json"},
    )


@app.route("/inbox", methods=["POST"])
def inbox():
    j = request.get_json(force=True)
    if j.get('type') == 'Follow':
        p = urlparse(j.get('actor'))
        send(p.netloc, '/inbox', str(time.time()), 'Accept', j)
    return ("", 202, {})


def sign_and_send(body, hostname, path):
    from email.utils import formatdate
    from Crypto.Hash import SHA256
    from Crypto.Signature import pkcs1_15
    from Crypto.PublicKey import RSA

    now = formatdate(usegmt=True)
    pk = RSA.import_key(open("private.key").read())
    post_hash = SHA256.new(body.encode("u8")).digest()
    post_hash_decoded = base64.b64encode(post_hash).decode()

    headers = (
        "(request-target): post "
        + path
        + "\n"
        + "host: "
        + hostname
        + "\n"
        + "date: "
        + now
        + "\n"
        + "digest: SHA-256="
        + post_hash_decoded
    )
    signature = base64.b64encode(
        pkcs1_15.new(pk).sign(SHA256.new(headers.encode("u8")))
    ).decode()  # such transcode, wow
    keyId = "https://%(HOSTNAME)s/u/%(USERNAME)s#main-key" % app.config
    sig_header = (
        'keyId="%s", algorithm="rsa-sha256", headers="(request-target) host date digest", signature="%s"'
        % (keyId, signature)
    )
    headers = {
        "signature": sig_header,
        "host": hostname,
        "digest": "SHA-256=" + post_hash_decoded,
        "content-type": "application/activity+json",
        "date": now,
    }
    res = requests.post("https://%s%s" % (hostname, path), data=body, headers=headers)
    return res.text

def send(server, uri, id_, type_, object_):
    my_url = "https://%(HOSTNAME)s/u/%(USERNAME)s" % app.config
    data = json.dumps(
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                ],
                "id": my_url + "/" + id_,
                "actor": my_url,
                "type": type_,
                "object": object_
            }
    )
    return sign_and_send(data, server, uri)
