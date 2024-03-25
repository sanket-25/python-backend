from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, world!'

@app.route("/mbsa")
def mbsa():
    return render_template('index.html')

@app.route('/api/post', methods=['POST'])
def post_api():
    if request.method == 'POST':
        # Get the user's input from the request data
        user_input = request.json.get('input')
        
        # Return the user's input in the response
        return jsonify({'input': user_input}), 200
    else:
        return jsonify({'message': 'Method not allowed'}), 405

if __name__ == "__main__":
    app.run(debug=True)
