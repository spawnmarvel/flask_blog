import os
UPLOAD_FOLDER = './uploads'

def check_file(fil):
    file_format = fil.filename
    valid = False
    if file_format.endswith("png") or file_format.endswith("jpg"):
        valid = True
    return valid

def list_images():
    for fi in os.listdir(UPLOAD_FOLDER):
        print(format(fi))


