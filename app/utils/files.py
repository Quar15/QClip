import magic
import subprocess


def is_allowed_mime_type(file, allowed_mime_types: list) -> bool:
    mime = magic.from_buffer(file.stream.read(2048), mime=True)
    file.stream.seek(0)  # Reset file pointer after reading
    return mime in allowed_mime_types


def generate_thumbnail(file_path: str, out_path: str):
    # get 1st frame, scale it down (or up) to 720px wide, save as jpg
    cmd = ["ffmpeg", "-v", "quiet", "-y", "-i", file_path, "-ss", "0", "-vframes", "1", "-vf", "scale=720:-1", out_path]

    subprocess.call(cmd)
