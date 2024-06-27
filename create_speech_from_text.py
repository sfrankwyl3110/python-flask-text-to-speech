# loading env
import os
import base64
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import json

load_dotenv('.env')

import asyncio
from wyl.tts import WYLTTS

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

wyl_tts = WYLTTS()

#coro = wyl_tts.create_speech(text_input="We are there!", play=False)

if not os.path.isdir(os.path.join(os.path.dirname(__file__), "templates")):
    os.makedirs(os.path.join(os.path.dirname(__file__), "templates"), exist_ok=True)
if not os.path.isdir(os.path.join(os.path.dirname(__file__), "static")):
    os.makedirs(os.path.join(os.path.dirname(__file__), "static"), exist_ok=True)


def create_app():
    app_ = Flask(__name__, template_folder="templates", static_folder="static")
    return app_


app = create_app()


@app.route('/')
def result():
    return render_template("index.html")


responses_base_filepath = os.path.join(os.path.dirname(__file__), "responses")


@app.get('/get_responses_list')
def get_responses_list():
    dir_list = os.listdir(responses_base_filepath)
    files_ = []
    for file_ in dir_list:
        if file_.endswith('.base64'):
            with open(os.path.join(responses_base_filepath, file_)) as current_f:
                content = current_f.read()
                file_json = json.loads(base64.b64decode(content).decode("utf-8"))
                file_json["filename"] = file_
                files_.append(file_json)
    return jsonify(files_)


@app.post('/load_mp3')
def load_mp3():
    mp3_filename = request.form.get('mp3_file')
    mp3_filepath = os.path.join(responses_base_filepath, mp3_filename)
    exist_ok = os.path.isfile(mp3_filepath)
    resp_base_ret = {
        "file": mp3_filename, "exist": exist_ok
    }
    if exist_ok:
        base64_mp3 = base64.b64encode(open(mp3_filepath, 'rb').read()).decode('utf-8')
        resp_base_ret["base64"] = base64_mp3
        return jsonify(resp_base_ret)
    else:
        return jsonify(resp_base_ret)


@app.post("/generate")
async def generate_index():
    phrase_ = request.form.get('phrase')

    mp3_filepath = await wyl_tts.create_speech(text_input=phrase_, play=False)

    with open(mp3_filepath[0], 'rb') as mp3_file:
        content = base64.b64encode(mp3_file.read()).decode('utf-8')
    return jsonify({"audio": content})



if __name__ == '__main__':
    # loop.run_until_complete(coro)

    app.run(host="0.0.0.0", port=5000, debug=True)
