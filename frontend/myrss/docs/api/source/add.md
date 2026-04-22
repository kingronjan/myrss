## add source

endpoint: post /feed-source/add

request example:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/feed-source/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "1111",
  "description": "2222"
}'
```

response example:

```json
{
  "deleted": false,
  "created_at": "2026-04-22T05:44:23",
  "url": "1111",
  "sync_status": 4,
  "updated_at": "2026-04-22T05:44:23",
  "id": 6,
  "description": "2222",
  "sync_msg": null
}
```
