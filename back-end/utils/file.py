import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp4", "mov", "avi"}
ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/gif",
    "video/mp4", "video/quicktime", "video/x-msvideo"
}

def allowed_file(filename, content_type):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS and
        content_type in ALLOWED_MIME_TYPES
    )

def save_file(file, upload_folder="uploads"):
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(str(uuid.uuid4()) + '.' + ext)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filepath, file.mimetype
