from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd


app = Flask(__name__)
api = Api(app)

class Students(Resource):
    def get(self):
        data = pd.read_csv('students.csv')
        data = data.to_dict('records')
        
        return {'data' : data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        args = parser.parse_args()

        data = pd.read_csv('students.csv')

        new_data = pd.DataFrame({
            'id'      : [args['id']],
            'first_name'      : [args['first_name']],
            'last_name'      : [args['last_name']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('students.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('first_name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('students.csv')

        data = data[data['id'] != args['id']]

        data.to_csv('students.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200

api.add_resource(Students, "/students")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)