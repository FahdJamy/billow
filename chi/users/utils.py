import secrets
from PIL import Image
import os
from flask import current_app

def save_profile_pic(picture_name):
	token = secrets.token_hex(9)
	_, f_ext = os.path.splitext(picture_name.filename)
	pic_name = token + f_ext
	pic_path = os.path.join(current_app.root_path, 'static/ProfilePics', pic_name)

	new_size = (250,250)
	i = Image.open(picture_name)
	i.thumbnail(new_size)
	i.save(pic_path)

	return pic_name