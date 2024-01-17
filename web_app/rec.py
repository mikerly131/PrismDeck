from flask import Blueprint, render_template, request, jsonify
from pyspark.sql import SparkSession
from flask_login import current_user, login_required
from .models import MovieRating, Movie
from .recommendation_model import load_als_model, get_recommendations

rec = Blueprint('rec', __name__)


@rec.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        # Specify the path where your ALS model is saved
        als_model_path = "/Users/joey/Downloads/model_training"

        # Load ALS model
        spark = SparkSession.builder.appName("PrismDeck").getOrCreate()
        als_model = load_als_model(als_model_path)

        # Extract user ID from the request data
        user_id = request.json['user_id']

        # Get recommendations using the ALS model
        result = get_recommendations(als_model, spark, user_id)

        # Stop the spark session
        spark.stop()

        return jsonify({'recommendations': result})
    except Exception as e:
        return jsonify({'error': str(e)})
