Проект для генерации субтитров для видео.
## Запуск
Выставить переменные окружения в файле `compose.yml` и запустить:
```bash
docker compose up
```
## Переменные окружения
  - DEVICE=cpu - какое устройство использовать для работы модели. У меня Radeon, поэтому только `cpu`. Если есть карта NVidia, можно попробовать cuda:0
  - MODEL_SIZE=medium.en  # Модель Whisper (можно изменить на small.en, large-v3 и т. д.). Список [тут](https://github.com/openai/whisper#user-content-available-models-and-languages)
  - INPUT_DIR=/input Папка с видеофайлами. При запуске в докере менять не стоит, зато пригодится при отладочных запусках без контейнера
  - AUDIO_TRACK_NUMBER=0 номер извлекаемой звуковой дорожки (zero-based)
  - CACHE_DIR=/cache Путь к кешу внутри контейнера. При запуске в докере менять не стоит, зато пригодится при отладочных запусках без контейнера
  - SKIP_IF_EXISTS=True # не создавать субтитры, если файл субтитров уже существует

## Полезные команды для локальной отладки без докера

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install tinytag openai-whisper tf_keras


INPUT_DIR="/mnt/work/temp/for-subtitles" DEVICE=cpu CACHE_DIR=/home/tim/work/docker/subtitles/whisper/whisper-build/cache SKIP_IF_EXISTS=0 python3 process-video-openai.py

# получить список всех дорожек:
ffprobe /mnt/work/temp/for-subtitles2/6.Below.Miracle.On.the.Mountain.WEB-DL.1080p.m4v -show_entries stream=index,codec_type:stream_tags=title,language -of compact=p=0:nk=1


# вытащить вторую звуковую дорожку
ffmpeg -i 1.m4v -ar 16000 -ac 1 -map 0:a:1 -c:a pcm_s16le -y -loglevel error 1.wav
```
