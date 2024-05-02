'''from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__, template_folder='templates')
app.config['JSONIFY_RESPONSE_OPTIONS'] = {'max_length': 1000000}  # Set to a higher value

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

    output = stdout.decode('utf-8')  # Assuming the output is in bytes
    #print(output)
    show_charts = True

    response_data = {
        'result': output,
        'show_charts': show_charts
    }

    # Return the response as JSON
    return jsonify(response_data)

    # Parse the sentiment analysis results and return them
    # Modify this part according to your main.py output
    #return render_template('index.html', show_charts = show_charts)

if __name__ == '__main__':
    app.run(debug=True)'''

import streamlit as st
import subprocess

# Function to trigger sentiment analysis
def trigger_sentiment_analysis(youtube_url):
    # Trigger execution of main.py in the background
    process = subprocess.Popen(['python', 'main.py', youtube_url],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8')  # Assuming the output is in bytes

# Streamlit app
def main():
    # Set layout width to 1000 pixels
    st.set_page_config(layout="wide")

    st.title('YouTube Comment Analyzer')
    st.markdown('Understand the Sentiment Behind YouTube Comments')

    # Input fields for YouTube URL and user email
    youtube_url = st.text_input('Paste your YouTube video URL:')
    user_email = st.text_input('Your Email Address:')

    if st.button('Analyze Comments'):
        if youtube_url:
            # Trigger sentiment analysis
            result = trigger_sentiment_analysis(youtube_url)
            with st.expander('Analysis Results'):
                st.write(result)
        else:
            st.error('Please enter a YouTube URL')

if __name__ == '__main__':
    main()
