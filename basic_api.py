# Simple example of a REST API without use SQLAlchemy and a model
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

videos_put_args = reqparse.RequestParser()  # parases through videos
videos_put_args.add_argument("name", type=str, help="Name of the video is required!",
                             required=True)  # help = error message
videos_put_args.add_argument("views", type=str, help="Views of the video", required=True)
videos_put_args.add_argument("likes", type=str, help="Likes on the video", required=True)

videos = {}


def abort_if_video_null(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not a valid id...")


def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message=f"Video already exists with this id... {videos[video_id]}")

names = {"tim": {"age": 20, "gender": "male"},
         "zach": {"age": 25, "gender": "male"},
         "emily": {"age": 29, "gender": "female"}}


class HelloWorld(Resource):
    def get(self, name):
        return names[name]

class Video(Resource):
    def get(self, video_id):
        abort_if_video_null(video_id)
        return videos[video_id]
    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = videos_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id]

api.add_resource(HelloWorld, '/', '/helloworld/<string:name>')
api.add_resource(Video, '/', '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)