from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_json_files():
    folder_path = '/Users/diegoguzman/Downloads/provenance/front_end/src/interface/resultsData' 
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        if not files:
            return jsonify({'error': 'No JSON files found in the folder'}), 404

        json_data_list = []
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r') as f:
                try:
                    json_content = json.load(f)
                    json_data_list.append({
                        'file_path': file_path,
                        'retrieved_docs': json_content["retrieved_docs"]
                    })
                except json.JSONDecodeError as json_err:
                    print(f"Error decoding JSON from file {file_path}: {json_err}")
                    return jsonify({'error': f"Error decoding JSON from file {file_path}: {json_err}"}), 500

        return (jsonify(json_data_list))

    except Exception as err:
        return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
