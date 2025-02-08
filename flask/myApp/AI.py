# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/hello', methods=['POST'])
# def hello():
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     return 'Hello %s %s have fun learning python <br/> <a href="/">Back Home</a>' % (first_name, last_name)

# if __name__ == '__main__':
#     app.run(host = '0.0.0.0', port = 3001)


from flask import Flask, render_template

app = Flask(__name__)
# app = Flask(__name__, template_folder='templates')
app = Flask(__name__, template_folder='/home/rhinks/Desktop/hackathon babbyyyy/flask/myApp/templates')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
