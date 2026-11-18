# Configuration and error handling

[README](../README.md) · [Examples](../examples/README.md) · [Responses](responses.md)

## Runtime and client

Requires Python 3.10+.

`Client(key, base_url="https://api.uptimescout.com", timeout=30)`. Timeout is in seconds. Named helpers and `request(method, **params)` are available.

The API base URL is an origin without `/v1`; the client adds the versioned method path. Override it only for a server you trust with your license key. Redirects are disabled in the default clients.

## Response and error types

Python dictionaries; errors use `UptimeScoutError.status` and `.payload`. Network/timeout errors may also raise standard urllib exceptions.

[HTTP status handling](responses.md#errors). These clients do not automatically retry. Respect HTTP 429; apply a bounded delay with jitter if you implement retries. Some clients expose only the error status/message rather than HTTP headers; do not assume a `retry_after` property exists.

## Region and language

Pass `region=GB` and `lang=en` explicitly for reproducible examples. Region and language are independent. Use `available_regions` to discover current coverage.

## Pagination and batches

Use `limit` and zero-based `offset`. After processing a response, read `next_offset`; stop on null or when your page budget is reached. Each extra page is another successful request. Batch requests use comma-separated service IDs over HTTP and are limited by the selected plan.

## Credentials

Load the key from `UPTIMESCOUT_LICENSE_KEY` in your server environment. Keep it out of source control, browser JavaScript, logs and issue reports. Example scripts check the key before making a request; `--help` requires no key.

## Transport and request budget

Reuse a client within your application, set a suitable timeout and bound concurrency to your plan. A fresh response can contain an old observation: inspect `stale` and `observed_at`, not just HTTP success. See [request accounting](../README.md#plans-and-request-accounting).
