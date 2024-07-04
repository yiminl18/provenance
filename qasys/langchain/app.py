'''
    This is the backend server for the RAG-based question answering system.
'''
from flask import Flask, jsonify
from flask_cors import CORS
import logging
from rag import rag

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

@app.route('/api/rag', methods=['GET'])
def process_questions():
    try:
        results = rag()
        return jsonify(results), 200
    except Exception as e:
        logging.error(f"Error processing civic questions: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
