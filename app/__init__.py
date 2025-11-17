from flask import Flask
import json

def create_app():
    app = Flask(__name__)
    app.config.from_file("config.json", load=json.load)
    
    @app.route('/')
    def hello():
        return "Hello, Flask!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)