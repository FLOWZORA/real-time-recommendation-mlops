#!/usr/bin/env python3
import sys
import os

# Sanitize sys.argv so invalid port strings like '$PORT' or empty string default to $PORT or 8080
fallback_port = os.environ.get("PORT", "8080")
if not fallback_port.isdigit():
    fallback_port = "8080"

new_argv = []
for i, arg in enumerate(sys.argv):
    if i > 0 and sys.argv[i - 1] == "--port" and not arg.isdigit():
        new_argv.append(fallback_port)
    elif arg in ["$PORT", "${PORT}", "${PORT:-8080}", "${PORT:-8000}"]:
        new_argv.append(fallback_port)
    else:
        new_argv.append(arg)

sys.argv = new_argv

from uvicorn.main import main

if __name__ == "__main__":
    sys.exit(main())
