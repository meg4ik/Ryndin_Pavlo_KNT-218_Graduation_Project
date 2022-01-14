from src import aws_client
from io import BytesIO

def upload_img(file, object_name):
    bytesio = BytesIO(file.read())
    ext = file.filename[-4:]
    aws_client.upload_fileobj(bytesio, "gamestorebucket", object_name+ext, ExtraArgs=None)