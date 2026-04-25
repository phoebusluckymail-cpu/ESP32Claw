import socket
import sys   # 导入 sys 模块来接收命令行参数

ESP32_IP = "192.168.43.128"
ESP32_PORT = 7788

def send(cmd):
    # 发送及收取回复函数
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    sock.sendto(cmd.encode(), (ESP32_IP, ESP32_PORT))
    print(f"[发送] {cmd}")
    try:
        data, addr = sock.recvfrom(1024)
        print(f"[回复] {data.decode()}")
    except socket.timeout:
        print("[超时] 无回复")
    sock.close()

if __name__ == "__main__":
    # 获取用户在命令行里输入的第一个参数
    if len(sys.argv) < 2:
        print("用法: python led_control.py [on/off/status]")
        sys.exit(1)
    
    user_cmd = sys.argv[1].lower()
    
    # 根据参数调用相应的功能
    if user_cmd == "on":
        send("light on")
    elif user_cmd == "off":
        send("light off")
    elif user_cmd == "status":
        send("status")
    else:
        print(f"未知命令: {user_cmd}")