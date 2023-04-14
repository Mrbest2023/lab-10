from flask import Flask, request, jsonify

from main import process1, process2


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})
@app.route('/process1')
def process1()
    data= request.get_json()
return jsonify(process1(data))
@app.route('/process2')
def process2()
    data=request.get_json()
return jsonify(process2(data))

# TODO: Create a flask app with two routes, one for each function.
# The route should get the data from the request, call the function, and return the result.
