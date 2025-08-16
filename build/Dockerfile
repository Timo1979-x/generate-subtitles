FROM rocm/pytorch:rocm6.4.1_ubuntu24.04_py3.12_pytorch_release_2.7.1

RUN apt-get update
RUN apt-get install -y \
  ffmpeg \
  less

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
RUN chmod +x /app/*.py
RUN mkdir /cache

# Указываем точку входа
# ENTRYPOINT ["python3", "/app/test.py"]
ENTRYPOINT ["python3", "/app/process-video-openai.py"]
# ENTRYPOINT ["rocminfo"]
# ENTRYPOINT ["/usr/bin/bash"]
