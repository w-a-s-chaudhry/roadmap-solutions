# Caching Proxy

A command-line caching proxy server: forwards requests to an origin
server, caches responses in Redis, and serves identical subsequent
requests from cache.

Project page: https://roadmap.sh/projects/caching-server

## Requirements

- Python 3 with the `redis` package (`pip install redis`)
- A Redis server reachable at `redis://localhost:6379/0`
  (this project was developed against Redis running in a local
  Docker container named `redis` — `docker start redis`)

## Usage

Start the proxy, forwarding to an origin server:

```bash
python caching_proxy.py --port 3000 --origin http://dummyjson.com
```

Requests to the proxy are forwarded to the origin and cached:

```bash
curl -i http://localhost:3000/products
```

- First request: `X-Cache: MISS` (fetched from origin, stored in
  cache).
- Identical subsequent request: `X-Cache: HIT` (served from Redis,
  origin not contacted).

Clear the cache:

```bash
python caching_proxy.py --clear-cache
```

## Manual test walkthrough

1. Start Redis (`docker start redis`) and confirm it's running.
2. Start the proxy against a real origin:
   ```bash
   python caching_proxy.py --port 3000 --origin \
       https://jsonplaceholder.typicode.com
   ```
3. Request an endpoint twice and compare:
   ```bash
   curl -i http://localhost:3000/todos/1
   curl -i http://localhost:3000/todos/1
   ```
   The first response has `X-Cache: MISS`; the second has
   `X-Cache: HIT`. Status, headers, and body match between the two.
4. Clear the cache and repeat step 3 — the request should be a
   `MISS` again, confirming the cache was actually wiped:
   ```bash
   python caching_proxy.py --clear-cache
   ```

## Known limitations

- Only `GET` requests are proxied/cached.
- Origin `Transfer-Encoding`/`Content-Length` headers are dropped and
  `Content-Length` is recomputed from the actual (already-read) body,
  so chunked origin responses are handled correctly instead of
  hanging or truncating the client.
