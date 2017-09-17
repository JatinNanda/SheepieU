from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_pymongo import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'myFirstMB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myFirstMB'

mongo = PyMongo(app)

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
  result = objects.insert_one({
      'name': name,
      'x': x,
      'y': y,
      'z': z,
      'pitch': pitch,
      'yaw': yaw,
      'roll': roll
      })
  return jsonify({"id": str(result.inserted_id)})

@app.route('/remove_object', methods=['POST'])
def remove_object():
    object_id = request.json['object_id']
    objects = mongo.db.objects
    result = objects.delete_one({"_id" : ObjectId(object_id)})
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
    result = objects.update_one(
        {"_id" : ObjectId(object_id)},
        {'$set': {
            'name': name,
            'x': x,
            'y': y,
            'z': z,
            'pitch': pitch,
            'yaw': yaw,
            'roll': roll
        }})
    print result.matched_count
    return jsonify({"id": result.acknowledged})

@app.route('/get_all_objects', methods=['GET'])
def get_all_objects():
    objects = mongo.db.objects
    result = []
    for obj in objects.find():
        obj['_id'] = str(obj['_id'])
        result.append(obj)
    return jsonify({'result' : result})

if __name__ == '__main__':
    app.run(debug=True)
