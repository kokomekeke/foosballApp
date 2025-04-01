from server import create_app
from server.api.routes import api

app = create_app()

app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run()
