from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

# Cookie, Post ID, Comment, और Time.txt पढ़ना
with open('cookie.txt', 'r') as file:
    cookie = file.read().strip()

with open('postid.txt', 'r') as file:
    post_id = file.read().strip()

with open('comment.txt', 'r') as file:
    comment = file.read().strip()

with open('time.txt', 'r') as file:
    delay = int(file.read().strip())

# HTML इंटरफेस
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment Tool</title>
</head>
<body style="background-color: black; text-align: center; color: white;">
    <h2>Auto Comment Tool</h2>
    <form method="POST">
        <input type="text" name="cookie" placeholder="Enter Facebook Cookie" required><br><br>
        <input type="text" name="post_id" placeholder="Enter Post ID" required><br><br>
        <input type="text" name="comment" placeholder="Enter Comment" required><br><br>
        <button type="submit" style="background-color: yellow;">Submit</button>
    </form>
</body>
</html>
"""

# कमेंट पोस्ट करने का फंक्शन
def post_comment(cookie, post_id, comment):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {'message': comment, 'access_token': cookie}
    response = requests.post(url, data=payload)
    return response.status_code, response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookie = request.form['cookie']
        post_id = request.form['post_id']
        comment = request.form['comment']

        while True:
            status_code, response = post_comment(cookie, post_id, comment)
            if status_code == 200:
                print("Comment Posted Successfully!")
            else:
                print(f"Error: {response}")
            time.sleep(delay)

    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
