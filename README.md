# custom-http-server
A polyglot collection of HTTP servers built from the ground up using only standard libraries and sockets. No frameworks, just raw TCP and RFC compliance.  **Goal:** To understand the inner workings of the web by implementing the protocol specification manually across different programming languages. 

## Python HTTP Server

Minimal HTTP server with static file serving and `.env` support. Run `./scripts/start.sh`, configure `.env` with `PORT` and `STATIC_DIR`. Endpoints: `/` (static files), `/api/env-info` (JSON with env vars).
