from flask import Flask
from config import Config
from controllers.mattermost_controller import bp as mm_bp
from utils.logger import setup_logging
from controllers.mock_controller import mock_bp

app = Flask(__name__)
app.config.from_object(Config)
setup_logging()

# register webhook endpoint
app.register_blueprint(mock_bp)
@app.route("/")
def index():
    return "OK – service is running"


app.register_blueprint(mm_bp, url_prefix="/webhook")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"])
    index
