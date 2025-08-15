#!/usr/bin/python3

import whisper, time, sys, os, subprocess
from tinytag import TinyTag

def to_bool(value):
  return value.lower() in ["true", "1", "t", "y", "yes"]
# Конфигурация из переменных окружения
INPUT_DIR = os.path.abspath(os.getenv("INPUT_DIR", "/input"))
# Доступные модели: 
# 'tiny.en', 'tiny', 'base.en', 'base', 'small.en','small', 
# 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo'
MODEL_SIZE = os.getenv("MODEL_SIZE", "medium.en")
DEVICE = os.getenv("DEVICE", "cpu")
CACHE_DIR = os.getenv("CACHE_DIR", "/cache")
AUDIO_TRACK_NUMBER = int(os.getenv("AUDIO_TRACK_NUMBER", "0"))
SKIP_IF_EXISTS = to_bool(os.getenv("SKIP_IF_EXISTS", "1"))

model = None

# audio_file = "/home/tim/work/docker/subtitles/python-env/audio.wav"
# audio = TinyTag.get(audio_file)

# print(">>> transcribing...")
# start_time = time.time()
# transcription = model.transcribe(audio_file)
# print(f"Transcription took {time.time() - start_time:.2f} seconds")

# print(f"audio file length is {str(audio.duration)} seconds")

# print(list(transcription.keys()))
# print(transcription["text"])
# print(transcription["segments"])

# with open(audio_file + ".pickle", 'wb') as f:
#   pickle.dump(transcription, f, pickle.HIGHEST_PROTOCOL)

def create_model():
  global model
  print(">>> Creating model... ", end = "", flush = True)
  start_time = time.time()
  model = whisper.load_model(
    MODEL_SIZE,
    device=DEVICE,
    download_root = CACHE_DIR
  )
  print(f"took {time.time() - start_time:.2f} seconds")

def extract_audio(video_path, audio_path):
    """Извлекает аудио из видео в формате WAV (16kHz, моно)"""
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        "-map", "0:a:" + str(AUDIO_TRACK_NUMBER),
        "-c:a", "pcm_s16le",
        "-y", 
        "-loglevel", "error",
        audio_path,
    ]
    subprocess.run(command, check=True)

def seconds_to_time(seconds):
  """Переводит время в секундах и миллисекундах (например 5678.012) в формат HH:MM:SS,MMM (например 01:34:38,012)"""
  ms=int(seconds*1000 % 1000)
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{ms:03d}"

def transcribe_audio(audio_path, srt_path, video_path):
  """Создает субтитры в формате SRT"""
  audio_length = TinyTag.get(audio_path).duration
  print(f">>> Transcribing : {video_path} -> {srt_path} ", end = "", flush = True)
  start_time = time.time()
  transcription = model.transcribe(audio_path, fp16 = not DEVICE == "cpu")
  time_taken = time.time() - start_time
  print(f"time: {time_taken:.2f}, audio length: {audio_length:.2f}, ratio: {time_taken / audio_length:.2f}")
  segments = transcription["segments"]
  with open(srt_path, "w") as f:
    for i, segment in enumerate(segments, start=1):
      f.write(f"{i}\n")
      f.write(f"{seconds_to_time(segment["start"])} --> {seconds_to_time(segment["end"])}\n")
      f.write(f"{segment["text"].strip()}\n\n")

    # segments, _ = model.transcribe(audio_path, beam_size=5)
    # with open(srt_path, "w") as f:
    #     for i, segment in enumerate(segments, start=1):
    #         f.write(f"{i}\n")
    #         f.write(f"{segment.start:.2f} --> {segment.end:.2f}\n")
    #         f.write(f"{segment.text}\n\n")

def process_videos(file_list):
    """Обрабатывает все видеофайлы в file_list"""
    for (dir_name, video_name, srt_name) in file_list:
      video_path = os.path.join(dir_name, video_name)
      audio_path = "/tmp/bda16166-f9cc-48b2-b2df-62ac22f4ad86.wav"
      srt_path = os.path.join(dir_name, srt_name)

      extract_audio(video_path, audio_path)
      
      transcribe_audio(audio_path, srt_path, video_path)

      # Удаляем временный аудиофайл
      os.remove(audio_path)

def list_files(dir):
  """сканирует директорию в поиске видеофайлов и субтитров
    Если видеофайл не имеет парного файла субтитров, то он добавляется в список.
    Если видеофайл имеет парный файл субтитров, но задана опция пересоздания (not SKIP_IF_EXISTS), то он также добавляется в список.
    возвращает список кортежей вида ("директория", "видеофайл.mkv", "файл субтитров.srt")
  """
  result = []
  video_exts = (".mp4", ".mkv", ".avi", ".mov", ".m4v")
  for dir_files in os.walk(dir):
    for filename in dir_files[-1]:
      if not filename.lower().endswith(video_exts):
        continue
      
      video_basename = os.path.splitext(filename)[0]
      for f in dir_files[-1]:
        (file_basename, file_ext) = os.path.splitext(f)
        if file_basename == video_basename and file_ext.lower() == ".srt":
          if not SKIP_IF_EXISTS:
            result.append((dir_files[0], filename, f))
          break
      else:
        result.append((dir_files[0], filename, video_basename + ".srt"))
  return result

if __name__ == "__main__":
    files = list_files(INPUT_DIR)
    if len(files) == 0:
      print(">>> Nothing to do")
      exit(0)
    create_model()
    process_videos(files)