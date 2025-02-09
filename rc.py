from flask import Flask, request, render_template_string
import requests
import re
import time

app = Flask(__name__)

class FacebookCommenter:
    def __init__(self):
        self.comment_count = 0

    def comment_on_post(self, cookie, post_id, comment):
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        })

        response = session.get(f'https://mbasic.facebook.com/{post_id}', cookies={'cookie': cookie})
        action_url = re.search('method="post" action="(/a/comment/.*?)"', response.text)
        fb_dtsg = re.search('name="fb_dtsg" value="(.*?)"', response.text)
        jazoest = re.search('name="jazoest" value="(.*?)"', response.text)

        if action_url and fb_dtsg and jazoest:
            data = {
                'fb_dtsg': fb_dtsg.group(1),
                'jazoest': jazoest.group(1),
                'comment_text': comment
            }
            post_url = f"https://mbasic.facebook.com{action_url.group(1)}"
            post_response = session.post(post_url, data=data, cookies={'cookie': cookie})

            if post_response.status_code == 200:
                self.comment_count += 1
                return f"✅ Comment {self.comment_count} done!"
            else:
                return f"❌ Failed to comment (Status Code: {post_response.status_code})"
        else:
            return "⚠️ Error: Unable to find form data!"

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        cookie = request.form['cookie']
        post_id = request.form['post_id']
        comment = request.form['comment']

        commenter = FacebookCommenter()
        message = commenter.comment_on_post(cookie, post_id, comment)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto Comment by Raghu ACC Rullx Boy</title>
        <style>
            body { background-color: #111; color: white; font-family: Arial; text-align: center; padding: 20px; }
            input, button { padding: 10px; margin: 5px; border-radius: 5px; border: none; }
            button { background-color: yellow; color: black; cursor: pointer; }
            button:hover { background-color: orange; }
            .container { background: #222; padding: 20px; border-radius: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Auto Comment Tool</h1>
            <form method="POST">
                <input type="text" name="cookie" placeholder="Enter Facebook Cookie" required><br>
                <input type="text" name="post_id" placeholder="Enter Post ID" required><br>
                <input type="text" name="comment" placeholder="Enter Comment" required><br>
                <button type="submit">Submit</button>
            </form>
            <p>{{ message }}</p>
        </div>
    </body>
    </html>
    """, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
