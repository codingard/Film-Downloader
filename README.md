# Film Downloader

Console-based video downloader that extracts `.m3u8` links from a video page (e.g., Rezka) using Chrome Developer Tools, downloads all `.ts` segments asynchronously, and merges them into a single `.mp4` file using a built-in `ffmpeg`.

---

## 🔧 Requirements

- Python 3.8+
- Google Chrome browser installed  
- You do **not** need to install `ffmpeg` — it's included in the project

---

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/film_downloader.git
cd film_downloader
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **(macOS ONLY) Fix SSL certificate error**  
Run this once:
```bash
/Applications/Python\ 3.X/Install\ Certificates.command
```

---

## 📦 Usage

Start the script:

```bash
python -m film_downloader
```

You will be prompted to paste a video page URL (from Rezka or similar). The script will:

1. Launch Chrome in headless mode
2. Scan network logs and extract `.m3u8` links
3. Download all video segments asynchronously
4. Merge them into one `.mp4` using the embedded `ffmpeg`
5. Save the final video into the `output/` folder

---

## 📁 Output

- Temporary `.ts` files are stored in `temp_segments/` (and deleted automatically)
- Final video is saved to: `output/your-video.mp4`

---

## ✅ Example

```bash
🔗 Enter the URL of the video page: https://rezka.ag/films/drama/806-pobeg-iz-shoushenka-1994.html
🎯 Target stream: https://cdn.example.com/playlist.m3u8
💾 Output file will be saved as: output/pobeg-iz-shoushenka.mp4
```

---

## 📂 FFmpeg

The script uses a bundled version of `ffmpeg` located in the `ffmpeg/` folder:
```
ffmpeg/
├── ffmpeg.exe     ← for Windows
└── ffmpeg         ← for macOS/Linux (must be executable)
```

If missing:
- [Download `ffmpeg.exe` for Windows](https://www.gyan.dev/ffmpeg/builds/)
- [Download `ffmpeg` for macOS](https://evermeet.cx/ffmpeg/)
- Or copy from your system and place it here manually

---

## 🛠 Notes

- Built with [undetected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) to bypass bot protection
- Segment downloading uses `aiohttp` for async performance
- `.m3u8` links expire quickly, so run the script right after copying the page URL
- Make sure the stream is accessible from your IP region
  
