from flask import Flask, request, jsonify
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout

from functions import clean_text, get_tags, format_inputs

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# session = tf.Session(config=config,...)

application = Flask(__name__)

# loading tokenizer, model, and weights
#---------------------------------------------

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

json_file = open('combined_model2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("combined_weights2.h5")
print("Loaded model from disk")
#---------------------------------------------


@application.route('/')
def home():
    return 'You made it'

@application.route('/api/tags', methods=['POST'])
def api():
    data = request.get_json()
    uid = data['id']
    sender = data['sender']
    sender = format_inputs(sender, 100)
    subject = data['subject']
    subject = format_inputs(subject, 150)
    message = data['message']
    message = format_inputs(message, 5000)
    text = [message, subject, sender]
    tag = get_tags(text, loaded_model)
    print(tag[0])
    tag = tag[0]
    tagged_email = {'message-id': uid, 'from': sender, 'subject': subject,
                    'message': message, 'tag': tag}
    
    # print('This is error output', file=sys.stderr)
    # print('This is standard output', file=sys.stdout)

    return jsonify(tagged_email)


if __name__ == "__main__":
    application.run(debug=True)