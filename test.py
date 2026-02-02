from flask import Flask

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def home():
    return "Hello, Flask! 🚀"

# Another route
@app.route('/about')
def about():
    return "This is the About Page."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
