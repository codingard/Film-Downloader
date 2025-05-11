# M3U8 Downloader

Video downloader that extracts `.m3u8` links from a web page using Chrome Developer Tools, downloads all `.ts` segments, and merges them into a single `.mp4` file using ffmpeg.

---

## 🔧 Requirements

- Python 3.8+
- FFmpeg installed and added to PATH
- Google Chrome browser installed

---

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/m3u8_downloader.git
cd m3u8_downloader
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **[macOS ONLY] Fix SSL certificate error**  
Run this once:
```bash
/Applications/Python\ 3.X/Install\ Certificates.command
```

---

## 📦 Usage

Run the script:

```bash
python -m m3u8_downloader
```

You will be asked to enter the video page URL. The script will:
1. Open Chrome in headless mode
2. Extract `.m3u8` links
3. Download all `.ts` segments asynchronously
4. Merge them into one `.mp4` file in the `output/` directory

---

## 📁 Output

- Temporary `.ts` segments are saved in `temp_segments/` and automatically deleted after merge
- The final merged `.mp4` file is saved in the `output/` folder

---

## ✅ Example

```bash
🔗 Enter the URL of the video page: https://example.com/video
🎯 Target stream: https://cdn.example.com/playlist.m3u8
💾 Output file will be saved as: output/video-title.mp4
```

---

## 🛠 Notes

- This project uses [undetected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) to bypass anti-bot systems
- Segment downloading is fully asynchronous via `aiohttp`
- `ffmpeg` must be installed and available in system PATH
- Ensure that the target streaming source is accessible from your current IP or region
