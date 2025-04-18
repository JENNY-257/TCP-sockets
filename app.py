from flask import Flask, render_template, request
import socket

app = Flask(__name__)

def send_request_to_server(message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9999))
        client.send(message.encode())
        response = client.recv(4096).decode()
        client.close()
        return response
    except Exception as e:
        return f"Error connecting to server: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        action = request.form.get('action')
        first = request.form.get('first')
        last = request.form.get('last')
        dept = request.form.get('dept')

        if action == "get_email_by_name":
            msg = f"get_email_by_name|{first}|{last}"
        elif action == "get_email_by_dept":
            msg = f"get_email_by_dept|{dept}|{last}"
        elif action == "get_phone":
            msg = f"get_phone|{first}|{last}"
        elif action == "list_by_dept":
            msg = f"list_by_dept|{dept}"
        else:
            msg = ""

        if msg:
            result = send_request_to_server(msg)
        else:
            result = "Invalid request."

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
