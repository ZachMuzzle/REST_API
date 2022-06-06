# STOPPED VIDEO @30:31
# API REST using a model for the database.
from flask import Flask, request
from flask_restful import Resource, Api, reqparse,abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite://database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

db.create_all() #Only do this once after models are created

videos_put_args = reqparse.RequestParser() #parases through videos
videos_put_args.add_argument("name",type=str, help="Name of the video is required!", required=True) #help = error message
videos_put_args.add_argument("views",type=str, help="Views of the video", required=True)
videos_put_args.add_argument("likes",type=str, help="Likes on the video", required=True)

videos_update_args = reqparse.RequestParser()
videos_update_args.add_argument("name",type=str, help="Name of the video is required!") #help = error message
videos_update_args.add_argument("views",type=str, help="Views of the video")
videos_update_args.add_argument("likes",type=str, help="Likes on the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields) # Take return value and put into json format
    def get(self, video_id): #get data
        result = VideoModel.query.filter_by(id=video_id).first() #filter all videos by id, return first entry
        if not result:
            abort(404, message="Video could be found with an id...")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id): #add data
        args = videos_put_args.parse_args() #dict stores all values passed in
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id is taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video) # add video to db temporarily
        db.session.commit() # add video to db permanently
        return video

    @marshal_with(resource_fields)
    def patch(self,video_id): #update data
        args = videos_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist, cannot update...")
        if args["name"]: # Tells if key is not a None value
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']

        db.session.commit() # Only need to commit to database since it is already added.

        return result


api.add_resource(Video, '/', '/video/<int:video_id>')
if __name__ == '__main__':
    app.run(debug=True)