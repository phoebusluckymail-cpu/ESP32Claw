import machine
import network
import socket
import time

try:
    import config
except ImportError:
    raise SystemExit(
        "缺少 config.py：请复制 config.example.py 为 config.py，填好 WiFi 信息后重新上传"
    )


def send_response(message, target_ip, target_port):
    """发送回复到指定 IP 和端口"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), (target_ip, target_port))
        sock.close()
        print(f"📤 已回复: {message} -> {target_ip}:{target_port}")
    except Exception as e:
        print(f"回复失败: {e}")
        
def do_connect():  # 连接 WiFi 并设置静态 IP
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to {}...".format(config.WIFI_SSID))
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(0.5)  # ✅ 用 time.sleep() 代替 machine.idle()
            print(".", end="")
            timeout -= 0.5
    if wlan.isconnected():
        print("原有 network config:", wlan.ifconfig())
        STATIC_CONFIG = (
            config.STATIC_IP,     # 固定 IP
            config.SUBNET_MASK,   # 子网掩码
            config.GATEWAY,       # 网关
            config.DNS,           # DNS = 网关 ✅
        )
        wlan.ifconfig(STATIC_CONFIG)
        print("固定IP已设置:", wlan.ifconfig())

    return wlan

def creat_udp_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", config.UDP_PORT))
    print("UDP socket 已创建，实际监听端口:{}".format(config.UDP_PORT))
    return udp_socket

def main():
    wlan = do_connect()
    
    if not wlan.isconnected():
        print("无法连接 WiFi，程序退出，请检查 config.py 中的热点名称与密码")
        return
    
    udp_socket = creat_udp_socket()
    LED = machine.Pin(2,machine.Pin.OUT)
    while True:
        recv_data, sender_info = udp_socket.recvfrom(1024)
        recv_data_str = recv_data.decode("utf-8")
        print("{}发送的数据：{}".format(sender_info, recv_data_str))
        
        if recv_data_str == "light on":
            LED.value(1)
            print("LED 已点亮")
            udp_socket.sendto(b"LED is ON", sender_info)
            
        elif recv_data_str == "light off":
            LED.value(0)
            print("LED 已熄灭")
            udp_socket.sendto(b"LED is OFF", sender_info)
            
        elif recv_data_str == "status":
            status = "ON" if LED.value() else "OFF"
            udp_socket.sendto(f"LED is {status}", sender_info)
        
        
if __name__ == "__main__":
    main()
    
