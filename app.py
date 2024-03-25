from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/mbsa')
def mbsa():
    return render_template('index.html')

@app.route('/api/post_example', methods=['POST'])
def post_example():
    if request.method == 'POST':
        # Get the user input from the request
        user_input = request.form.get('user_input')
        
        # Return the user input as a JSON response
        return jsonify({'user_input': user_input}), 200
    else:
        # Return an error if the request method is not POST
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
