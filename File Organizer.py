# ==========================================
# Project: CYBER TECHNOLOGY System Toolkit (4K Pro Edition)
# Developer: Lynx1 / CYBER TECHNOLOGY
# Version: 2.2 (2026)
# Description: Scaled 4K UI with immersive dark window framing integration.
# ==========================================

import os
import sys
import shutil
import ctypes
import platform
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests

# --- 4K High-DPI Resolution Scaling Tweak ---
def enable_4k_awareness():
    try:
        # Forces Windows to render fonts and layouts natively crisp on modern high-DPI displays
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

enable_4k_awareness()

# --- Global Configurations ---
DOWNLOADS = {
    "windhawk": {
        "url": "https://ramensoftware.com/downloads/windhawk_setup.exe",
        "filename": "windhawk_setup.exe",
        "display_name": "Windhawk Modding Engine (x64)"
    },
    "lively": {
        "url": "https://github.com/rocksdanister/lively/releases/download/v2.2.1.0/lively_setup_x86_full_v2210.exe",
        "filename": "lively_setup_x86_full_v2210.exe",
        "display_name": "Lively Animated Wallpaper"
    }
}

EXTENSIONS_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico", ".heic", ".psd", ".ai"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv", ".rtf", ".odt", ".epub"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".dmg"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp"],
    "Programs": [".exe", ".msi", ".bat", ".sh", ".cmd", ".apk", ".jar"],
    "Code": [".py", ".html", ".css", ".js", ".json", ".xml", ".cpp", ".c", ".java", ".php"]
}

is_downloading = False

# --- GUI Window Setup ---
root = tk.Tk()
root.title("CYBER TECHNOLOGY System Toolkit")

# EXPANDED GEOMETRY: Prevents text cut-off on scaled 4K displays
root.geometry("900x400") 
root.configure(bg="#121212")
root.resizable(False, False)

# Windows Immersive Dark Mode Title Bar Alignment Fix
def apply_dark_title_bar(window):
    try:
        window.update()
        # DWM attribute to turn the native Windows outer title bar pure black/dark
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        rendering_policy = ctypes.c_int(2) # Active True flag
        
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 
            DWMWA_USE_IMMERSIVE_DARK_MODE, 
            ctypes.byref(rendering_policy), 
            ctypes.sizeof(rendering_policy)
        )
    except Exception:
        pass

apply_dark_title_bar(root)

# --- Core Logic Functions ---

def organize_files():
    target_dir = filedialog.askdirectory(title="Select Folder to Organize")
    if not target_dir:
        return

    moved_count = 0
    try:
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isdir(item_path):
                continue
                
            _, ext = os.path.splitext(item)
            ext = ext.lower()
            
            moved = False
            for folder_name, extensions in EXTENSIONS_MAP.items():
                if ext in extensions:
                    master_folder = os.path.join(target_dir, "[ Sorted Files ]")
                    dest_folder = os.path.join(master_folder, folder_name)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    shutil.move(item_path, os.path.join(dest_folder, item))
                    moved_count += 1
                    moved = True
                    break
            
            if not moved:
                master_folder = os.path.join(target_dir, "[ Sorted Files ]")
                others_folder = os.path.join(master_folder, "Others")
                if not os.path.exists(others_folder):
                    os.makedirs(others_folder)
                shutil.move(item_path, os.path.join(others_folder, item))
                moved_count += 1

        messagebox.showinfo("Success", f"Optimization complete!\n{moved_count} files successfully organized inside '[ Sorted Files ]'.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")


def run_all_downloads_pipeline():
    global is_downloading
    if is_downloading:
        return
        
    is_64bit = platform.machine().endswith('64') or os.environ.get("PROCESSOR_ARCHITECTURE") == "AMD64"
    if not is_64bit:
        messagebox.showerror(
            "Architecture Incompatible", 
            "Critical Error: An x64 operating system environment is required.\n32-bit (x32) systems are blocked."
        )
        return

    is_downloading = True
    download_all_btn.config(state="disabled", bg="#333333", fg="#666666")
    
    # --- [حل مشكلة الاختفاء والمجلدات] فحص ذكي لمسار سطح المكتب الفعلي ودعم OneDrive تلقائياً ---
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    onedrive_desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    
    if os.path.exists(onedrive_desktop):
        desktop_path = onedrive_desktop
        
    # حماية إضافية: التأكد من أن مسار سطح المكتب متوفر وصالح للكتابة
    if not os.path.exists(desktop_path):
        try:
            os.makedirs(desktop_path)
        except Exception:
            desktop_path = os.path.expanduser("~") # العودة للمجلد الرئيسي للمستخدم في حال فشل كل شيء
    # ----------------------------------------------------------------------------------------
    
    try:
        for app_key, target in DOWNLOADS.items():
            url = target["url"]
            filename = target["filename"]
            save_path = os.path.join(desktop_path, filename)
            
            status_label.config(text=f"Connecting to fetch {target['display_name']}...", fg="#FFFFFF")
            progress_bar['value'] = 0
            root.update_idletasks()
            
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            status_label.config(text=f"Downloading: {filename}")
            
            downloaded = 0
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            progress_bar['value'] = percent
                            root.update_idletasks()
                            
        status_label.config(text="All Downloads Complete!", fg="#00E676")
        messagebox.showinfo("Success", f"All software binaries successfully dropped onto your Desktop!\nPath: {desktop_path}")
        
    except Exception as e:
        status_label.config(text="Download failed.", fg="#FF1744")
        messagebox.showerror("Network Error", f"Transmission failure:\n{str(e)}")
        
    finally:
        is_downloading = False
        download_all_btn.config(state="normal", bg="#00E676", fg="#000000")

