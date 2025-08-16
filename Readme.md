Проект для генерации субтитров для видео.
## Запуск
Выставить переменные окружения в файле `compose.yml` и запустить:
```bash
docker compose up --build
```
## Переменные окружения
  - DEVICE=cpu - какое устройство использовать для работы модели (cpu|cuda:0). Если не указать, скрипт попробует использовать GPU, если он доступен. Иначе - CPU
  - MODEL_SIZE=medium.en  # Модель Whisper (можно изменить на small.en, large-v3 и т. д.). Список [тут](https://github.com/openai/whisper#user-content-available-models-and-languages)
  - AUDIO_TRACK_NUMBER=0 номер извлекаемой звуковой дорожки (zero-based)
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
## заметки на полях
```
# просто запустить контейнер с pytorch с поддержкой ROCm:
docker run -it \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  --ipc=host \
  --shm-size 8G \
  -v .:/mnt1 \
  rocm/pytorch:rocm6.4.1_ubuntu24.04_py3.12_pytorch_release_2.7.1 \
  bash

# Вытащить звук для экспериментов:
ffmpeg -i /mnt1/001\ Introduction.mp4 -ar 16000 -ac 1 -map 0:a:0 -c:a pcm_s16le -y -loglevel error /mnt1/001\ Introduction.wav

# найти самые большие файлы:
find / -type f -exec du -h {} + | sort -rh | less
```

## Результаты измерений
Конфигурация тестового стенда:
- GPU: Gigabyte Radeon RX 7800 XT OC 16Gb
- CPU: Amd Ryzen 5 7500F @ 3700/5200 MHz
- RAM: 2x16GB g.skill ripjaws ddr5 6400MHz
- OS: Linux mint 22.1 Xia

### medium.en
#### GPU
```
18:08:15 - >>> Creating model = medium.en, cache dir = /cache, device= cuda:0
18:08:27 - >>> Model creation took 11.99 seconds
18:08:30 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
18:09:15 - >>> transcribing complete, time: 45.54, audio length: 532.01, ratio: 0.09
18:09:16 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
18:09:32 - >>> transcribing complete, time: 16.40, audio length: 194.86, ratio: 0.08
18:09:33 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
18:10:34 - >>> transcribing complete, time: 61.03, audio length: 774.53, ratio: 0.08
```

#### CPU
```
18:13:01 - >>> Creating model = medium.en, cache dir = /cache, device= cpu
18:13:11 - >>> Model creation took 10.50 seconds
18:13:12 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
18:16:21 - >>> transcribing complete, time: 189.03, audio length: 532.01, ratio: 0.36
18:16:21 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
18:17:33 - >>> transcribing complete, time: 71.15, audio length: 194.86, ratio: 0.37
18:17:33 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
18:21:57 - >>> transcribing complete, time: 263.66, audio length: 774.53, ratio: 0.34
```

### large-v3
#### GPU
```
hisper-subtitles-1  | 19:25:45 - >>> Creating model = large-v3, cache dir = /cache, device= cuda:0
19:26:18 - >>> Model creation took 32.62 seconds
19:26:18 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
19:27:27 - >>> transcribing complete, time: 69.27, audio length: 532.01, ratio: 0.13
19:27:28 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
19:27:54 - >>> transcribing complete, time: 26.19, audio length: 194.86, ratio: 0.13
19:27:55 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
19:29:49 - >>> transcribing complete, time: 113.86, audio length: 774.53, ratio: 0.15
```
#### CPU
```
19:02:43 - >>> Creating model = large-v3, cache dir = /cache, device= cpu
19:02:52 - >>> Model creation took 9.91 seconds
19:02:53 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
19:09:13 - >>> transcribing complete, time: 379.89, audio length: 532.01, ratio: 0.71
19:09:13 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
19:11:43 - >>> transcribing complete, time: 150.03, audio length: 194.86, ratio: 0.77
19:11:44 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
19:23:29 - >>> transcribing complete, time: 704.57, audio length: 774.53, ratio: 0.91
```

### tiny.en
#### GPU
```
19:31:15 - >>> Creating model = tiny.en, cache dir = /cache, device= cuda:0
19:31:42 - >>> Model creation took 26.52 seconds
19:31:42 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
19:31:51 - >>> transcribing complete, time: 8.54, audio length: 532.01, ratio: 0.02
19:31:51 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
19:31:54 - >>> transcribing complete, time: 2.32, audio length: 194.86, ratio: 0.01
19:31:54 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
19:32:03 - >>> transcribing complete, time: 8.75, audio length: 774.53, ratio: 0.01
```
#### CPU
```
19:33:22 - >>> Creating model = tiny.en, cache dir = /cache, device= cpu
19:33:22 - >>> Model creation took 0.27 seconds
19:33:23 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
19:33:47 - >>> transcribing complete, time: 23.91, audio length: 532.01, ratio: 0.04
19:33:47 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
19:33:55 - >>> transcribing complete, time: 7.18, audio length: 194.86, ratio: 0.04
19:33:55 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
19:34:23 - >>> transcribing complete, time: 27.26, audio length: 774.53, ratio: 0.04
```
### small.en
#### GPU
```
19:42:11 - >>> Creating model = small.en, cache dir = /cache, device= cuda:0
19:42:20 - >>> Model creation took 8.89 seconds
19:42:21 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
19:42:41 - >>> transcribing complete, time: 20.76, audio length: 532.01, ratio: 0.04
19:42:42 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
19:42:49 - >>> transcribing complete, time: 7.20, audio length: 194.86, ratio: 0.04
19:42:50 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
19:43:16 - >>> transcribing complete, time: 26.40, audio length: 774.53, ratio: 0.03
```
#### CPU
```
19:35:46 - >>> Creating model = small.en, cache dir = /cache, device= cpu
19:37:41 - >>> Model creation took 115.34 seconds
19:37:42 - >>> Transcribing : /input/08 - Whats next/002 What's Next.mp4 -> /input/08 - Whats next/002 What's Next.srt
19:38:59 - >>> transcribing complete, time: 77.09, audio length: 532.01, ratio: 0.14
19:38:59 - >>> Transcribing : /input/08 - Whats next/001 Migration Guide For Existing Applications.mp4 -> /input/08 - Whats next/001 Migration Guide For Existing Applications.srt
19:39:28 - >>> transcribing complete, time: 29.16, audio length: 194.86, ratio: 0.15
19:39:29 - >>> Transcribing : /input/08 - Whats next/004 Is Reactive Programming Dead.mp4 -> /input/08 - Whats next/004 Is Reactive Programming Dead.srt
19:41:18 - >>> transcribing complete, time: 109.14, audio length: 774.53, ratio: 0.14
```