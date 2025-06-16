import os
import json
import traceback
from flask import Flask, request, jsonify
from ai import responses

app = Flask(__name__)
clientsList = []

def loadClients(file_path='clients.json'):
    global clientsList
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            clientsList = json.load(f)
    else:
        clientsList = []

def saveClients(file_path='clients.json'):
    with open(file_path, 'w') as f:
        json.dump(clientsList, f, indent=4)

@app.route('/langchain', methods=['POST'])
def langchain_f():
    data = request.json
    msg = data.get("prompt", "")
    reply = responses([{"role": "user", "content": msg}])
    return jsonify({"reply": reply})

@app.route('/clients', methods=['POST'])
def createClientList():
    global clientsList
    try:
        input_data = request.json
        if not input_data:
            return jsonify({'message': 'Missing data'}), 400
        
        age = int(input_data.get('varsta', 0))
        accesses = int(input_data.get('accesari', 0))

        messages = [
            {"role": "system", "content": "You are a helpful assistant who writes detailed responses about client eligibility."},
            {"role": "user", "content": f"The client is {age} years old and has {accesses} visits. Explain if we should register them."}
        ]

        ai_reply = responses(messages)
        print(f"AI response: {ai_reply}")
        eligible = (age > 18 and accesses > 20)

        if eligible:
            existing = next((c for c in clientsList if c.get('email') == input_data.get('email')), None)
            if existing:
                return jsonify({'message': 'Client already exists'}), 400

            clientsList.append(input_data)
            saveClients()
            return jsonify({
                'message': 'Client successfully enrolled',
                'ai_comment': ai_reply
            }), 200
        else:
            return jsonify({
                'message': 'Client did not meet eligibility criteria',
                'ai_comment': ai_reply
            }), 403

    except Exception as e:
        print(f"Exception in createClientList: {e}")
        traceback.print_exc()
        return jsonify({'message': 'Error while processing the client', 'error': str(e)}), 500

@app.route('/clients', methods=['GET'])
def readClients():
    try:
        return jsonify(clientsList), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Could not retrieve clients"}), 500

@app.route('/clients/accesses', methods=['PUT'])
def updateClientAccesses():
    global clientsList
    try:
        client = request.json
        if not client:
            return jsonify({'message': 'Client data missing'}), 400

        email = client.get('email')
        if not email:
            return jsonify({'message': 'Email is required'}), 400

        age = int(client.get('varsta', 0))
        accesses = int(client.get('accesari', 0))

        existing_client = next((c for c in clientsList if c.get('email') == email), None)

        if existing_client is None:
            return jsonify({'message': 'Client not found'}), 404
        eligible = (age > 18 and accesses > 20)

        if not eligible:
            return jsonify({'message': 'Client not eligible due to age or accesses'}), 403
        existing_client['accesari'] = accesses
        existing_client['varsta'] = age
        saveClients()

        return jsonify({'message': 'Client accesses updated successfully'}), 200

    except Exception as e:
        print(f"Exception in updateClientAccesses: {e}")
        traceback.print_exc()
        return jsonify({'message': 'Error while updating client accesses', 'error': str(e)}), 500


@app.route('/clients', methods=['DELETE'])
def removeClient():
    global clientsList
    try:
        client = request.json
        if not client or not client.get('email'):
            return jsonify({'message': 'Missing email in request'}), 400

        email = client['email']
        existing_client = next((c for c in clientsList if c.get('email') == email), None)

        if len(clientsList) > 34:
            if existing_client:
                clientsList.remove(existing_client)
                saveClients()
                return jsonify({'message': 'Client removed due to capacity'}), 200
            else:
                return jsonify({'message': 'Client not found'}), 404
        else:
            return jsonify({'message': 'Capacity not exceeded. No removal needed.'}), 403

    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Server error', 'error': str(e)}), 500

@app.route('/clients/accesses', methods=['GET'])
def get_accesses_info():
    return jsonify({'message': 'GET not supported on /clients/accesses. Use PUT.'}), 405

if __name__ == "__main__":
    loadClients()
    app.run(host='0.0.0.0', port=5000, debug=True)
