import magic
import subprocess


def is_allowed_mime_type(file, allowed_mime_types: list) -> bool:
    mime = magic.from_buffer(file.stream.read(2048), mime=True)
    file.stream.seek(0)  # Reset file pointer after reading
    return mime in allowed_mime_types


def generate_thumbnail(file_path: str, out_path: str):
    cmd = ["ffmpeg", "-v", "quiet", "-y", "-i", file_path, "-ss", "0", "-vframes", "1", out_path]

    subprocess.call(cmd)
