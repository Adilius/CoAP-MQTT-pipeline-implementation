from flask import Flask,  render_template
from turbo_flask import Turbo
from .. import cache_manager
import sys, threading, time

HOST = '0.0.0.0'
PORT = 5000

# Only log errors from Werkzeug
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Suppress Flask start message
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

# Create flask app
app = Flask(__name__)
turbo = Turbo(app)

# Default route
@app.route("/")
def hello():
    topics = cache_manager.read_cache()
    return render_template('index.html', topics=topics)

@app.context_processor
def inject_load():
    topics = cache_manager.read_cache()
    return topics

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            topics = cache_manager.read_cache()
            turbo.push(turbo.replace(render_template('topics.html', topics=topics),'topics'))

def run_server():
    print("\u001b[33;1m" + f"Web server | Starting on port {PORT} " + "\u001b[0m")
    app.run(host=HOST, port=PORT)

if __name__ == "__main__":
    run_server()