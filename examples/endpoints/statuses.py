"""One UptimeScout request. --help sends no request."""
import argparse
import json
import os
import sys
from uptimescout import Client, UptimeScoutError


def main():
    parser = argparse.ArgumentParser(description='Check several services in one call')
    parser.add_argument('--region', default='GB', help='Observation country code')
    parser.add_argument('--lang', default='en', help='Service-description language')
    parser.add_argument('--services', default='github,cloudflare')
    args = parser.parse_args()
    key = os.environ.get('UPTIMESCOUT_LICENSE_KEY', '')
    if not key:
        parser.error('Set UPTIMESCOUT_LICENSE_KEY in your environment')
    try:
        response = Client(key, base_url=os.environ.get('UPTIMESCOUT_BASE_URL', 'https://api.uptimescout.com')).request('statuses', **vars(args))
        print(json.dumps(response, indent=2, ensure_ascii=False))
    except UptimeScoutError as error:
        print(f'UptimeScout HTTP {error.status}; check your key, plan and parameters.', file=sys.stderr)
        return 1
    except Exception:
        print('Connection, timeout or response error; check the endpoint and network.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
