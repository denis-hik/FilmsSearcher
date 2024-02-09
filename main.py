import json

from flask_cors import CORS, cross_origin
from flask import Flask, render_template, make_response, request

from SaverImage.init import ImagesSaver
from UnWrap.init import UnWap

try:
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/serials', methods=['GET'])
    @cross_origin()
    def Serials():
        temp = UnWap(request.remote_addr).getSearials()
        if (temp != None):
            return '{"list": ' + json.dumps(temp) + ' }'
        else:
            return '{"list": [] }'
    def SerialsSearch():
        search = str(request.query_string).split("'")[1]
        temp = UnWap(request.remote_addr).getSearials(search)
        if (temp != None):
            return '{"list": ' + json.dumps(temp) + ' }'
        else:
            return '{"list": [] }'

    @app.route('/films', methods=['GET'])
    @cross_origin()
    def Films():
        temp = UnWap(request.remote_addr).getFilms()
        if (temp != None):
            return '{"list": ' + json.dumps(temp) + ' }'
        else:
            return '{"list": [] }'

    @app.route('/films/search', methods=['GET'])
    @cross_origin()
    def FilmsSearch():
        search = str(request.query_string).split("'")[1]
        temp = UnWap(request.remote_addr).getFilms(search)
        if (temp != None):
            return '{"list": ' + json.dumps(temp) + ' }'
        else:
            return '{"list": [] }'

    @app.route('/image/<id>', methods=['GET'])
    @cross_origin()
    def FilmsImage(id):
        try:
            return ImagesSaver("UnWrap", request.remote_addr).getBitmap(int(id))
        except Exception as e:
            print(e)
            return "Error"

except Exception as e:
    print(e)

if (True):
    if __name__ == "__main__":
        app.env = "development"
        app.run()