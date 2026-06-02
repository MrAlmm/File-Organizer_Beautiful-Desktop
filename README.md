# 🛠️ WINDOWS CYBER TECHNOLOGY System Toolkit (4K Pro Edition)

![Version](https://img.shields.io/badge/Version-2.2%20%282026%29-00E676?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20%28x64%29-00E676?style=flat-square)
![UI](https://img.shields.io/badge/UI-Tkinter%20%7C%204K%20High--DPI-00E676?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-00E676?style=flat-square)

An immersive, dark-themed Windows management suite engineered for modern desktop environments. Combining automated high-speed file categorization with an asynchronous, architecture-aware utility deployment pipeline, this toolkit optimizes workflows without visual clutter.

Developed by **Lynx1 / CYBER TECHNOLOGY**.

---

## 📖 Table of Contents
1. [Key Features](#-key-features)
2. [Technical Deep Dive](#-technical-deep-dive)
3. [File Architecture Mapping](#-file-architecture-mapping)
4. [📥 Installation & Download Options](#-installation--download-options)
5. [🚀 Quick Start Guide](#-quick-start-guide)
6. [📋 Requirements & Guardrails](#-requirements--guardrails)
7. [🗺️ Future Development Roadmap](#%EF%B8%8F-future-development-roadmap)
8. [📄 License](#-license)

---

## ⚡ Key Features

* **Ultra-Crisp 4K Scale Integration:** Implements native Win32/Shcore DPI awareness wrappers to prevent text blur, low-res scaling bugs, and layout shifting on modern high-resolution displays.
* **Immersive Dark Mode Frame:** Direct Desktop Window Manager (DWM) attribute hooks seamlessly blend the native Windows system title bar into a pure-black dark aesthetic (`DWMWA_USE_IMMERSIVE_DARK_MODE`).
* **Intelligent File Organizer:** Parses chaotic directories, recursively processes items based on an explicit structural map, and safely isolates clutter inside neatly sorted target folders.
* **Asynchronous Software Provisioner:** Downloads required external customization binaries using non-blocking Python `threading` routines with live progress reporting, network validation wrappers, and native OneDrive fallback target checks.

---

## 🔬 Technical Deep Dive

### High-DPI & Fluid Rendering
Standard Tkinter interfaces scale poorly on high-resolution screens. This toolkit calls `SetProcessDpiAwareness(2)` inside `shcore.dll` directly upon initialization to enforce native system-level crisp rendering:
```python
ctypes.windll.shcore.SetProcessDpiAwareness(2)
