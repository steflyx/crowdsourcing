from flask import Flask, render_template, request, json, jsonify
import pandas as pd
import random
MAX_ANSWER_PER_SENTENCE = 3
app = Flask(__name__, static_url_path='/static')

"""

Columns:
	sentence: text of the sentence
	speaker: sentence speaker
	answer_to_give: id of the next answer to give
	answer_0: first answer
	answer_1: second answer
	answer_3: third answer

"""
df_sentences = pd.read_csv('info/sentences.csv')

@app.route("/")
def main():
    return render_template('index.html')


def pick_new_sentence():
	rand_id = random.randint(0, len(df_sentences)-1)
	while df_sentences.at[rand_id, 'answer_to_give'] >= 3:
		rand_id = random.randint(0, len(df_sentences)-1)
	return {'sentence_id': rand_id, 'sentence_text': df_sentences.at[rand_id, 'sentence']}

"""

Receives: old_sentence_id, response
Updates results on df_sentences
Returns: sentence_text, sentence_id

"""
@app.route("/send_sentence")
def send_sentence():

	global df_sentences

	#Read values
	old_sentence_id = request.args.get('sentence_id', 0, type=int)
	response = request.args.get('response', 0, type=str)

	#User just entered
	if old_sentence_id != -1:
		answer_to_give = df_sentences.at[old_sentence_id, 'answer_to_give']
		df_sentences.at[old_sentence_id, 'answer_' + str(answer_to_give)] = response
		df_sentences.at[old_sentence_id, 'answer_to_give'] = answer_to_give + 1
		df_sentences.to_csv('info/sentences.csv', index=False)


	#Pick a sentence among the ones that have not been touched
	new_data = pick_new_sentence()
	return jsonify(new_data)

"""

Runs the application server side

"""
if __name__ == "__main__":
    app.run()