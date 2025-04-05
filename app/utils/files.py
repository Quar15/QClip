import magic
import subprocess


def is_allowed_mime_type(file, allowed_mime_types) -> bool:
    mime = magic.from_buffer(file.stream.read(2048), mime=True)
    file.stream.seek(0)  # Reset file pointer after reading
    return mime in allowed_mime_types


def generate_thumbnail(file, out_path):
    cmd = ["ffmpeg", "-v", "quiet", "-y", "-i", str(file), "-ss", "0", "-vframes", "1", str(out_path)]

    subprocess.call(cmd)
