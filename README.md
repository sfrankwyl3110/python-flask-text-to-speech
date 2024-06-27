# python-flask-text-to-speech

### Installation & Start

##### Assuming you have cloned the following Repo and updated the default_tts_url in wyl/tts.py:
```git clone https://github.com/matatonic/openedai-speech```
```cd openedai-speech```
```cp sample.env speech.env```
```docker compose -f docker-compose.min.yml up -d ```

##### Now clone and run the Flask-App:
```git clone https://github.com/sfrankwyl3110/python-flask-text-to-speech.git```
```cd python-flask-text-to-speech```
```pip install -r requirements.txt```
```python create_speech_from_text.py```
