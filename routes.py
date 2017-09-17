from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_pymongo import ObjectId
from flask_socketio import SocketIO,emit


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'myFirstMB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myFirstMB'

mongo = PyMongo(app)
socketio = SocketIO(app)

@app.route('/add_object', methods=['POST'])
def add_object():
  objects = mongo.db.objects
  name = request.json['name']
  x = request.json['x']
  y = request.json['y']
  z = request.json['z']
  pitch = request.json['pitch']
  yaw = request.json['yaw']
  roll = request.json['roll']
  object_to_add = {
      'name': name,
      'x': x,
      'y': y,
      'z': z,
      'pitch': pitch,
      'yaw': yaw,
      'roll': roll
  }
  result = objects.insert_one(object_to_add)
  object_id = str(result.inserted_id)
  broadcast_add(object_id, object_to_add)
  return jsonify({"id": object_id})

@app.route('/remove_object', methods=['POST'])
def remove_object():
    print "removing"
    object_id = request.json['object_id']
    objects = mongo.db.objects
    result = objects.delete_one({"_id" : ObjectId(object_id)})
    broadcast_delete(object_id)
    return jsonify({"count" : result.acknowledged})

@app.route('/update_object', methods=['POST'])
def update_object():
    objects = mongo.db.objects
    object_id = request.json['object_id']
    name = request.json['name']
    x = request.json['x']
    y = request.json['y']
    z = request.json['z']
    pitch = request.json['pitch']
    yaw = request.json['yaw']
    roll = request.json['roll']
    updated_object = {
        'name': name,
        'x': x,
        'y': y,
        'z': z,
        'pitch': pitch,
        'yaw': yaw,
        'roll': roll
    }
    result = objects.update_one(
        {"_id" : ObjectId(object_id)},
        {'$set': updated_object}
        )
    broadcast_update(object_id, updated_object)
    return jsonify({"id": result.acknowledged})

@app.route('/get_all_objects', methods=['GET'])
def get_all_objects():
    objects = mongo.db.objects
    result = convert_object(objects.find())
    return jsonify({'result' : result})

def convert_object(objects):
    result = []
    for obj in objects:
        obj['_id'] = str(obj['_id'])
        result.append(obj)
    return result
    

def broadcast_add(object_id, updated_object):
    objects = mongo.db.objects
    updated_object['_id'] = str(updated_object["_id"])
    socketio.emit('object_added', (object_id, updated_object))
    print updated_object

@socketio.on('test', namespace='/chat')
def verify(json):
    print('received it: ' + str(json))
    return 'one' 

def broadcast_delete(object_id):
    socketio.emit('object_deleted', object_id)

def broadcast_update(object_id, updated_object):
    updated_object['_id'] = str(updated_object["_id"])
    socketio.emit('object_updated', (object_id, updated_object))

if __name__ == '__main__':
    socketio.run(app, debug=True, port = 80, host = '0.0.0.0')
