import os
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from routes.stock_routes import stock_bp
from routes.prediction_routes import prediction_bp
from routes.news_routes import news_bp
from routes.dashboard_routes import dashboard_bp


def create_app():
    app = Flask(__name__)
    CORS(app, origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app"
    ])
    app.register_blueprint(stock_bp,      url_prefix='/api/stock')
    app.register_blueprint(prediction_bp, url_prefix='/api/predict')
    app.register_blueprint(news_bp,       url_prefix='/api/news')
    app.register_blueprint(dashboard_bp,  url_prefix='/api/dashboard')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            "status" : "ok",
            "message": "Stock AI API is running"
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "error"  : "Route not found"
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "success": False,
            "error"  : "Internal server error"
        }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        debug = os.getenv('FLASK_ENV') == 'development',
        port  = int(os.getenv('PORT', 5000)),
        host  = '0.0.0.0'
    )