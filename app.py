from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from peewee import *

db = "something.db"
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class user(BaseModel):
	id = AutoField(primary_key=True)
	name = CharField()
	username = CharField(unique=True)
	password = CharField()

class todo(BaseModel):
	id = AutoField(primary_key=True)
	id_user = ForeignKeyField(user)
	kegiatan = CharField()

def create_tables():
	with database:
		database.create_tables([user,todo])

app = Flask(__name__)
api = Api(app)

class resource_user(Resource):
    def get(self):
    	parser = reqparse.RequestParser()
    	parser.add_argument('id_user', type=int, help='iki ngunu id_user, tipe datane int')
    	parser.add_argument('username', type=str, help='iki username')
    	args = parser.parse_args()
    	if args['id_user']  and args['username']:
    		return jsonify({"message":"Tolong pilih salah satu antara username atau id_user"})
    	elif args['id_user']:
    		get_user = list(user.select().where(user.id == args['id_user']).dicts())
    		return {'data': get_user,"message":'data e kejupuk kabeh'}
    	elif args['username']:
	    	get_user = list(user.select().where(user.username == args['username']).dicts())
	    	return {'data': get_user,"message":'data e kejupuk kabeh'}
    	else:
	    	get_user = list(user.select().dicts())
    		return {'data': get_user,"message":'data e kejupuk kabeh'}

    def post(self):
    	name = request.form['name']
    	username = request.form['username']
    	password = request.form['password']

    	user.create(name=name,
    		username=username,
    		password=password)
    	
    	return jsonify({'message':"user created"})

    def put(self):
    	parser = reqparse.RequestParser()
    	parser.add_argument('id_user', type=int, help='iki ngunu id_user perlu. dadi katutno cuk, tipe datane int', required=True)
    	args = parser.parse_args()
    	cek_user = user.select().where(user.id == args['id_user'])
    	if cek_user.exists():
    		password = request.form['password']

    		update_user = user.update(password=password).where(user.id == args['id_user'])
    		update_user.execute()
    		return jsonify({"message":"User updated"})
    	else:
    		return jsonify({'message':'user not found'})

class resource_todo(Resource):
	def get():
		return 'iki get tekok todo'

api.add_resource(resource_user, '/api/user/')
api.add_resource(resource_todo, '/api/todo/')


if __name__ == '__main__':
	create_tables()
	app.run(debug=True)