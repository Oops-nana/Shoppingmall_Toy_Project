from flask.scaffold import F
from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import re

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbsparta

def phone_valid_check(phone):
    check = re.search("(\d{3}).(\d{4}).(\d{4})",phone)
    if(check):
        return True
    else:
        return False
        

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop', methods = ['GET'])
def road_list():
    order_data = list(db.shop.find({}, {'_id' : False}))
    
    return jsonify({'data' : order_data})

@app.route('/shop', methods = ['POST'])
def save():
    name = request.form['client']
    amount = request.form['amount']
    address = request.form['address']
    phone = request.form['phone_num']

    if(phone_valid_check(phone)):
        
        dat = {
            'client' : name,
            'amount' : amount,
            'address' : address,
            'phone' : phone
        }
        db.shop.insert_one(dat);
        return jsonify({'msg' : 'post'})
    else:
        print('invalid phone format!')
        return jsonify({'valid' : False})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)