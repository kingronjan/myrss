## sync source's feed

endpoint: post /feed-source/sync?source_id=

response example:
```json
{
  "data": null,
  "message": "Task created successfully",
  "code": 0
}
```

## sync status

endpoint: get feed-source/sync-status?source_id=

request example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/feed-source/sync-status?source_id=2' \
  -H 'accept: application/json'
```

response example:

```json
{
  "id": 2,
  "updated_at": "2026-04-21T07:50:41",
  "description": "阮一峰的网络日志",
  "sync_msg": "",
  "url": "https://feeds.feedburner.com/ruanyifeng",
  "deleted": false,
  "created_at": "2026-04-19T05:38:50",
  ",": 3  // 0 pending, 1 running, 2 success, 3 failed, 4 unset
}
```
