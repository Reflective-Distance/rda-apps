import sys
import urllib.request
import urllib.error

def main():
    if len(sys.argv) != 2:
        print("Usage: python healthcheck.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                sys.exit(0)
            else:
                print(f"Health check failed: status {response.status}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"Health check failed: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

    sys.exit(1)

if __name__ == "__main__":
    main()
