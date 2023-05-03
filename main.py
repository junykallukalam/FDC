import os
import logging
from logging import StreamHandler
from waitress import serve
from flask import Flask, request, jsonify, send_from_directory
import requests
import json

app = Flask(__name__)

FOODDATA_API_URL = 'https://api.nal.usda.gov/fdc/v1'
API_KEY = '85ep9vdHhqKgk7mhQlFVKOVzoztpW7fwGCVSfKx2'

app.logger.handlers.clear()

handler = StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

app.logger.info("Application started")


def search_foods(query):
  url = f"{FOODDATA_API_URL}/foods/search?api_key={API_KEY}&query={query}"
  response = requests.get(url)

  if response.status_code == 200:
    result = response.json()
    return result
  else:
    raise Exception(f"Error: {response.status_code}, {response.text}")


def get_food_details(fdc_id):
  url = f"{FOODDATA_API_URL}/food/{fdc_id}?api_key={API_KEY}"
  response = requests.get(url)

  if response.status_code == 200:
    result = response.json()
    return result
  else:
    raise Exception(f"Error: {response.status_code}, {response.text}")


# test changes
@app.route('/food', methods=['GET'])
def fetch_food_data():
  app.logger.info("Fetching food data")
  query = request.args.get('query')

  try:
    foods = search_foods(query)
    return jsonify(foods)
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@app.route('/food/<int:fdc_id>', methods=['GET'])
def fetch_food_details(fdc_id):
  app.logger.info("Fetching food details")

  try:
    food_details = get_food_details(fdc_id)
    return jsonify(food_details)
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@app.route('/')
def serve_homepage():
  app.logger.info("Serving homepage")
  return send_from_directory('.', 'index.html', mimetype='text/html')


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  app.logger.info("Serving ai-plugin.json")
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  app.logger.info("Serving openapi.yaml")
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
