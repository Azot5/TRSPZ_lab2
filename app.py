from flask import Flask, jsonify, request, abort

app = Flask(__name__)

users = {}
categories = {}
records = {}
user_counter = 1
category_counter = 1
record_counter = 1

@app.route('/user', methods=['POST'])
def create_user():
    global user_counter
    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "User name is required"}), 400
    user_id = user_counter
    users[user_id] = {"id": user_id, "name": data['name']}
    user_counter += 1
    return jsonify(users[user_id]), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id])

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 204

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

@app.route('/category', methods=['POST'])
def create_category():
    global category_counter
    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Category name is required"}), 400
    category_id = category_counter  
    categories[category_id] = {"id": category_id, "name": data['name']}
    category_counter += 1
    return jsonify(categories[category_id]), 201

@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values()))

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id not in categories:
        return jsonify({"error": "Category not found"}), 404
    del categories[category_id]
    return jsonify({"message": "Category deleted"}), 204

@app.route('/record', methods=['POST'])
def create_record():
    global record_counter
    data = request.get_json()
    if 'user_id' not in data or 'category_id' not in data or 'amount' not in data:
        return jsonify({"error": "Record must include user_id, category_id, and amount"}), 400
    if data['user_id'] not in users or data['category_id'] not in categories:
        return jsonify({"error": "User or category not found"}), 404
    record_id = record_counter
    records[record_id] = {
        "id": record_id,
        "user_id": data['user_id'],
        "category_id": data['category_id'],
        "amount": data['amount'], 
        "timestamp": data.get("timestamp", "2024-11-06T00:00:00Z")
    }
    record_counter += 1
    return jsonify(records[record_id]), 201

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    if record_id not in records:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(records[record_id])

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id not in records:
        return jsonify({"error": "Record not found"}), 404
    del records[record_id]
    return jsonify({"message": "Record deleted"}), 204

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    filtered_records = [
        record for record in records.values()
        if (user_id is None or record['user_id'] == user_id) and
           (category_id is None or record['category_id'] == category_id)
    ]
    
    if user_id is None and category_id is None:
        return jsonify({"error": "user_id or category_id parameter is required"}), 400
    
    return jsonify(filtered_records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
