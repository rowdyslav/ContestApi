from fastapi import UploadFile


accepted_file_types = ["image/png", "image/jpeg", "image/jpg", "image/heic", "image/heif", "image/heics", "png",
                       "jpeg", "jpg", "heic", "heif", "heics"]

def validator_picture(picture: UploadFile):
    if picture.content_type in accepted_file_types:
        return picture
    return None