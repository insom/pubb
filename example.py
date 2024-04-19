from app import send, app
import json
from datetime import datetime, timezone

def example_upload():
    my_url = 'https://example.com/u/example'
    now = datetime.now(timezone.utc).isoformat()
    idx = str(8)
    print(repr(send('tiny.tilde.website', '/inbox', idx, 'Create',
                    {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "id": my_url + "/" + idx,
                        "type": "Note",
                        "attributedTo": my_url,
                        "published": now,
                        "to": ["https://tiny.tilde.website/users/insom"],
                        'tag': [
                            {
                                'type': 'Mention',
                                'href': 'https://tiny.tilde.website/users/insom',
                                'name': '@insom@tiny.tilde.website',
                                },
                            ],
                        "attachment": [
                            {
                                "type": "Image",
                                "mediaType": "image/jpeg",
                                "url": "https://example.com/example.png",
                                "name": "example alt text",
                                }
                            ]
                        })))
