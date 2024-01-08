import json
from flask import Flask, jsonify, request

from model.tweet import Tweet

tweets = []

app = Flask(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tweet):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong'})


@app.route('/tweet', methods=['POST'])
def create_tweet():
    """{"body": "Hello World", "author": "@Dastan"}
    """
    tweet_json = request.get_json()
    tweet = Tweet(tweet_json['body'], tweet_json['author'])
    tweets.append(tweet)
    return json.dumps({'status': 'success', 'id': tweet.id}, cls=CustomJSONEncoder)


@app.route('/tweet', methods=['GET'])
def read_tweets():
    # Создаем список твитов с их идентификаторами
    tweets_data = [{'id': tweet.id, 'body': tweet.body, 'author': tweet.author} for tweet in tweets]
    return json.dumps({'tweets': tweets_data}, cls=CustomJSONEncoder)


@app.route('/tweet/<string:tweet_id>', methods=['PUT'])
def update_tweet(tweet_id):
    tweet_json = request.get_json()
    new_body = tweet_json.get('body')

    # Найти твит по tweet_id и обновить его
    for tweet in tweets:
        if tweet_id == tweet.id:
            tweet.update(new_body)
            return json.dumps({'status': 'success'}, cls=CustomJSONEncoder)

    return jsonify({'error': 'Tweet not found'}), 404


@app.route('/tweet/<string:tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id):
    # Найти твит по tweet_id и удалить его
    for tweet in tweets:
        if tweet_id == tweet.id:
            tweets.remove(tweet)
            return json.dumps({'status': 'success'}, cls=CustomJSONEncoder)

    return jsonify({'error': 'Tweet not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
