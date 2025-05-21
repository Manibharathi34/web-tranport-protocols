from flask import Flask, render_template
from flask_socketio import SocketIO

socketio = SocketIO()  # create without app to init later

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
   # app.config['SECRET_KEY'] = 'your-secret-key'

    from .sse import sse_bp
    from .longpoll import longpoll_bp
    from .websocket import ws_bp

    app.register_blueprint(sse_bp, url_prefix='/sse')
    app.register_blueprint(longpoll_bp, url_prefix='/lp')
    app.register_blueprint(ws_bp, url_prefix='/ws')

    # Serve the homepage
    @app.route("/")
    def index():
        return render_template("index.html")

    socketio.init_app(app)  # now init with app

    return app
