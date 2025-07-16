import sys
import os

# Thêm thư mục gốc vào sys.path để có thể import các module nội bộ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app.config import settings


import os
import subprocess
from datetime import datetime
from VietTTS.tts import TTS
from VietTTS.utils.file_utils import load_prompt_speech_from_file, load_voices
from app.utils import create_folder

tts_obj = TTS(model_dir=os.path.join(settings.DIR_ROOT, "VietTTS", "models"))

VOICE_DIR = os.path.join(settings.DIR_ROOT, "VietTTS", "samples")

VOICE_MAP = load_voices(VOICE_DIR)


def text_to_speech(text: str, voice: str = "0", speed: float = 1.0, output_format: str = "mp3") -> str:
    # Lấy tệp giọng nói từ VOICE_MAP
    if voice.isdigit():
        voice_file = list(VOICE_MAP.values())[int(voice)]
    else:
        voice_file = VOICE_MAP.get(voice)

    if not voice_file or not os.path.exists(voice_file):
        raise ValueError("Voice file not found")

    # Load giọng nói mẫu
    prompt_speech_16k = load_prompt_speech_from_file(filepath=voice_file, min_duration=3, max_duration=5)

    # TTS suy luận
    model_output = tts_obj.inference_tts(
        tts_text=text,
        prompt_speech_16k=prompt_speech_16k,
        speed=speed,
        stream=False,
    )

    # Gộp dữ liệu âm thanh
    raw_audio = b"".join(chunk["tts_speech"].numpy().tobytes() for chunk in model_output)

    # Tạo file tạm
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{timestamp}.{output_format}"

    folder_file = os.path.join(settings.DIR_ROOT, "utils", "download", "VietTTS")

    create_folder(folder_file)

    output_file = os.path.join(folder_file, output_file)

    # Chuyển định dạng qua ffmpeg
    ffmpeg_args = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "f32le",
        "-ar",
        "24000",
        "-ac",
        "1",
        "-i",
        "-",
        "-f",
        output_format,
        "-c:a",
        "libmp3lame" if output_format == "mp3" else "pcm_s16le",
        "-ab",
        "64k" if output_format == "mp3" else "",
        output_file,
    ]
    # Loại bỏ phần tử rỗng trong lệnh
    ffmpeg_args = [arg for arg in ffmpeg_args if arg != ""]

    proc = subprocess.run(ffmpeg_args, input=raw_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {proc.stderr.decode()}")

    return output_file


# Ví dụ sử dụng
if __name__ == "__main__":
    text = "Xin chào, đây là ví dụ chuyển văn bản thành giọng nói."
    audio_path = text_to_speech(text, voice="0", speed=1.0, output_format="mp3")
    print(f"Đã tạo file âm thanh: {audio_path}")
