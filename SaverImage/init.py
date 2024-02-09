import json
from pathlib import Path

import requests
from flask import Response

class ImagesSaver:
    def __init__(self, name, ip):
        self.ip = ip
        self.path = Path(__file__).parent / "images.json"
        self.type = name
        try:
            with open(self.path, 'r') as f:
                data = json.loads(f.read())
                print("✅ VRCatRoutes/ImagesSaver")

        except Exception as e:
            if ("No such file or directory" in str(e)):
                with open(self.path, 'x') as f:
                    f.write('{}')
                    return
            print(e)

    def saveImages(self, images):
        try:
            if (len(images) > 0):
                with open(self.path, 'r') as f:
                    data = json.loads(f.read())
                    print(data)
                    result = {self.ip: {self.type: images}}
                    data.update(result)
                with open(self.path, 'w') as f:
                    json.dump(data, f, indent=4)

            return True

        except Exception as e:
            print(e)
            return False

    def getImage(self, index):
        try:
            with open(self.path, 'r') as f:
                data = json.loads(f.read())
                print(data[self.ip][self.type][int(index)], index, self.ip)
                if (self.ip in data and self.type in data[self.ip] and len(data[self.ip][self.type]) > int(index)):
                    return data[self.ip][self.type][int(index)]

        except Exception as e:
            print(e)
            return None

    def getBitmap(self, index):
        url = self.getImage(index)
        if (url != None):
            response = requests.get(url)

            if (response.status_code == 200):
                content_type = response.headers['Content-Type']

                return Response(response.content, content_type=content_type)
            else:
                return None
        else:
            return None