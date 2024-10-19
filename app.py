import os
import subprocess
import platform
from datetime import datetime
import pytz
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

def get_username():
    try:
        return os.getlogin()
    except OSError:
        try:
            import pwd
            return pwd.getpwuid(os.getuid())[0]
        except:
            return "Unknown"

def get_top_output():
    try:
        if platform.system() == "Windows":
            return "Top command not available on Windows"
        else:
            return subprocess.check_output(['top', '-b', '-n', '1']).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error running 'top' command: {str(e)}"
    except OSError as e:
        return f"OS Error when running 'top' command: {str(e)}"

@app.route('/')
def root():
    return redirect(url_for('htop'))

@app.route('/htop')
def htop():
    # Get full name (replace with your actual name)
    name = "Your Full Name"

    # Get system username
    username = get_username()

    # Get server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')

    # Get top output
    top_output = get_top_output()

    # Get system information
    system_info = f"OS: {platform.system()} {platform.release()}"

    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTOP Information</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
            }
            h1, h2 {
                color: #333;
            }
            pre {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <h1>HTOP Information</h1>
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Username:</strong> {{ username }}</p>
        <p><strong>Server Time (IST):</strong> {{ server_time }}</p>
        <p><strong>System Info:</strong> {{ system_info }}</p>
        <h2>Top Output:</h2>
        <pre>{{ top_output }}</pre>
    </body>
    </html>
    """

    return render_template_string(html_template, name=name, username=username, server_time=server_time, top_output=top_output, system_info=system_info)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)