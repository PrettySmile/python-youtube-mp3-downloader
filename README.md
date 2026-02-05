# YouTube MP3 Downloader (Python)

這是一個練習用專案。

一個使用 **Python** 撰寫的工具，可將 YouTube 影片下載並轉換成 **MP3 音訊檔案**。  
支援在本機執行，並可透過 **PyInstaller** 打包成 Windows 可執行檔（`.exe`），方便一般使用者使用。

---

## 📌 專案功能

- 使用 `yt-dlp` 下載 YouTube 影片
- 透過 `ffmpeg` 轉換為 MP3 音訊格式
- 可打包成單一 `.exe` 檔（不需安裝 Python）

---

## 🧰 使用技術

- Python 3
- yt-dlp
- ffmpeg / ffprobe
- PyInstaller

---

## 🖥️ 環境需求

- Windows 作業系統
- Python 已安裝（僅開發與打包時需要）

---

## 🚀 使用方式

### STEP 01:
```bash
    py --version
```

### STEP 02
```bash
    winget install ffmpeg
```

### STEP 03:
```bash
    pip install -U yt-dlp
```

### STEP 04:
```bash
    pip install pyinstaller
    # 打包成exe檔
    pyinstaller --clean --onefile --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." --icon="icon.ico" --name "MP3音樂下載" download-youtube.py
```