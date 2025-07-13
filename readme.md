# 🦆 DuckAi

**DuckAi** is a lightweight Python client for DuckDuckGo's experimental AI chat interface, reverse-engineered and revived based on earlier implementations that no longer function.  
It allows you to send prompts to a variety of models through DuckDuckGo’s unofficial `duckchat` API.

---

## ✨ Features

- ✅ Supports multiple models: GPT-4o, Claude, LLaMA, Mixtral, and more  
- ✅ Automatically handles `x-vqd-hash` validation  
- ✅ Uses browser-like headers to avoid detection  
- ✅ Clean and minimal interface  
- ✅ Pythonic and production-ready

---

## 📦 Installation

```bash
pip install py_mini_racer requests
```

---

## 🚀 Quick Start

```python
from DuckAi import DuckAi

duck = DuckAi()
response = duck.chat("What is the capital of Iceland?")
print(response)
```

---

## 🤖 Available Models

You can use the `models()` method to see supported models:

```python
duck.models()
```

Returns:

```python
[
    "gpt-4o-mini",
    "o3-mini",
    "claude-3-haiku-20240307",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "mistralai/Mixtral-8x7B-Instruct-v0.1"
]
```

---

## 📜 Disclaimer

This project is based on an earlier version of a DuckDuckGo AI chat wrapper that no longer works. This version was refactored, modernized, and made operational again.

---

## ⚖️ Legal / DMCA

If you are a representative of DuckDuckGo or another affected party and believe this project violates your terms or policies, please contact me directly.

**📱 Signal contact:** `https://signal.me/#eu/q8RNQUVVlXzL577K_qXnYVlAtcD6rmAtwK3Cu5DfpWQB_28YcPZN8Zeu_HZoWgwT`

---


## 🐤 Not Affiliated

This project is **not affiliated with DuckDuckGo**. It is an independent, unofficial tool built for educational and personal use.
