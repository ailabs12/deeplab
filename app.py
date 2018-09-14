from flask import Flask, request, json
import deeplab

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return 'Hello World POST'
    else:
        # IMAGE_URL = 'https://static.mk.ru/upload/entities/2018/07/27/articles/detailPicture/29/bc/22/88/836556deb3f8e01b2d80a627916145f1.jpg'
        if request.args.get('image'):
          found_objects = deeplab.run_visualization(request.args.get('image'))
          return json.jsonify(found_objects)
        else:  
          return 'Not found arg image'

if __name__ == "__main__":
    app.run(port=8080)