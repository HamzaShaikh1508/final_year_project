from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap():
    youtube_url = request.form['youtube_url']
    user_email = request.form['user_email']

    # Trigger execution of main.py in the background
    process = subprocess.Popen(['python', 'main.py', youtube_url],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Parse the sentiment analysis results and return them
    # Modify this part according to your main.py output
    return render_template('index.html', show_charts=True)

if __name__ == '__main__':
    app.run(debug=True)
