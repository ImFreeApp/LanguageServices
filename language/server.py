from flask import Flask, request, make_response
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def parseText():
    stop_words = set(stopwords.words('english'))
    lem = WordNetLemmatizer()
    parsedTokens = None

    def getKeywords(text):
        words = word_tokenize(text)
        # filter out punctuation
        tokens = [word.lower() for word in words if word.isalnum()]
        # filter out filler/stop words and lemmatize each word
        return [lem.lemmatize(key) for key in tokens if not key in stop_words]

    def getLemmas(words):
        lemmaCount = {}
        for word in words:
            lemmas = reduce(lambda lemmas, syn: lemmas + [lem.name() for lem in syn.lemmas()], wordnet.synsets(word), [])
            for lemma in lemmas:
                if lemma in lemmaCount:
                    lemmaCount[lemma] += 1;
                else:
                    lemmaCount[lemma] = 1

        return lemmaCount

    try:
        parsedTokens = getLemmas(getKeywords(request.data))
    except:
        return make_response('ERROR parsing text', 500)
    else:
        return make_response(json.dumps(parsedTokens), 200)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run();
