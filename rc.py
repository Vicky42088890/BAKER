from flask import Flask, request, render_template_string
import requests
import re
import time

app = Flask(__name__)

class FacebookAutoComment:
    def __init__(self):
        self.comment_count = 0

    def post_comment(self, cookie, post_id, comment):
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/89.0.4389.90 Mobile Safari/537.36'
        })

        response = session.get(f'https://mbasic.facebook.com/{post_id}', cookies={'cookie': cookie})
        action_url = re.search(r'method="post" action="(.*?)"', response.text)
        fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
        jazoest = re.search(r'name="jazoest" value="(.*?)"', response.text)

        if action_url and fb_dtsg and jazoest:
            data = {
                'fb_dtsg': fb_dtsg.group(1),
                'jazoest': jazoest.group(1),
                'comment_text': comment
            }
            post_url = 'https://mbasic.facebook.com' + action_url.group(1).replace('&amp;', '&')
            post_response = session.post(post_url, data=data, cookies={'cookie': cookie})

            if post_response.status_code == 200:
                self.comment_count += 1
                print(f"Comment {self.comment_count} posted successfully!")
            else:
                print(f"Failed to post comment. Status code: {post_response.status_code}")
        else:
            print("Unable to find necessary form data.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookie = request.form['cookie']
        post_id = request.form['post_id']
        comment = request.form['comment']
        delay = int(request.form['delay'])

        commenter = FacebookAutoComment()

        for _ in range(5):  # Adjust loop as needed
            commenter.post_comment(cookie, post_id, comment)
            time.sleep(delay)

        return "Comments posted successfully!"

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto Comment Tool - Raghu ACC Rullx Boy</title>
        <style>
            body { background-color: #111; color: #fff; font-family: Arial; text-align: center; padding: 20px; }
            input, button { padding: 10px; margin: 5px; border-radius: 5px; }
            button { background-color: yellow; color: black; cursor: pointer; }
            button:hover { background-color: orange; }
        </style>
    </head>
    <body>
        <h1>Facebook Auto Comment Tool</h1>
        <form method="POST">
            <input type="text" name="cookie" placeholder="Enter Facebook Cookie" required><br>
            <input type="text" name="post_id" placeholder="Enter Post ID" required><br>
            <input type="text" name="comment" placeholder="Enter Comment" required><br>
            <input type="number" name="delay" placeholder="Delay (in seconds)" value="5" required><br>
            <button type="submit">Submit</button>
        </form>
        <footer>Created by Raghu ACC Rullx Boy</footer>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
