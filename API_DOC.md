# API DOCUMENTATION

## Shortened URL
POST/shorten

### Request
{
  "url" : "https://example.com"
}

### Response
{
  "short_url" : "https://localhost:5000/abc123"
}

---

## Redirect
GET/
* Redirects to the original url
* stores click counts

---
## Rate limiter
Status: 429
{
  "error":"Rate limit exceeded",
  "retry_after" : 25, "s"
}
