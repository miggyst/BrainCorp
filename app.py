from flask import Flask

app = Flask(__name__)

@app.route('/')

# <summary>Index function that returns Hello World!; Outputs the string onto the flask frontend site</summary>
# <returns>Hello World!</returns>
def index():
    return 'Hello World!'


'''
<summary>Main Function that runs the flask service application</summary>
'''
if __name__ == '__main__':
    app.run(debug=True)