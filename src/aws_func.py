from src import aws_client
from io import BytesIO
import base64
from src import aws_client

def upload_img(file, object_name):
    bytesio = BytesIO(file.read())
    ext = file.filename[-4:]
    aws_client.upload_fileobj(bytesio, "gamestorebucket", object_name+ext, ExtraArgs=None)

def upload_user_img(file, object_name):
    bytesio = BytesIO(file.read())
    ext = file.filename[-4:]
    aws_client.upload_fileobj(bytesio, "gamestoreuserbucket", object_name+ext, ExtraArgs=None)

def get_aws_image(bucket, obj):
    a_file = BytesIO()
    aws_client.download_fileobj(bucket, obj+".jpg", a_file)
    a_file.seek(0)
    str_equivalent_image = base64.b64encode(a_file.getvalue()).decode()
    return ("data:image/png;base64," + str_equivalent_image)