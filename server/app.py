from flask import Flask, jsonify, request
from flask_cors import CORS

from db.vitalDB import VitalDB, db

from models.models import convo

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    global google_user_id
    google_user_id = data.get('googleUserId')
    
    print(google_user_id)
    
    VitalDB.create_collection(google_user_id)
    
    return google_user_id


@app.route('/form/choosegender', methods=['POST'])
def formGender():
    data = request.json
    global gender
    gender = str(data.get('gender'))

    print('Received gender:', gender)
    
    return gender
    

@app.route('/form/allergies', methods=['POST'])
def formAllergies():
    data = request.json
    global allergies
    allergies = str(data.get('allergies'))

    print(allergies)

    return allergies


@app.route('/form/age', methods=['POST'])
def formAge():
    data = request.json
    global age
    age = str(data.get('age'))

    print(age)
    
    return age


@app.route('/form/problems', methods=['POST'])
def formProblems():
    data = request.json
    global problems
    problems = str(data.get('problems'))

    print(problems)

    return problems


@app.route('/prompt', methods=['POST', 'GET'])
def prompt():
    
    prompt = f'i am {age} year old. i am a {gender}. i have allergies from {allergies}. {problems}. how can i improve it? give me prompt in the format, 1st->allergies, 2nd->things related to allergies to avoid that can trigger, 3rd->medicinal supplements that one can have related to it, 4->seeking professional help. make sure prompt is strictly in this format. i want a description regarding them as well, along each point. dont mention description separately, give more information about everything in the same point itself.'
    convo.send_message(prompt)
    
    response = convo.last.text
    
    VitalDB.store_prompt(google_user_id, prompt, response)
    
    return response


@app.route('/dashboard', methods=['GET'])
def get_user_queries():
    
    collection = db[google_user_id]
    user_queries = list(collection.find({}, {'_id': 0}))  # Exclude _id field from response

    return jsonify(user_queries), 200

if __name__ == "__main__":
  app.run(debug=True)