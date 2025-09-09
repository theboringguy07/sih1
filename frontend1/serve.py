import http.server
import os
import socketserver
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import List


PROJECT_ROOT = Path(__file__).resolve().parent
DIST_DIR = PROJECT_ROOT / 'dist'
DEFAULT_PORT = int(os.environ.get('PORT', '8000'))


def run_cmd(cmd: List[str], *, cwd: Path | None = None, shell: bool = False) -> int:
    try:
        print('> ' + ' '.join(cmd))
        return subprocess.call(cmd, cwd=str(cwd or PROJECT_ROOT), shell=shell)
    except FileNotFoundError as exc:
        print(f"Command not found: {cmd[0]}\n{exc}")
        return 1


def ensure_node_available() -> None:
    code = run_cmd(['node', '-v'])
    if code != 0:
        print("Node.js is required. Install from https://nodejs.org and re-run: py serve.py")
        sys.exit(1)
    run_cmd(['npm', '-v'])


def install_dependencies(skip_install: bool) -> None:
    if skip_install:
        return
    lockfile = PROJECT_ROOT / 'package-lock.json'
    if lockfile.exists():
        code = run_cmd(['npm', 'ci'])
    else:
        code = run_cmd(['npm', 'install'])
    if code != 0:
        sys.exit(code)


def build_prod() -> None:
    code = run_cmd(['npm', 'run', 'build'])
    if code != 0:
        sys.exit(code)


class SPARequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        # Cleaner console logs
        sys.stdout.write("%s - - [%s] " % (self.client_address[0], self.log_date_time_string()))
        sys.stdout.write((format % args) + "\n")

    def send_head(self):
        # Try normal file; on 404 serve index.html for SPA routes
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            index = os.path.join(path, 'index.html')
            if os.path.exists(index):
                self.path = self.path.rstrip('/') + '/index.html'
        try:
            return super().send_head()
        except Exception:
            # Fallback to root index.html
            self.path = '/index.html'
            return super().send_head()


def open_browser_when_ready(url: str):
    def _open():
        try:
            webbrowser.open_new(url)
        except Exception:
            pass
    threading.Timer(1.0, _open).start()


def serve_dist(port: int):
    handler = SPARequestHandler
    with socketserver.TCPServer(('', port), handler) as httpd:
        url = f'http://localhost:{port}'
        print(f"Serving dist at {url}")
        open_browser_when_ready(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down...')


def run_dev_server():
    # Start Vite dev server and pass through output
    print('Starting Vite dev server...')
    proc = subprocess.Popen(['npm', 'run', 'dev', '--', '--host'], cwd=str(PROJECT_ROOT))
    # Give Vite a moment to boot
    time.sleep(1.2)
    open_browser_when_ready('http://localhost:5173')
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()


def parse_args():
    import argparse
    p = argparse.ArgumentParser(description='Serve or develop the AI Internship Engine UI')
    p.add_argument('--dev', action='store_true', help='Run Vite dev server instead of static build server')
    p.add_argument('--port', type=int, default=DEFAULT_PORT, help='Port for static server (build mode)')
    p.add_argument('--skip-install', action='store_true', help='Skip npm install/ci step')
    return p.parse_args()


def main():
    args = parse_args()
    ensure_node_available()
    if args.dev:
        install_dependencies(skip_install=args.skip_install)
        return run_dev_server()
    # build + serve dist
    install_dependencies(skip_install=args.skip_install)
    build_prod()
    serve_dist(args.port)


if __name__ == '__main__':
    main()


