endpoint: get /feed

request example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/feed/?source_id=4' \
  -H 'accept: application/json'
```

response example:
```json
[
  {
    "deleted": false,
    "updated_at": "2026-04-19T14:15:08",
    "id": "https://lucumr.pocoo.org/2026/4/11/the-center-has-a-bias/",
    "title": "The Center Has a Bias",
    "summary": "<p>Whenever a new ... than AI coding agents.</p>\n...",
    "published": "2026-04-11T00:00:00",
    "is_read": false,
    "created_at": "2026-04-19T14:15:08",
    "source_id": 4,
    "link": "https://lucumr.pocoo.org/2026/4/11/the-center-has-a-bias/",
    "is_sent": false
  },
]
```
