# ESP32 端网络配置模板
#
# 用法：
#   1. 复制本文件为同目录下的 config.py
#   2. 填入你自己的热点名称、密码与网络参数
#   3. 把 config.py 与 main.py 一起上传到 ESP32
#
# config.py 已被 .gitignore 忽略，不会被提交到仓库。

# ---------- WiFi 热点 ----------
WIFI_SSID = "your-wifi-ssid"
WIFI_PASSWORD = "your-wifi-password"

# ---------- 静态 IP ----------
# 需与主机端 esp32-light/led_control.py 里的 ESP32_IP 保持一致
STATIC_IP = "192.168.43.128"
SUBNET_MASK = "255.255.255.0"
GATEWAY = "192.168.43.1"
DNS = "192.168.43.1"

# ---------- UDP 监听端口 ----------
UDP_PORT = 7788
