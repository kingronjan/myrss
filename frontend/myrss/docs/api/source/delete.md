endpoint: delete /feed-source/{source_id}


request example:

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/feed-source/1' \
  -H 'accept: application/json'
```

response example:

```json
{
  "data": null,
  "message": "Source deleted successfully",
  "code": 0
}
```
