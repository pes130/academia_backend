from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from werkzeug.datastructures import FileStorage 
import time
import os


class UploadImage(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=FileStorage, location='files')
        nombre = str(time.time())
        args = parser.parse_args()

        imagen = args['image']
        print(imagen)
        extension = ''
        if imagen.mimetype == "image/png":
            extension = ".png"
        elif imagen.mimetype == "image/jpg" or imagen.mimetype == "image/jpeg":
            extension = ".jpg"

        nombre = nombre+extension
        imagen.save('/var/www/html/uploads/'+nombre)

        return {'filename': nombre}
      
    