def trigger_download_thread():
    threading.Thread(target=run_all_downloads_pipeline, daemon=True).start()


# --- UI Layout Views ---

def show_view(frame):
    frame.tkraise()

# Sidebar Panel — Width widened to 220 to hold long titles perfectly under 4K scale
sidebar = tk.Frame(root, bg="#0A0A0A", width=220, height=400)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content_area = tk.Frame(root, bg="#121212")
content_area.pack(side="right", fill="both", expand=True)

organizer_view = tk.Frame(content_area, bg="#121212")
downloader_view = tk.Frame(content_area, bg="#121212")

for frame in (organizer_view, downloader_view):
    frame.grid(row=0, column=0, sticky="nsew")
content_area.grid_rowconfigure(0, weight=1)
content_area.grid_columnconfigure(0, weight=1)

# Sidebar Branding Header
sidebar_title = tk.Label(sidebar, text="CYBER TECH", fg="#00E676", bg="#0A0A0A", font=("Segoe UI", 13, "bold"))
sidebar_title.pack(pady=(30, 30))

# Sidebar View Toggles
btn_view_org = tk.Button(
    sidebar, text="File Organizer", command=lambda: show_view(organizer_view),
    fg="#FFFFFF", bg="#0A0A0A", activebackground="#121212", activeforeground="#00E676",
    font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2", anchor="w", padx=25, pady=12
)
btn_view_org.pack(fill="x")

btn_view_dl = tk.Button(
    sidebar, text="Software Downloader", command=lambda: show_view(downloader_view),
    fg="#FFFFFF", bg="#0A0A0A", activebackground="#121212", activeforeground="#00E676",
    font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2", anchor="w", padx=25, pady=12
)
btn_view_dl.pack(fill="x")

# --- VIEW 1: FILE ORGANIZER INTERFACE ---
org_title = tk.Label(organizer_view, text="@ALMM FILE File Organizer", fg="#FFFFFF", bg="#121212", font=("Segoe UI", 18, "bold"))
org_title.pack(pady=(60, 5))

org_sub = tk.Label(organizer_view, text="Clean up your workspace directory layout.", fg="#888888", bg="#121212", font=("Segoe UI", 11))
org_sub.pack(pady=(0, 40))

organize_btn = tk.Button(
    organizer_view, text="Select & Organize Folder", command=organize_files,
    fg="#000000", bg="#00E676", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2",
    activebackground="#00B254", activeforeground="#000000", padx=35, pady=12
)
organize_btn.pack()

# --- VIEW 2: DOWNLOADER INTERFACE ---
dl_title = tk.Label(downloader_view, text="@ALMM FILE ORGANIZER", fg="#FFFFFF", bg="#121212", font=("Segoe UI", 16, "bold"))
dl_title.pack(pady=(40, 10))

list_frame = tk.Frame(downloader_view, bg="#121212")
list_frame.pack(pady=5)

tk.Label(list_frame, text=f"• {DOWNLOADS['windhawk']['display_name']}", fg="#FFFFFF", bg="#121212", font=("Segoe UI", 11)).pack(anchor="w", pady=2)
tk.Label(list_frame, text=f"• {DOWNLOADS['lively']['display_name']}", fg="#FFFFFF", bg="#121212", font=("Segoe UI", 11)).pack(anchor="w", pady=2)

status_label = tk.Label(downloader_view, text="System Idle | Pipeline Ready", fg="#888888", bg="#121212", font=("Segoe UI", 10))
status_label.pack(pady=(25, 2))

style = ttk.Style()
style.theme_use('default')
style.configure("Horizontal.TProgressbar", background="#00E676", troughcolor="#222222", bordercolor="#121212", lightcolor="#00E676", darkcolor="#00E676")

progress_bar = ttk.Progressbar(downloader_view, orient="horizontal", length=400, mode="determinate", style="Horizontal.TProgressbar")
progress_bar.pack(pady=5)

download_all_btn = tk.Button(
    downloader_view, text="Download All Software", command=trigger_download_thread,
    fg="#000000", bg="#00E676", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2",
    activebackground="#00B254", activeforeground="#000000", padx=30, pady=10
)
download_all_btn.pack(pady=(15, 0))

# Initialize application frame state view
show_view(organizer_view)

root.mainloop()