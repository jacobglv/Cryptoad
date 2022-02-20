import boto3
from flask import Flask, json
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('wallet')
parser.add_argument('change_funds')
parser.add_argument('bet_amount')
parser.add_argument('user')
parser.add_argument('pass')
parser.add_argument('login_token')
parser.add_argument('bet_type')

TABLE_NAME = 'cryptoad_info'
PART_KEY = 'cryptoad'

def add_header(data):
    response = json.jsonify({'data': data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

class Login(Resource):
    def get(self):
        args = parser.parse_args()
        print(args)
        response = table.get_item(
            Key={
                PART_KEY: str(args['user'])
            }
        )

        if 'Item' in response and response['Item']['pass'] == args['pass']:
            data = True
            response = json.jsonify({'data': data})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        elif 'Item' in response and response['Item']['pass'] != args['pass'] and args['pass'] is not None:
            data = False
            response = json.jsonify({'data': data})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            if args['pass']:
                table.put_item(
                        Item = {
                            PART_KEY: args['user'],
                            'pass': args['pass'],
                            'wallet': random.randint(100000,999999),
                            'wallet_bal': 0
                        } 
                    )
                data = 'Unregistered user, creating account... '
                response = json.jsonify({'data': data})
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            else:
                data = 'No Password'
                response = json.jsonify({'data': data})
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
    pass

class Wallet(Resource):
    def get(self):
        args = parser.parse_args()
        response = table.get_item(
            Key={
                PART_KEY: str(args['user'])
            }
        )
        if 'Item' in response and response['Item']['pass'] == args['pass'] and int(args['change_funds']) > 0:
            new_wal_val = int(args['change_funds']) + int(response['Item']['wallet_bal'])
            table.update_item(
                Key={
                    PART_KEY: str(args['user']),
                },
                UpdateExpression='SET wallet_bal = :val1',
                ExpressionAttributeValues={
                    ':val1': new_wal_val
                }
            )
            response = table.get_item(
                Key={
                    PART_KEY: str(args['user'])
                }
            )
            return {'data': 'Funds Added To Wallet:' + str(args['change_funds']) + ' Funds total: ' +  str(new_wal_val)}, 200
        elif 'Item' in response and response['Item']['pass'] == args['pass'] and int(args['change_funds']) < 0:
            return {'data': 'NYI, Will be Account Withdrawal'}, 200

class Gamba(Resource):
    pass
        

class Gamba_Info(Resource):

    def post(self):
        args = parser.parse_args()
        
    def get_rates():
        rates = {
            'mult_per_lvl': 1.5,
        }
        return rates, 200



api.add_resource(Login, '/login')  # '/users' is our entry point for Users
api.add_resource(Wallet, '/wal')
api.add_resource(Gamba, '/bet') 

if __name__ == '__main__':
    app.run(host="0.0.0.0")  # run our Flask app
