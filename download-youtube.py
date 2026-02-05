import yt_dlp
import os
import sys

current_video_title = ""

def progress_hook(d):
    global current_video_title
    # info_dict 是最可靠的來源，當 yt-dlp 進入下載流程時會填入
    if 'info_dict' in d:
        current_video_title = d['info_dict'].get('title', current_video_title)

    # 處理下載進度列印
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r   [下載中] {percent} | 速度: {speed} | 剩餘時間: {eta}", end="")

class MyLogger:
    """ 自定義記錄器，用來捕捉並美化錯誤訊息 """
    def debug(self, msg):
        # print(msg)
        pass
    def warning(self, msg):
        # print(msg)
        pass
    def error(self, msg):
        global current_video_title
        if "Requested format" in msg or "DRM" in msg or "not available" in msg:
            print(f"❌ 無法下載: 【{current_video_title}】")
            print(f"   原因: 該影片受版權保護 (DRM) 或格式受限。")
        else:
            print(f"❌ 錯誤: 【{current_video_title}】 -> {msg}")

def get_resource_path():
    """ 取得內部資源路徑 (FFmpeg 所在之處) """
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_export_path():
    """ 取得外部輸出路徑 (音樂存放之處) """
    if getattr(sys, 'frozen', False):
        # 如果是 EXE，存放在 EXE 旁邊
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def download_best_audio(url):
    global current_video_title
    ffmpeg_dir = get_resource_path()
    export_dir = get_export_path()
    
    # 音樂實際存放的路徑
    download_folder = os.path.join(export_dir, 'downloads')
    output_path = os.path.join(download_folder, '%(title)s.%(ext)s')

    ydl_opts = {
        # 1. 核心邏輯：從高品質開始嘗試，不行的話就降級
        'format': 'bestaudio/best',
        # 'format': (
        #     'bestaudio[abr<=320]/bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best'
        # ),
        'ffmpeg_location': ffmpeg_dir,

        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
        'ignoreerrors': True, # 遇到錯誤，繼續執行
        'quiet': True, # True=隱藏 yt-dlp 的所有標準輸出訊息（如進度條、伺服器回應、版本資訊）。

        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],
                'oauth': True,
            }
        },

        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }, 
        {
            'key': 'FFmpegMetadata',
        }],
        'postprocessor_args': {
            'ExtractAudio': ['-af', 'loudnorm'],    # 使用國際電信聯盟（ITU）的標準化算法
        },
        'playlist_items': '1-200',
        'outtmpl': output_path,
        'writethumbnail': False,
    }

    try:
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"正在準備下載: {url}")
            try:
                info_result = ydl.extract_info(url, download=False)
            except Exception as e:
                print(f"❌ 無法讀取影片資訊: {e}")
                return

            if info_result is None:
                print("❌ 搜尋結果為空，可能是受限影片或網址錯誤。")
                return

            if 'entries' in info_result:
                # 情況 A: 這是一個播放清單
                entries = list(info_result['entries'])
                total = len(entries)
                print(f"找到播放清單，共 {total} 個項目。")

                for i, entry in enumerate(entries, 1):
                    if not entry: continue
                    current_video_title = entry.get('title', '未知影片')
                    print(f"\n[進度] 正在處理第 {i}/{total} 首: {current_video_title}")
                    
                    ydl.download([entry['webpage_url']])
            else:
                # 情況 B: 這是單一影片
                ydl.download([url])
            
            print(f"\n✅ 下載完成！檔案已存放在: {download_folder}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    print("=" * 52)
    print("            YouTube 高音質音樂下載器")
    print("提示：若是第一次使用，畫面可能會出現驗證網址與代碼，")
    print("請依照指示開啟瀏覽器輸入代碼以取得高品質下載授權。")

    while True:
        print("=" * 52)
        print("提示：輸入 'exit' 或 'q' 可結束程式")
        print("-" * 52)
        video_url = input("\n請輸入 YouTube 影片或清單網址:").strip()
        
        if video_url.lower() in ['exit', 'q', 'quit', '退出', '離開']:
            print("\n程式即將關閉，再見！")
            break
            
        if video_url:
            download_best_audio(video_url)
            print("-" * 52)
            print("任務結束。您可以繼續輸入下一個網址。")
        else:
            print("⚠️  網址不能為空，請重新輸入。")

