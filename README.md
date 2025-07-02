# video-dubber

**Automated video dubbing with Whisper, DeepL & ElevenLabs**
**Автоматизированный дубляж видео с Whisper, DeepL и ElevenLabs**
**多语言视频配音：Whisper 转录 + DeepL 翻译 + ElevenLabs 合成**

---

## 📖 Description / Описание / 项目简介

**video-dubber** is a Python toolchain that automatically extracts audio from a video, transcribes it with Whisper, translates it via DeepL, synthesizes dubbed speech with ElevenLabs, and muxes the new audio back into the original video.
**video-dubber** — это Python-скрипт, который автоматически извлекает звук из видео, транскрибирует его с помощью Whisper, переводит через DeepL, синтезирует дубляж на ElevenLabs и интегрирует новый звук обратно в видео.
**video-dubber** 是一个 Python 工具链，能够自动从视频中提取音频，用 Whisper 转录，使用 DeepL 翻译，再调用 ElevenLabs 合成配音，最后将新的音轨合并回原始视频。

---

## 🚀 Features / Возможности / 功能

* **Whisper transcription** for accurate speech-to-text
  **Транскрипция Whisper** для точного преобразования речи в текст
  **Whisper 转录**，实现精准的语音转文字
* **DeepL translation** for high-quality translations
  **Перевод DeepL** для качественного перевода текста
  **DeepL 翻译**，提供高质量翻译
* **ElevenLabs TTS** for natural-sounding dubbed audio
  **Генерация голоса ElevenLabs** для естественного звучания
  **ElevenLabs 语音合成**，生成自然配音
* **Parallel processing** with `ThreadPoolExecutor` & `tqdm` progress bars
  **Параллельная обработка** с `ThreadPoolExecutor` и индикаторами прогресса `tqdm`
  **并行处理**，结合 `ThreadPoolExecutor` 与 `tqdm` 进度展示
* **Precise audio mixing** via Pydub
  **Точное смешивание аудио** через Pydub
  **Pydub 精确混音**
* **Volume boost** configurable via FFmpeg
  **Настраиваемое усиление громкости** через FFmpeg
  **通过 FFmpeg 可配置音量增强**
* **Clean-up temporary files**
  **Автоматическая очистка временных файлов**
  **临时文件自动清理**

---

## ⚙️ Prerequisites / Требования / 环境要求

* Python 3.8+
  **Python 3.8+**
  **Python 3.8 及以上**
* FFmpeg installed and available in PATH
  **FFmpeg, доступен в PATH**
  **已安装并配置到 PATH 的 FFmpeg**
* DeepL API key
  **Ключ API DeepL**
  **DeepL API 密钥**
* ElevenLabs API key & voice ID
  **Ключ API ElevenLabs и ID голоса**
  **ElevenLabs API 密钥及声线 ID**
* Required Python packages:

  ```bash
  pip install \
    whisper \
    requests \
    pydub \
    imageio-ffmpeg \
    tqdm
  ```

---

## 🔧 Installation / Установка / 安装

1. **Clone the repo** / **Клонировать репозиторий** / **克隆仓库**

   ```bash
   git clone https://github.com/your-username/video-dubber.git
   cd video-dubber
   ```
2. **Create and activate a virtual environment** / **Создать и активировать виртуальное окружение** / **创建并激活虚拟环境**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Ensure FFmpeg is installed** / **Проверить установку FFmpeg** / **确保已安装 FFmpeg**

   * macOS: `brew install ffmpeg`
     **macOS:** `brew install ffmpeg`
     **macOS:** `brew install ffmpeg`
   * Ubuntu/Debian: `sudo apt install ffmpeg`
     **Ubuntu/Debian:** `sudo apt install ffmpeg`
     **Ubuntu/Debian:** `sudo apt install ffmpeg`

---

## 🔑 Configuration / Конфигурация / 配置

Create a `.env` file in project root (or export env vars):
Создайте файл `.env` в корне проекта (или экспортируйте переменные):
在项目根目录创建 `.env` 文件（或导出环境变量）：

```bash
DEEPL_API_KEY="your_deepl_key"
ELEVENLABS_API_KEY="your_elevenlabs_key"
ELEVENLABS_VOICE="21m00Tcm4TlvDq8ikWAM"
```

---

## 🎬 Usage / Использование / 使用方法

```bash
python dub_script.py \
  --video   path/to/input.mp4 \
  --output  path/to/output_dubbed.mp4 \
  --model   small \
  --workers 4 \
  --volume  7.0
```

* `--video` – input video file
  **`--video`** – входной видеофайл
  **`--video`** – 输入视频文件
* `--output` – output video file name
  **`--output`** – имя выходного файла
  **`--output`** – 输出文件名
* `--model` – Whisper model (`tiny`, `base`, `small`, `medium`, `large`)
  **`--model`** – модель Whisper (`tiny`, `base`, `small`, `medium`, `large`)
  **`--model`** – Whisper 模型
* `--workers` – number of parallel TTS threads
  **`--workers`** – число потоков для TTS
  **`--workers`** – 并发 TTS 线程数
* `--volume` – amplification factor
  **`--volume`** – коэффициент усиления
  **`--volume`** – 音量增强倍数

---

## 🛠️ Advanced Options / Дополнительно / 高级选项

* **LUFS normalization**: integrate `ffmpeg-normalize` for consistent loudness.
  **Нормализация LUFS**: интеграция `ffmpeg-normalize` для уровня громкости.
  **LUFS 归一化**：集成 `ffmpeg-normalize` 实现一致响度
* **Subtitle export**: generate `.srt` from Whisper segments.
  **Экспорт субтитров**: генерация `.srt` из сегментов Whisper.
  **导出字幕**：从 Whisper 段生成 `.srt`
* **Dockerfile**: containerize for reproducible envs.
  **Dockerfile**: контейнеризация для повторяемости.
  **Dockerfile**：容器化以复现环境
* **Cloud deployment**: adapt for AWS Lambda / GCP Cloud Functions.
  **Развертывание в облаке**: адаптация под AWS Lambda / GCP Cloud Functions.
  **云部署**：适配 AWS Lambda/GCP 云函数

---

## 📝 License / Лицензия / 许可证

MIT © 2025 Your Name
Released under the MIT License.
По стандарту MIT.
根据 MIT 协议。
