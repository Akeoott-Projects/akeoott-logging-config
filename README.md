# akeoott-logging-config: The Effortless Python Logging Library

![PyPI - Version](https://img.shields.io/pypi/v/LogConfig.svg)
**Accidental yet powerful: a simple Python library for robust, configurable logging.**

akeoott-logging-config provides an incredibly easy-to-use, modular, and enterprise-ready logging solution designed to simplify logging setup for Python applications of any scale, from quick scripts to complex backend systems.<br>

> [!WARNING]
> This project is licensed under the GNU Lesser General Public License v3.0 (LGPL-3.0) - see the [LICENSE](https://www.gnu.org/licenses/lgpl-3.0.html) website or [LICENSE](https://github.com/Akeoottt/LogConfig/blob/main/LICENCE) file for details.

## ✨ Features

* **Effortless Setup:** Configure comprehensive logging with a single function call.
* **Zero Unwanted Logs:** Implements `NullHandler` by default, ensuring your library doesn't spam user consoles unless explicitly configured.
* **Highly Configurable:** Control log levels, output destinations (console, file), log formats, and date formats with flexible parameters.
* **Intelligent File Handling:** Automatically resolves log file paths, creates necessary directories, and handles common file-related issues gracefully.
* **Idempotent Configuration:** Safely call `setup` multiple times without creating duplicate log handlers.
* **Dedicated Logger:** Provides a named logger (`github_activity`) isolated from the root logger, preventing interference with other application logging.
* **Robust Error Reporting:** Logs internal errors during logging setup itself (e.g., file writing issues) to ensure visibility.
* **Cross-Platform Compatibility:** Utilizes `pathlib` for robust and platform-independent file path management.

## 🚀 Installation

You can install `akeoott-logging-config` directly from PyPI using pip:

```bash
pip install akeoott-logging-config
```
