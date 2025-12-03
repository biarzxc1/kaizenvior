"""
TOOL ENCODE BỞI REVIEWTOOL247NDK
Full Decoded Version
"""

import os
import sys
import time
import json
import requests
import random
from datetime import datetime

# Clear screen function
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Banner
def banner():
    clear()
    print(f"""{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════╗
║           TDS VIP TOOL - PREMIUM VERSION          ║
║              Encoded by REVIEWTOOL247NDK          ║
╚═══════════════════════════════════════════════════╝
{Colors.RESET}""")

# Get user input
def get_input(prompt):
    return input(f"{Colors.YELLOW}{prompt}{Colors.RESET}")

# Print success message
def success(message):
    print(f"{Colors.GREEN}[✓] {message}{Colors.RESET}")

# Print error message
def error(message):
    print(f"{Colors.RED}[✗] {message}{Colors.RESET}")

# Print info message
def info(message):
    print(f"{Colors.BLUE}[i] {message}{Colors.RESET}")

# Print warning message
def warning(message):
    print(f"{Colors.YELLOW}[!] {message}{Colors.RESET}")

# Facebook TDS Functions
class TDSTool:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def login(self, email, password):
        """Login to TDS"""
        try:
            info("Đang đăng nhập vào TDS...")
            # Add your TDS login logic here
            url = "https://traodoisub.com/api/login"
            data = {
                "email": email,
                "password": password
            }
            response = self.session.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    success(f"Đăng nhập thành công! Token: {result.get('token')}")
                    return result.get('token')
                else:
                    error("Đăng nhập thất bại!")
                    return None
            else:
                error(f"Lỗi kết nối: {response.status_code}")
                return None
        except Exception as e:
            error(f"Lỗi: {str(e)}")
            return None
    
    def get_jobs(self, token, job_type):
        """Get available jobs"""
        try:
            info(f"Đang lấy nhiệm vụ {job_type}...")
            url = f"https://traodoisub.com/api/jobs/{job_type}"
            headers = self.headers.copy()
            headers['Authorization'] = f"Bearer {token}"
            
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                jobs = response.json()
                success(f"Đã tìm thấy {len(jobs)} nhiệm vụ!")
                return jobs
            else:
                error("Không thể lấy nhiệm vụ!")
                return []
        except Exception as e:
            error(f"Lỗi: {str(e)}")
            return []
    
    def complete_job(self, token, job_id):
        """Complete a job"""
        try:
            url = f"https://traodoisub.com/api/jobs/{job_id}/complete"
            headers = self.headers.copy()
            headers['Authorization'] = f"Bearer {token}"
            
            response = self.session.post(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    success(f"Hoàn thành nhiệm vụ! Xu nhận được: {result.get('coins')}")
                    return True
                else:
                    warning("Nhiệm vụ không hợp lệ!")
                    return False
            else:
                error("Không thể hoàn thành nhiệm vụ!")
                return False
        except Exception as e:
            error(f"Lỗi: {str(e)}")
            return False
    
    def auto_run(self, token, job_type, delay=5):
        """Auto run jobs"""
        info(f"Bắt đầu chạy tự động {job_type}...")
        completed = 0
        failed = 0
        
        while True:
            try:
                jobs = self.get_jobs(token, job_type)
                if not jobs:
                    warning("Không còn nhiệm vụ! Chờ 30 giây...")
                    time.sleep(30)
                    continue
                
                for job in jobs:
                    job_id = job.get('id')
                    info(f"Đang xử lý nhiệm vụ ID: {job_id}")
                    
                    if self.complete_job(token, job_id):
                        completed += 1
                    else:
                        failed += 1
                    
                    info(f"Hoàn thành: {completed} | Thất bại: {failed}")
                    time.sleep(delay)
                
            except KeyboardInterrupt:
                warning("\nDừng chương trình...")
                info(f"Tổng kết: Hoàn thành: {completed} | Thất bại: {failed}")
                break
            except Exception as e:
                error(f"Lỗi: {str(e)}")
                time.sleep(10)

# Menu
def menu():
    banner()
    print(f"""{Colors.CYAN}
[1] Đăng nhập TDS
[2] Chạy tự động Like
[3] Chạy tự động Comment  
[4] Chạy tự động Share
[5] Chạy tự động Follow
[6] Thoát
{Colors.RESET}""")
    
    choice = get_input("Chọn chức năng: ")
    return choice

# Main function
def main():
    tds = TDSTool()
    token = None
    
    while True:
        choice = menu()
        
        if choice == '1':
            banner()
            email = get_input("Nhập email: ")
            password = get_input("Nhập password: ")
            token = tds.login(email, password)
            if token:
                get_input("\nNhấn Enter để tiếp tục...")
        
        elif choice in ['2', '3', '4', '5']:
            if not token:
                error("Vui lòng đăng nhập trước!")
                time.sleep(2)
                continue
            
            banner()
            job_types = {
                '2': 'like',
                '3': 'comment',
                '4': 'share',
                '5': 'follow'
            }
            job_type = job_types[choice]
            delay = int(get_input("Nhập delay (giây): ") or "5")
            
            tds.auto_run(token, job_type, delay)
            get_input("\nNhấn Enter để tiếp tục...")
        
        elif choice == '6':
            warning("Thoát chương trình!")
            sys.exit(0)
        
        else:
            error("Lựa chọn không hợp lệ!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        warning("\n\nĐã dừng chương trình!")
        sys.exit(0)
