# Author:      Wajid Ali Saleem Chaudhry
# Description: Caching proxy CLI entry point — parses arguments and
#              will start the proxy server or clear the cache.

import argparse
import redis
import sys
import http.server
import urllib.request, urllib.parse
import json


_redis_client = redis.from_url("redis://localhost:6379/0")

# --- CLI ---


# Build and return the argument parser for the caching proxy CLI
def build_parser():
    parser = argparse.ArgumentParser(prog="caching-proxy")
    parser.add_argument("--port", type=int)
    parser.add_argument("--origin", type=str)
    parser.add_argument("--clear-cache", action="store_true")
    return parser


# --- Cache ---


# Wipe all cached entries from redis
def clear_cache():
    try:
        _redis_client.flushdb()
        print("Cache Cleared Successfully")
    except redis.RedisError as e:
        print(f"Error: {e}")


# --- Proxy ---


# Headers that describe framing of the *original* transfer and no
# longer apply once the body has been fully read into memory
_FRAMING_HEADERS = {"transfer-encoding", "content-length"}


# Send status + headers + body, dropping framing headers that no
# longer match `body_bytes` (e.g. Transfer-Encoding: chunked, stale
# Content-Length) and recomputing Content-Length from the real bytes
def send_response_with_body(handler, status, headers, body_bytes,
                             cache_flag):
    handler.send_response(status)
    for name, value in headers.items():
        if name.lower() in _FRAMING_HEADERS:
            continue
        handler.send_header(name, value)
    handler.send_header("Content-Length", str(len(body_bytes)))
    handler.send_header("X-Cache", cache_flag)
    handler.end_headers()
    handler.wfile.write(body_bytes)


# Handles one incoming HTTP request, serving from cache or origin
class ProxyHandler(http.server.BaseHTTPRequestHandler):
    # Serve a GET request from cache if present, else fetch + store it
    def do_GET(self):
        key = f"cache:{self.path}"
        try:
            cached = _redis_client.get(key)
            if cached:
                data = json.loads(cached)
                send_response_with_body(
                    self,
                    data["status"],
                    data["headers"],
                    data["body"].encode(),
                    "HIT",
                )
                return
        except redis.RedisError as e:
            print(f"Error: {e}")

        url = urllib.parse.urljoin(self.origin, self.path)
        response = urllib.request.urlopen(url)
        status = response.status
        headers = dict(response.getheaders())
        body = response.read().decode()

        try:
            _redis_client.set(
                key,
                json.dumps(
                    {
                        "status": status,
                        "headers": headers,
                        "body": body,
                    }
                ),
            )
        except redis.RedisError as e:
            print(f"Error: {e}")

        send_response_with_body(
            self, status, headers, body.encode(), "MISS"
        )


# Start an HTTP server on the given port using ProxyHandler
def start_server(port, origin):
    ProxyHandler.origin = origin
    server = http.server.HTTPServer(("", port), ProxyHandler)
    print(f"Serving on port {port}, forwarding to {origin}")
    server.serve_forever()


# --- CLI ---


# Parse CLI args and dispatch to the right behavior
def main():
    args = build_parser().parse_args()

    if args.clear_cache:
        clear_cache()
        return

    if args.port is None:
        print("Error: port not supplied")
        sys.exit(2)
    if args.origin is None:
        print("Error: origin not supplied")
        sys.exit(2)

    start_server(args.port, args.origin)


if __name__ == "__main__":
    main()
