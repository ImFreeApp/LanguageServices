from flask import Flask, request, make_response
import nltk

app = Flask(__name__)

@app.route('/', methods=['POST'])
def parseText():
    # make_response(body, status_code, header)
    response = make_response('RESPONSE BODY: ' + request.data, 200)
    return response

if __name__ == '__main__':
    app.run(debug=True)
    # app.run();
