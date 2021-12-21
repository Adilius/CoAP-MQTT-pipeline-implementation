from flask import Flask,  render_template
import sys

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

# Default route
@app.route("/")
def hello():
    return render_template('index.html')
    return "<h1 style='color:blue'>Hello There!</h1>"

def run_server():
    print("\u001b[33;1m" + f"Web server | Starting on port {PORT} " + "\u001b[0m")
    app.run(host=HOST, port=PORT)
    

if __name__ == "__main__":
    run_server()