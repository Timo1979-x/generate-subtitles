FROM python:3.13.5-bookworm

RUN apt-get update && apt-get install -y \
  ffmpeg \
  less
  # && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-пакеты
RUN pip install --no-cache-dir \
  openai-whisper \
  tf_keras \
  tinytag
  # tqdm \
  # pydub

# Создаем рабочую директорию
WORKDIR /app
COPY . .

# Скрипт для обработки видео
COPY process-video-openai.py /app/process-video-openai.py
RUN chmod +x /app/process-video-openai.py
RUN mkdir /cache
# RUN echo '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
# RUN python3 /app/process_videos.py

# Указываем точку входа
ENTRYPOINT ["python3", "/app/process-video-openai.py"]
# ENTRYPOINT ["rocminfo"]
# ENTRYPOINT ["/bin/sh"]