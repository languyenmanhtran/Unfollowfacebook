"""
Facebook Unfollow Tool
Author: LNMT x KST
GitHub: https://github.com/languyenmanhtran
"""


import json
import os
import time
import requests
import re
from datetime import datetime
import platform
import threading
import random
import string
import html


# Màu sắc ANSI
class Colors:
    """Màu sắc cho terminal"""
    # Reset
    RESET = '\033[0m'
    
    # Màu chữ
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Màu chữ sáng
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Màu nền
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Style
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    @staticmethod
    def colorize(text, color, style=''):
        """Thêm màu và style cho text"""
        return f"{style}{color}{text}{Colors.RESET}"


CLEAR_CONSOLE = True  # Có clear màn hình giữa các bước hay không


def clear_screen():
    """Xóa màn hình console"""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def maybe_clear_screen():
    """Clear màn hình nếu người dùng bật tùy chọn CLEAR_CONSOLE"""
    if CLEAR_CONSOLE:
        clear_screen()


def typing_effect(text, delay=0.02):
    """Hiệu ứng gõ chữ từng ký tự"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def loading_spinner(message="Đang xử lý", duration=0.5):
    """Hiệu ứng loading spinner"""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        spinner = Colors.colorize(spinner_chars[i % len(spinner_chars)], Colors.BRIGHT_CYAN)
        msg_colored = Colors.colorize(message, Colors.BRIGHT_CYAN)
        print(f'\r{spinner} {msg_colored}...', end='', flush=True)
        time.sleep(0.1)
        i += 1
    print('\r' + ' ' * (len(message) + 20) + '\r', end='')  # Xóa dòng


def print_with_animation(text, color=Colors.BRIGHT_WHITE, style='', delay=0.01):
    """In text với hiệu ứng typing và màu"""
    colored_text = Colors.colorize(text, color, style)
    typing_effect(colored_text, delay)


def blink_text(text, color, times=3, duration=0.5):
    """Hiệu ứng nhấp nháy cho text"""
    for _ in range(times):
        print(f'\r{Colors.colorize(text, color, Colors.BOLD)}', end='', flush=True)
        time.sleep(duration)
        print('\r' + ' ' * len(text) + '\r', end='', flush=True)
        time.sleep(0.2)
    print(f'\r{Colors.colorize(text, color, Colors.BOLD)}', end='', flush=True)


def safe_console_text(text):
    """
    Chuẩn hóa string để in ra console Windows:
    - Loại surrogate (gây UnicodeEncodeError)
    - Loại bớt ký tự ngoài BMP (đa số emoji phức tạp) để tránh hiện '????'
    - Giữ lại chữ cái/dấu tiếng Việt bình thường
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    cleaned_chars = []
    for ch in text:
        code = ord(ch)
        # Bỏ surrogate
        if 0xD800 <= code <= 0xDFFF:
            continue
        # Bỏ các ký tự ngoài BMP (nhiều emoji phức tạp) để hạn chế '????' trên console yếu
        if code > 0xFFFF:
            continue
        cleaned_chars.append(ch)
    return ''.join(cleaned_chars)

def hacker_reveal(text, color=Colors.BRIGHT_MAGENTA, style=Colors.BOLD, steps=16, delay=0.03):
    """
    Hiệu ứng "hacker" random ký tự rồi dần dần hiện đúng chữ.
    Dùng cho dòng BY LNMT x KST / bản quyền.
    """
    charset = string.ascii_letters + string.digits + "!@#$%^&*"
    length = len(text)
    
    for step in range(steps):
        chars = []
        progress = step / (steps - 1) if steps > 1 else 1.0
        solid_until = int(progress * length)
        
        for i, ch in enumerate(text):
            if ch == ' ':
                chars.append(' ')
            elif i < solid_until:
                chars.append(ch)
            else:
                chars.append(random.choice(charset))
        
        line = ''.join(chars)
        colored = Colors.colorize(line, color, style)
        print('\r' + colored, end='', flush=True)
        time.sleep(delay)
    
    # In lại text chuẩn và xuống dòng
    final = Colors.colorize(text, color, style)
    print('\r' + final)


def extract_info_from_target(target):
    """Extract thông tin từ target URL"""
    name = 'Unknown'
    username = 'N/A'
    uid = 'N/A'
    
    # Extract UID từ target URL
    uid_patterns = [
        r'profile\.php\?id=(\d+)',
        r'/profile/(\d+)',
        r'facebook\.com/(\d+)/?$',
    ]
    for pattern in uid_patterns:
        match = re.search(pattern, str(target))
        if match:
            uid = match.group(1)
            break
    
    # Extract username từ target URL
    username_patterns = [
        r'facebook\.com/([^/?]+)/?$',
        r'facebook\.com/([^/?]+)\?',
    ]
    for pattern in username_patterns:
        match = re.search(pattern, str(target))
        if match:
            potential_username = match.group(1)
            # Nếu không phải là số (không phải UID), thì là username
            if not potential_username.isdigit() and potential_username not in ['profile.php', 'www', 'web', 'm']:
                username = potential_username
                break
    
    # Nếu target là số thuần, coi như là UID
    if str(target).strip().isdigit():
        uid = str(target).strip()
    
    return name, username, uid


def print_success_table(item=None, target=None, unfollow_time=None,
                        name=None, username=None, uid=None,
                        index=None, total=None, duration=None):
    """
    In trạng thái hủy đơn giản (không dùng bảng),
    nhưng vẫn giữ đủ thông tin: Tên | user | UID | thời gian.
    """
    if unfollow_time is None:
        unfollow_time = datetime.now()

    # Lấy thông tin từ item hoặc từ target
    if item:
        name = name or item.get('name', 'Unknown')
        username = username or item.get('username', 'N/A')
        uid = uid or item.get('uid', 'N/A')
        if not target and item.get('profileUrl'):
            target = item.get('profileUrl')
    if target and (not username or username == 'N/A' or not uid or uid == 'N/A'):
        _, extracted_username, extracted_uid = extract_info_from_target(target)
        if (not username or username == 'N/A') and extracted_username != 'N/A':
            username = extracted_username
        if (not uid or uid == 'N/A') and extracted_uid != 'N/A':
            uid = extracted_uid

    # Fallback
    if not name:
        name = 'Unknown'
    if not username:
        username = 'N/A'
    if not uid:
        uid = 'N/A'

    time_str = unfollow_time.strftime("%d/%m/%Y %H:%M:%S")
    duration_str = f"{duration:.1f}s" if duration is not None else "N/A"
    
    # Đếm số lượng nếu có index/total
    count_text = None
    if index is not None and total is not None:
        count_text = Colors.colorize(f"[{index}/{total}]", Colors.BRIGHT_YELLOW, Colors.BOLD)
    
    # Dòng 1: [Success] -> Name: ...
    status_tag = Colors.colorize("[Success]", Colors.BRIGHT_GREEN, Colors.BOLD)
    name_label = Colors.colorize("Name:", Colors.BRIGHT_GREEN)
    name_text = Colors.colorize(name, Colors.BRIGHT_WHITE)
    
    line1_parts = [status_tag]
    if count_text:
        line1_parts.append(count_text)
    line1_parts.append(f"-> {name_label} {name_text}")
    line1 = " ".join(line1_parts)
    
    # Dòng 2: -> User: ... | -> UID: ... | Thời gian: ... | Xử lý: ...s
    user_label = Colors.colorize("User:", Colors.BRIGHT_GREEN)
    user_text = Colors.colorize(str(username), Colors.BRIGHT_CYAN)
    uid_label = Colors.colorize("UID:", Colors.BRIGHT_GREEN)
    uid_text = Colors.colorize(str(uid), Colors.BRIGHT_MAGENTA)
    time_label = Colors.colorize("Thời gian:", Colors.BRIGHT_GREEN)
    time_val = Colors.colorize(time_str, Colors.BRIGHT_BLUE)
    dur_label = Colors.colorize("Xử lý:", Colors.BRIGHT_MAGENTA)
    dur_val = Colors.colorize(duration_str, Colors.BRIGHT_WHITE)
    
    line2 = (
        f"-> {user_label} {user_text} | "
        f"-> {uid_label} {uid_text} | "
        f"{time_label} {time_val} | "
        f"{dur_label} {dur_val}"
    )
    
    print("\n" + line1)
    print(line2)


class FacebookUnfollowTool:
    def __init__(self, debug=True, log_file=None):
        self.debug = debug
        self.session = requests.Session()
        self.log_history = []
        self.log_file = log_file  # File log handler để ghi tất cả log
    
    def log(self, message, level="INFO"):
        """In log với mã màu và ghi vào file nếu có"""
        colors = {
            "INFO": "\033[94m",      # Blue
            "SUCCESS": "\033[92m",   # Green
            "ERROR": "\033[91m",     # Red
            "WARNING": "\033[93m",   # Yellow
            "DEBUG": "\033[95m",     # Magenta
            "INPUT": "\033[96m"      # Cyan
        }
        reset = "\033[0m"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        self.log_history.append(log_msg)
        
        # Ghi vào file log nếu có
        if self.log_file:
            try:
                # Loại bỏ mã màu ANSI khi ghi vào file
                clean_msg = re.sub(r'\033\[[0-9;]*m', '', log_msg)
                # Thay thế ký tự surrogate / không encode được
                safe_clean = clean_msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                self.log_file.write(safe_clean + "\n")
                self.log_file.flush()  # Đảm bảo ghi ngay lập tức
            except Exception as e:
                # Nếu không thể ghi file, vẫn tiếp tục in ra console
                pass
        
        if self.debug:
            colored = f"{colors.get(level, '')}{log_msg}{reset}"
            try:
                print(colored)
            except UnicodeEncodeError:
                # Nếu console không in được (surrogate...), thay bằng ký tự an toàn
                safe_msg = log_msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                print(f"{colors.get(level, '')}{safe_msg}{reset}")
    
    def parse_cookie(self, cookie_string):
        """Phân tích cookie string thành dict"""
        try:
            self.log("🔍 Phân tích cookie string...", "DEBUG")
            result = {}
            
            # Loại bỏ dấu ; ở cuối nếu có
            cookie_string = cookie_string.strip().rstrip(';')
            
            # Thử split với '; '
            if '; ' in cookie_string:
                parts = cookie_string.split('; ')
            else:
                parts = cookie_string.split(';')
            
            for part in parts:
                part = part.strip()
                if part and '=' in part:
                    key, value = part.split('=', 1)
                    result[key.strip()] = value.strip()
            
            self.log(f"✅ Thành công: {len(result)} cookie items", "SUCCESS")
            
            # Hiển thị các key quan trọng
            important_keys = ['c_user', 'xs', 'fr', 'datr', 'sb']
            found_keys = [k for k in important_keys if k in result]
            self.log(f"   Tìm thấy keys quan trọng: {', '.join(found_keys)}", "DEBUG")
            
            return result
        except Exception as e:
            self.log(f"❌ Lỗi phân tích cookie: {str(e)}", "ERROR")
            return None
    
    def extract_target_id(self, url_or_id):
        """Trích xuất target ID từ URL hoặc UID trực tiếp"""
        try:
            self.log(f"🔍 Phân tích target: {url_or_id}", "DEBUG")
            
            # Nếu là số thuần thì là UID
            if url_or_id.strip().isdigit():
                self.log(f"✅ UID trực tiếp: {url_or_id}", "SUCCESS")
                return url_or_id.strip()
            
            # Nếu là URL
            if 'facebook.com' in url_or_id or 'fb.com' in url_or_id:
                # Loại bỏ protocol
                url_clean = url_or_id.replace('https://', '').replace('http://', '')
                self.log(f"   URL clean: {url_clean}", "DEBUG")
                
                # Kiểm tra profile.php?id=UID (ưu tiên cao nhất)
                if 'profile.php' in url_or_id and 'id=' in url_or_id:
                    match = re.search(r'[?&]id=(\d+)', url_or_id)
                    if match:
                        uid = match.group(1)
                        self.log(f"✅ Profile ID từ query param: {uid}", "SUCCESS")
                        return uid
                
                # Kiểm tra /profile/UID/ format
                if '/profile/' in url_or_id:
                    match = re.search(r'/profile/(\d+)/?', url_or_id)
                    if match:
                        uid = match.group(1)
                        self.log(f"✅ Profile ID từ path: {uid}", "SUCCESS")
                        return uid
                
                # Trích xuất phần path
                if '/' in url_clean:
                    path = url_clean.split('/', 1)[1]
                else:
                    path = url_clean
                
                # Lấy phần đầu tiên (username hoặc profile ID)
                target = path.split('?')[0].split('#')[0].strip('/')
                
                # Nếu target là số thì là UID
                if target.isdigit():
                    self.log(f"✅ UID từ path: {target}", "SUCCESS")
                    return target
                
                self.log(f"✅ Username/Path: {target}", "SUCCESS")
                return target
            
            self.log(f"⚠️ Input không rõ ràng, coi là username: {url_or_id}", "WARNING")
            return url_or_id.strip()
            
        except Exception as e:
            self.log(f"❌ Lỗi phân tích target: {str(e)}", "ERROR")
            return None
    
    def _extract_tokens_from_response(self, response_text, url_name=""):
        """Helper function để trích xuất tokens từ response text"""
        fb_dtsg = None
        lsd = None
        uid = None
        
        # Tìm fb_dtsg - nhiều cách khác nhau
        patterns_fb_dtsg = [
            r'["\']fb_dtsg["\']\s*:\s*["\']([A-Za-z0-9_-]+:[0-9]+:[0-9]+)["\']',
            r'fb_dtsg["\']?\s*[:=]\s*["\']([A-Za-z0-9_-]+:[0-9]+:[0-9]+)["\']',
            r'name=["\']fb_dtsg["\'][^>]*value=["\']([A-Za-z0-9_-]+:[0-9]+:[0-9]+)["\']',
            r'fb_dtsg["\']?\s*=\s*["\']([A-Za-z0-9_-]+:[0-9]+:[0-9]+)["\']',
            r'["\']fb_dtsg["\']\s*:\s*["\']([^"\']{20,})["\']',
            r'fb_dtsg["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
            r'\["DTSGInitialData",\[\],\{"token":"([^"]+)"',
            r'"dtsg":\{"token":"([^"]+)"',
            r'"DTSGInitialData",\[\],\{"token":"([^"]+)"',
            r'DTSGInitialData.*?token":"([^"]+)"',
            r'"DTSGInitialData"[^}]*"token"\s*:\s*"([^"]+)"',
            r'"__d"["\']?\s*:\s*["\']([^"\']+)',
            r'name="fb_dtsg"\s+value="([^"]+)"',
            r'\["DTSG",\[\],\{"token":"([^"]+)"',
            r'DTSG["\']?\s*:\s*["\']([^"\']+)',
            r'requireLazy\(\["DTSGInitialData"[^\]]+\]\s*,\s*0\s*,\s*function[^}]*"token"\s*:\s*"([^"]+)"',
            r'requireLazy\(\["DTSGInitialData"[^\]]*\]\s*,\s*0[^}]*"token"\s*:\s*"([^"]+)"',
            r'require\(\["DTSGInitialData"[^\]]*\]\s*,\s*0[^}]*"token"\s*:\s*"([^"]+)"',
            r'window\.__d\s*=\s*"([^"]+)"',
            r'data-dtsg="([^"]+)"',
        ]
        
        for i, pattern in enumerate(patterns_fb_dtsg, 1):
            try:
                match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
                if match:
                    fb_dtsg = match.group(1)
                    if len(fb_dtsg) > 10:
                        # Hiển thị full token để dễ debug (log file đã an toàn)
                        if url_name:
                            self.log(f"✅ Tìm thấy fb_dtsg từ {url_name} (cách {i}): {fb_dtsg}", "SUCCESS")
                        else:
                            self.log(f"✅ Tìm thấy fb_dtsg (cách {i}): {fb_dtsg}", "SUCCESS")
                        break
            except Exception as e:
                continue
        
        # Tìm lsd
        patterns_lsd = [
            r'["\']lsd["\']\s*:\s*["\']([A-Za-z0-9_-]{10,30})["\']',
            r'lsd["\']?\s*[:=]\s*["\']([A-Za-z0-9_-]{10,30})["\']',
            r'name=["\']lsd["\'][^>]*value=["\']([A-Za-z0-9_-]{10,30})["\']',
            r'lsd["\']?\s*=\s*["\']([A-Za-z0-9_-]{10,30})["\']',
            r'["\']lsd["\']\s*:\s*["\']([^"\']{8,50})["\']',
            r'lsd["\']?\s*[:=]\s*["\']([^"\']{8,50})["\']',
            r'"LSD",\[\],\{"token":"([^"]+)"',
            r'"LSD".*?token":"([^"]+)"',
            r'"lsd":"([^"]+)"',
            r'name="lsd"\s+value="([^"]+)"',
            r'\["LSD",\[\],\{"token":"([^"]+)"',
            r'LSD["\']?\s*:\s*["\']([^"\']+)',
            r'requireLazy\(\["LSD"[^\]]*\]\s*,\s*0[^}]*"token"\s*:\s*"([^"]+)"',
            r'require\(\["LSD"[^\]]*\]\s*,\s*0[^}]*"token"\s*:\s*"([^"]+)"',
            r'data-lsd="([^"]+)"',
            r'<meta[^>]*name=["\']lsd["\'][^>]*content=["\']([^"\']+)',
        ]
        
        for i, pattern in enumerate(patterns_lsd, 1):
            try:
                match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
                if match:
                    lsd = match.group(1)
                    if len(lsd) > 5:
                        # Hiển thị full token để dễ debug
                        if url_name:
                            self.log(f"✅ Tìm thấy lsd từ {url_name} (cách {i}): {lsd}", "SUCCESS")
                        else:
                            self.log(f"✅ Tìm thấy lsd (cách {i}): {lsd}", "SUCCESS")
                        break
            except:
                continue
        
        # Tìm UID
        patterns_uid = [
            r'"USER_ID":"([^"]+)"',
            r'"userID":"([^"]+)"',
            r'"actorID":"([^"]+)"',
            r'"viewerID":"([^"]+)"',
            r'"actor_id":"([^"]+)"',
        ]
        
        for i, pattern in enumerate(patterns_uid, 1):
            try:
                match = re.search(pattern, response_text, re.IGNORECASE)
                if match:
                    uid = match.group(1)
                    if url_name:
                        self.log(f"✅ Tìm thấy UID từ {url_name} (cách {i}): {uid}", "SUCCESS")
                    else:
                        self.log(f"✅ Tìm thấy UID (cách {i}): {uid}", "SUCCESS")
                    break
            except:
                continue
        
        return fb_dtsg, lsd, uid
    
    def _decode_unicode_name(self, name):
        """Decode Unicode escape sequences trong tên"""
        if not name:
            return name
        
        if any(ord(c) > 127 for c in name) and '\\u' not in name:
            return name
        
        if '\\u' in name:
            try:
                decoded = name.encode('utf-8').decode('unicode_escape')
                if decoded != name:
                    return decoded
            except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
                pass
            
            try:
                decoded = name.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
                if decoded != name:
                    return decoded
            except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
                pass
        
        return name

    def _is_probable_person_name(self, candidate_name: str) -> bool:
        """
        Heuristic: true nếu chuỗi trông giống tên người hơn là key kỹ thuật.
        Dùng chung logic với facebook_unfollow.py để tránh các tên như 'latency_level'.
        """
        if not candidate_name:
            return False
        name = candidate_name.strip()
        if not name:
            return False
        lower = name.lower()
        bad_exact = {"connection_quality", "latency_level"}
        if lower in bad_exact:
            return False
        if any(ch.isdigit() for ch in name):
            return False
        if "_" in name:
            return False
        tech_keywords = [
            "bundle", "worker", "opus", "webopus",
            "latency", "quality", "connection",
            "level", "metric", "experiment", "test",
        ]
        if any(k in lower for k in tech_keywords):
            return False
        has_space = " " in name
        has_accent = any(ord(c) > 127 for c in name)
        if not has_space and not has_accent:
            if len(name) <= 4:
                return False
        return True
    
    def get_facebook_tokens_with_name(self, cookies):
        """Lấy fb_dtsg, lsd, uid và name từ trang Facebook"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        urls_to_try = [
            ("https://www.facebook.com", "www.facebook.com"),
            ("https://web.facebook.com", "web.facebook.com"),
            ("https://m.facebook.com", "m.facebook.com"),
        ]
        
        fb_dtsg = None
        lsd = None
        uid = None
        name = None
        
        for url, url_name in urls_to_try:
            try:
                self.log(f"🌐 Thử truy cập {url_name} để lấy tokens...", "INFO")
                
                response = self.session.get(url, headers=headers, cookies=cookies, timeout=15, allow_redirects=True)
                
                if response.encoding is None or response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'
                
                self.log(f"   Status code: {response.status_code}", "DEBUG")
                self.log(f"   Response size: {len(response.text)} bytes", "DEBUG")
                self.log(f"   Encoding: {response.encoding}", "DEBUG")
                
                try:
                    response_text = response.text
                    if not isinstance(response_text, str):
                        response_text = response_text.decode('utf-8', errors='ignore')
                except:
                    response_text = response.content.decode('utf-8', errors='ignore')
                
                temp_fb_dtsg, temp_lsd, temp_uid = self._extract_tokens_from_response(response_text, url_name)
                
                if not name and response.status_code == 200:
                    name_patterns = [
                        (r'<div[^>]*role="button"[^>]*>([^<]+?)<span', 'profile button'),
                        (r'"name"\s*:\s*"([^"]+)"', 'JSON name'),
                        (r'"profile_owner":\{"id":"\d+","name":"([^"]+)"', 'profile_owner'),
                        (r'"actor":\{"id":"\d+","name":"([^"]+)"', 'actor'),
                        (r'"viewer":\{"id":"\d+","name":"([^"]+)"', 'viewer'),
                        (r'requireLazy\(\["ProfileCometUserInfoQuery"[^\]]*\]\s*,\s*0[^}]*"name"\s*:\s*"([^"]+)"', 'ProfileCometUserInfoQuery'),
                        (r'"ProfileCometUserInfoQuery"[^}]*"name"\s*:\s*"([^"]+)"', 'ProfileCometUserInfoQuery (alt)'),
                        (r'<title[^>]*>([^<]+)</title>', 'title tag'),
                    ]
                    
                    for pattern, pattern_name in name_patterns:
                        matches = re.findall(pattern, response_text, re.IGNORECASE | re.DOTALL)
                        for match in matches:
                            candidate_name = match.strip()
                            # Unescape HTML entities (&nbsp;, &zwj;...)
                            candidate_name = html.unescape(candidate_name)
                            candidate_name = candidate_name.replace(' | Facebook', '').replace(' - Facebook', '').replace('Facebook', '').strip()
                            
                            if not self._is_probable_person_name(candidate_name):
                                continue
                            
                            name = self._decode_unicode_name(candidate_name)
                            self.log(f"✅ Tìm thấy tên từ {url_name} (pattern: {pattern_name}): {name}", "SUCCESS")
                            break
                        if name:
                            break
                
                if temp_fb_dtsg and temp_lsd:
                    fb_dtsg = temp_fb_dtsg
                    lsd = temp_lsd
                    if temp_uid:
                        uid = temp_uid
                    self.log(f"✅ Thành công lấy tokens từ {url_name}!", "SUCCESS")
                    break
                else:
                    if temp_fb_dtsg and not fb_dtsg:
                        fb_dtsg = temp_fb_dtsg
                    if temp_lsd and not lsd:
                        lsd = temp_lsd
                    if temp_uid and not uid:
                        uid = temp_uid
                    
            except Exception as e:
                self.log(f"⚠️ Lỗi khi truy cập {url_name}: {str(e)}", "WARNING")
                continue
        
        if not fb_dtsg:
            self.log("❌ Không tìm thấy fb_dtsg từ tất cả các URL", "ERROR")
        if not lsd:
            self.log("❌ Không tìm thấy lsd từ tất cả các URL", "ERROR")
        if not uid:
            self.log("⚠️ Không tìm thấy UID", "WARNING")
        
        return fb_dtsg, lsd, uid, name
    
    def get_user_info(self, cookie_string):
        """Lấy thông tin user từ cookie: UID, NAME, TOKENS"""
        try:
            self.log("🔍 Đang lấy thông tin user từ cookie...", "INFO")
            
            cookies = self.parse_cookie(cookie_string)
            if not cookies:
                return None
            
            # Hỗ trợ cả tài khoản thường (c_user) và profile phụ / TikTik (i_user)
            c_uid = cookies.get('c_user')
            i_uid = cookies.get('i_user')
            
            if i_uid and c_uid and i_uid != c_uid:
                self.log(f"ℹ️  Phát hiện tài khoản có profile phụ (i_user={i_uid}) và tài khoản gốc (c_user={c_uid})", "INFO")
                # Ưu tiên dùng i_user làm UID/actor_id (đúng với request CometUserUnfollowMutation mới)
                uid = i_uid
            else:
                uid = i_uid or c_uid
            
            if not uid:
                self.log("❌ Không tìm thấy c_user / i_user trong cookie", "ERROR")
                return None
            
            self.log(f"✅ UID: {uid}", "SUCCESS")
            
            self.log("🔍 Đang lấy tokens (fb_dtsg, lsd)...", "INFO")
            fb_dtsg, lsd, uid_from_token, name_from_token = self.get_facebook_tokens_with_name(cookies)
            
            if not fb_dtsg or not lsd:
                self.log("❌ Không thể lấy được tokens", "ERROR")
                return None
            
            name = name_from_token or 'Unknown'
            
            result = {
                'uid': uid,                  # UID đang dùng làm actor_id (ưu tiên i_user nếu có)
                'name': name,
                'fb_dtsg': fb_dtsg,
                'lsd': lsd,
                'cookies': cookies,
                'c_user': c_uid,
                'i_user': i_uid,
            }
            
            self.log(f"✅ Đã lấy thông tin user thành công!", "SUCCESS")
            if name:
                self.log(f"   Tên: {name}", "SUCCESS")
            self.log(f"   UID (actor_id): {uid}", "SUCCESS")
            if c_uid:
                self.log(f"   c_user: {c_uid}", "DEBUG")
            if i_uid:
                self.log(f"   i_user: {i_uid}", "DEBUG")
            # In full tokens để dễ debug
            self.log(f"   fb_dtsg: {fb_dtsg}", "SUCCESS")
            self.log(f"   lsd: {lsd}", "SUCCESS")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Lỗi khi lấy thông tin user: {str(e)}", "ERROR")
            return None
    
    def get_uid_from_username(self, username, cookies, fb_dtsg, lsd):
        """Lấy UID từ username"""
        try:
            self.log(f"🔍 Đang lấy UID từ username: {username}", "INFO")
            
            urls_to_try = [
                f"https://www.facebook.com/{username}",
                f"https://web.facebook.com/{username}",
                f"https://m.facebook.com/{username}",
            ]
            
            # Headers đầy đủ (KHÔNG dùng Accept-Encoding để tránh nén response)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                # KHÔNG dùng Accept-Encoding để tránh response bị nén
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            }
            
            # Nhiều patterns để tìm UID (giống facebook_unfollow.py)
            patterns = [
                # Profile owner patterns
                r'"profile_owner"\s*:\s*\{[^}]*"id"\s*:\s*"(\d+)"',
                r'"profile_owner":\{"id":"(\d+)"',
                r'profile_owner.*?"id"\s*:\s*"(\d+)"',
                
                # User ID patterns
                r'"userID"\s*:\s*"(\d+)"',
                r'"USER_ID"\s*:\s*"(\d+)"',
                r'"actorID"\s*:\s*"(\d+)"',
                r'"viewerID"\s*:\s*"(\d+)"',
                r'"actor_id"\s*:\s*"(\d+)"',
                
                # Profile URL patterns
                r'/profile\.php\?id=(\d+)',
                r'/profile/(\d+)/',
                r'profile\.php\?id=(\d+)',
                
                # Entity ID patterns
                r'"entity_id"\s*:\s*"(\d+)"',
                r'"profile_id"\s*:\s*"(\d+)"',
                r'profile_id:"(\d+)"',
                
                # GraphQL patterns
                r'"id"\s*:\s*"(\d+)"[^}]*"__typename"\s*:\s*"User"',
                r'"__typename"\s*:\s*"User"[^}]*"id"\s*:\s*"(\d+)"',
                
                # Meta tags
                r'<meta[^>]*property=["\']fb://profile/(\d+)["\']',
                r'<meta[^>]*content=["\'](\d+)["\'][^>]*property=["\']al:android:url',
                
                # JavaScript patterns
                r'profileID["\']?\s*[:=]\s*["\']?(\d+)',
                r'userID["\']?\s*[:=]\s*["\']?(\d+)',
                r'actorID["\']?\s*[:=]\s*["\']?(\d+)',
                
                # URL trong response
                r'facebook\.com/profile\.php\?id=(\d+)',
                r'facebook\.com/profile/(\d+)',
                
                # GraphQL response patterns
                r'"unsubscribee_id"\s*:\s*"(\d+)"',
                r'"target_id"\s*:\s*"(\d+)"',
            ]
            
            for url in urls_to_try:
                try:
                    self.log(f"   Thử URL: {url}", "DEBUG")
                    # Cập nhật referer cho mỗi URL
                    url_headers = headers.copy()
                    url_headers['Referer'] = 'https://www.facebook.com/'
                    response = self.session.get(url, headers=url_headers, cookies=cookies, timeout=15, allow_redirects=True)
                    
                    self.log(f"   Response status: {response.status_code}", "DEBUG")
                    
                    if response.status_code != 200:
                        self.log(f"   ⚠️ Status code không phải 200: {response.status_code}", "DEBUG")
                        # Log response body khi có lỗi để debug
                        if response.status_code in [400, 403, 404]:
                            try:
                                error_body = response.text[:500] if len(response.text) > 500 else response.text
                                self.log(f"   Response body (first 500 chars): {error_body}", "DEBUG")
                            except:
                                pass
                        continue
                    
                    # Xử lý encoding (giống facebook_unfollow.py)
                    if response.encoding is None or response.encoding == 'ISO-8859-1':
                        response.encoding = 'utf-8'
                    
                    # Kiểm tra xem response có phải text hợp lệ không
                    try:
                        # Thử decode lại để đảm bảo
                        response_text = response.text
                        if not isinstance(response_text, str):
                            response_text = response_text.decode('utf-8', errors='ignore')
                    except:
                        # Nếu có lỗi, thử decode với errors='ignore'
                        response_text = response.content.decode('utf-8', errors='ignore')
                    
                    self.log(f"   Response length: {len(response_text)} chars", "DEBUG")
                    
                    # Thử tất cả patterns
                    for i, pattern in enumerate(patterns, 1):
                        try:
                            matches = re.findall(pattern, response_text, re.IGNORECASE | re.DOTALL)
                            for match in matches:
                                uid = match if isinstance(match, str) else match[0] if isinstance(match, tuple) else str(match)
                                if uid.isdigit() and len(uid) > 5 and len(uid) < 20:  # UID thường từ 6-19 chữ số
                                    # Kiểm tra xem UID này có phải là của profile owner không (không phải viewer)
                                    # Nếu UID trùng với c_user thì bỏ qua
                                    if uid != cookies.get('c_user', ''):
                                        self.log(f"✅ Tìm thấy UID (pattern {i}) từ {url}: {uid}", "SUCCESS")
                                        return uid
                        except Exception as e:
                            continue
                    
                    # Nếu không tìm thấy, thử tìm trong script tags (giống facebook_unfollow.py)
                    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', response_text, re.DOTALL | re.IGNORECASE)
                    for script_content in script_matches:
                        for j, pattern in enumerate(patterns, 1):
                            try:
                                matches = re.findall(pattern, script_content, re.IGNORECASE | re.DOTALL)
                                for match in matches:
                                    uid = match if isinstance(match, str) else match[0] if isinstance(match, tuple) else str(match)
                                    if uid.isdigit() and len(uid) > 5 and len(uid) < 20:
                                        if uid != cookies.get('c_user', ''):
                                            self.log(f"✅ Tìm thấy UID trong script (pattern {j}) từ {url}: {uid}", "SUCCESS")
                                            return uid
                            except:
                                continue
                    
                    # Nếu không tìm thấy, log một phần response để debug
                    if self.debug:
                        # Kiểm tra xem response có phải text hợp lệ không
                        if len(response_text) > 0 and response_text[0].isprintable():
                            sample_text = response_text[:500] if len(response_text) > 500 else response_text
                            self.log(f"   Sample response (first 500 chars): {sample_text[:200]}...", "DEBUG")
                        else:
                            self.log(f"   ⚠️ Response có vẻ bị nén hoặc không phải text", "DEBUG")
                    
                except Exception as e:
                    self.log(f"⚠️ Lỗi khi truy cập {url}: {str(e)}", "WARNING")
                    continue
            
            self.log(f"❌ Không thể lấy UID từ username: {username} sau khi thử tất cả URL", "ERROR")
            return None
            
        except Exception as e:
            self.log(f"⚠️ Lỗi khi lấy UID: {str(e)}", "WARNING")
            import traceback
            if self.debug:
                self.log(f"   Traceback: {traceback.format_exc()}", "DEBUG")
            return None
    
    def extract_target_id(self, url_or_id):
        """Trích xuất target ID từ URL hoặc UID"""
        try:
            if url_or_id.strip().isdigit():
                return url_or_id.strip()
            
            if 'facebook.com' in url_or_id or 'fb.com' in url_or_id:
                url_clean = url_or_id.replace('https://', '').replace('http://', '')
                
                if 'profile.php' in url_or_id and 'id=' in url_or_id:
                    match = re.search(r'[?&]id=(\d+)', url_or_id)
                    if match:
                        return match.group(1)
                
                if '/profile/' in url_or_id:
                    match = re.search(r'/profile/(\d+)/?', url_or_id)
                    if match:
                        return match.group(1)
                
                if '/' in url_clean:
                    path = url_clean.split('/', 1)[1]
                else:
                    path = url_clean
                
                target = path.split('?')[0].split('#')[0].strip('/')
                
                if target.isdigit():
                    return target
                
                return target
            
            return url_or_id.strip()
            
        except Exception as e:
            return None
    
    def unfollow_with_tokens(self, user_info, target_url, silent=False, allow_username=True):
        """Thực hiện hủy theo dõi với token có sẵn"""
        try:
            if not target_url or len(target_url.strip()) < 2:
                self.log("❌ Target (URL/UID) trống", "ERROR")
                return False
            
            actor_id = user_info['uid']
            fb_dtsg = user_info['fb_dtsg']
            lsd = user_info['lsd']
            cookies = user_info['cookies']
            
            target_id = self.extract_target_id(target_url)
            if not target_id:
                if not silent or self.debug:
                    self.log(f"❌ Không thể extract target_id từ: {target_url}", "ERROR")
                return False
            
            if not target_id.isdigit():
                # Batch mode: chỉ dùng UID trong file, không resolve username nữa
                if not allow_username:
                    if not silent or self.debug:
                        self.log(f"⚠️ Batch mode yêu cầu UID (chỉ số). Bỏ qua target: {target_url}", "WARNING")
                    return False
                if not silent or self.debug:
                    self.log(f"🔍 Target không phải UID, đang lấy UID từ username: {target_id}", "DEBUG")
                actual_uid = self.get_uid_from_username(target_id, cookies, fb_dtsg, lsd)
                if actual_uid:
                    if not silent or self.debug:
                        self.log(f"✅ Tìm thấy UID: {actual_uid} từ username: {target_id}", "SUCCESS")
                    target_id = actual_uid
                else:
                    if not silent or self.debug:
                        self.log(f"❌ Không thể lấy UID từ username: {target_id}", "ERROR")
                    return False
            
            current_timestamp = int(time.time() * 1000)
            variables_data = {
                "action_render_location": "WWW_COMET_FRIEND_MENU",
                "input": {
                    "attribution_id_v2": f"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,{current_timestamp},622244,250100865708545,,",
                    "is_tracking_encrypted": False,
                    "subscribe_location": "PROFILE",
                    "tracking": None,
                    "unsubscribee_id": str(target_id),
                    "actor_id": str(actor_id),
                    "client_mutation_id": "1"
                },
                "scale": 3
            }
            
            current_time = int(time.time())
            payload = {
                'av': actor_id,
                '__aaid': '0',
                '__user': actor_id,
                '__a': '1',
                '__req': str(int(time.time() * 100) % 100),
                'dpr': '1',
                '__ccg': 'GOOD',
                'fb_dtsg': fb_dtsg,
                'jazoest': str(int(time.time()) % 100000),
                'lsd': lsd,
                '__spin_r': str(current_time),
                '__spin_b': 'trunk',
                '__spin_t': str(current_time),
                '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute',
                '__comet_req': '15',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometUserUnfollowMutation',
                'server_timestamps': 'true',
                'doc_id': '25804465272546872',
                'variables': json.dumps(variables_data)
            }
            
            url = "https://web.facebook.com/api/graphql/"
            
            if self.debug and not silent:
                self.log(f"🌐 Request URL: {url}", "DEBUG")
                self.log(f"🎯 Target ID: {target_id}", "DEBUG")
                self.log(f"👤 Actor ID: {actor_id}", "DEBUG")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'sec-ch-ua-full-version-list': '"Not(A:Brand";v="8.0.0.0", "Chromium";v="144.0.7559.60"',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144"',
                'x-fb-friendly-name': 'CometUserUnfollowMutation',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '"NX789J"',
                'x-asbd-id': '359341',
                'x-fb-lsd': lsd,
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'origin': 'https://web.facebook.com',
                'x-requested-with': 'mark.via.gp',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': f'https://web.facebook.com/{target_id}',
                'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                'priority': 'u=1, i',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
            }
            
            response = self.session.post(url, data=payload, headers=headers, cookies=cookies, timeout=20)
            
            response_text = response.text
            if response_text.startswith('for (;;);'):
                response_text = response_text[9:]
            
            # Log response status
            if not silent or self.debug:
                self.log(f"📡 Response Status: {response.status_code}", "DEBUG")
            
            try:
                response_json = json.loads(response_text)
                
                if 'error' in response_json:
                    error_msg = response_json.get('error', {})
                    error_str = json.dumps(error_msg, ensure_ascii=False) if isinstance(error_msg, dict) else str(error_msg)
                    if not silent or self.debug:
                        self.log(f"❌ API Error: {error_str}", "ERROR")
                    return False
                
                if 'errors' in response_json and response_json['errors']:
                    errors = response_json['errors']
                    error_details = []
                    for err in errors:
                        if isinstance(err, dict):
                            error_msg = err.get('message', str(err))
                            error_code = err.get('code', 'N/A')
                            error_details.append(f"Code: {error_code}, Message: {error_msg}")
                        else:
                            error_details.append(str(err))
                    if not silent or self.debug:
                        self.log(f"❌ API Errors: {'; '.join(error_details)}", "ERROR")
                    return False
                
                if 'data' in response_json:
                    data = response_json.get('data', {})
                    if data:
                        # Kiểm tra xem có actor_unsubscribe không
                        unsubscribe_data = data.get('actor_unsubscribe', {})
                        if unsubscribe_data:
                            subscribe_status = unsubscribe_data.get('subscribe_status', 'UNKNOWN')
                            if not silent or self.debug:
                                self.log(f"✅ Hủy theo dõi thành công! Status: {subscribe_status}", "SUCCESS")
                            return True
                        else:
                            if not silent or self.debug:
                                self.log(f"⚠️ Response có data nhưng không có actor_unsubscribe. Data: {json.dumps(data, ensure_ascii=False)[:200]}", "WARNING")
                            return False
                    else:
                        if not silent or self.debug:
                            self.log(f"⚠️ Response có 'data' nhưng data rỗng", "WARNING")
                        return False
                else:
                    if not silent or self.debug:
                        self.log(f"⚠️ Response không có 'data'. Response keys: {list(response_json.keys())}", "WARNING")
                        if self.debug:
                            self.log(f"📄 Full response: {json.dumps(response_json, ensure_ascii=False)[:500]}", "DEBUG")
                    return False
                    
            except json.JSONDecodeError as e:
                if not silent or self.debug:
                    self.log(f"❌ JSON Decode Error: {str(e)}", "ERROR")
                    self.log(f"📄 Response text (first 500 chars): {response_text[:500]}", "DEBUG")
                return False
            
        except requests.exceptions.Timeout:
            if not silent or self.debug:
                self.log(f"❌ Request timeout khi hủy theo dõi {target_url}", "ERROR")
            return False
        except requests.exceptions.RequestException as e:
            if not silent or self.debug:
                self.log(f"❌ Request Exception: {str(e)}", "ERROR")
            return False
        except Exception as e:
            if not silent or self.debug:
                self.log(f"❌ Lỗi không mong muốn: {str(e)}", "ERROR")
                import traceback
                if self.debug:
                    self.log(f"📋 Traceback: {traceback.format_exc()}", "DEBUG")
            return False
    
    def unfollow_single(self, cookie_string, target_url):
        """Hủy theo dõi 1 người"""
        try:
            header_line = Colors.colorize("="*80, Colors.BRIGHT_CYAN, Colors.BOLD)
            title_text = Colors.colorize("🎯 HỦY THEO DÕI 1 NGƯỜI", Colors.BRIGHT_YELLOW, Colors.BOLD)
            
            print("\n" + header_line)
            print(title_text)
            print(header_line)
            
            # Lấy thông tin user
            loading_msg = Colors.colorize("\n🔍 Đang lấy thông tin user...", Colors.BRIGHT_CYAN, Colors.BOLD)
            print(loading_msg)
            user_info = self.get_user_info(cookie_string)
            
            if not user_info:
                error_msg = Colors.colorize("❌ Không thể lấy thông tin user hoặc token!", Colors.BRIGHT_RED, Colors.BOLD)
                print(error_msg)
                return False
            
            # Hiển thị thông tin
            info_line = Colors.colorize("\n" + "="*80, Colors.BRIGHT_CYAN)
            info_header = Colors.colorize("📋 THÔNG TIN USER", Colors.BRIGHT_YELLOW, Colors.BOLD)
            
            print(info_line)
            print(info_header)
            print(info_line)
            
            name_label = Colors.colorize("👤 Tên:", Colors.BRIGHT_GREEN, Colors.BOLD)
            uid_label = Colors.colorize("🆔 UID:", Colors.BRIGHT_GREEN, Colors.BOLD)
            
            safe_name_single = safe_console_text(user_info['name'])
            safe_uid_single = safe_console_text(user_info['uid'])
            print(f"{name_label} {Colors.colorize(safe_name_single, Colors.BRIGHT_WHITE)}")
            print(f"{uid_label} {Colors.colorize(safe_uid_single, Colors.BRIGHT_WHITE)}")
            print(info_line)
            
            # Thực hiện unfollow với loading effect
            target_msg = Colors.colorize("\n🔍 Đang hủy theo dõi:", Colors.BRIGHT_CYAN, Colors.BOLD)
            target_value = Colors.colorize(target_url, Colors.BRIGHT_WHITE)
            print(f"{target_msg} {target_value}")
            
            # Hiệu ứng loading
            loading_spinner("Đang xử lý", 0.5)
            start_unfollow = time.time()
            result = self.unfollow_with_tokens(user_info, target_url, silent=False)
            
            if result:
                # Lấy thời gian hủy
                unfollow_time = datetime.now()
                duration = time.time() - start_unfollow
                
                # In trạng thái thành công với thời gian xử lý
                print_success_table(target=target_url, unfollow_time=unfollow_time, duration=duration)
            else:
                # Hiệu ứng thất bại
                error_msg = "❌ ❌ ❌ HỦY THEO DÕI THẤT BẠI! ❌ ❌ ❌"
                print()
                blink_text(error_msg, Colors.BRIGHT_RED, times=3, duration=0.2)
                print()
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
            return False


class BatchUnfollowTool:
    def __init__(self, cookie_string, json_file_path, delay_between_requests=2, debug=True, verbose=False, num_threads=5):
        """
        Khởi tạo tool batch unfollow
        
        Args:
            cookie_string: Cookie Facebook
            json_file_path: Đường dẫn đến file JSON chứa danh sách following
            delay_between_requests: Thời gian chờ giữa các request (giây)
            debug: Bật/tắt debug mode (cho unfollow tool)
            verbose: Hiển thị log chi tiết từ unfollow tool (False = chỉ hiển thị kết quả)
        """
        self.cookie_string = cookie_string
        self.json_file_path = json_file_path
        self.delay_between_requests = delay_between_requests
        self.debug = debug
        self.verbose = verbose
        self.num_threads = max(1, min(int(num_threads), 10))  # 1-10 luồng
        
        # Log file (sẽ được tạo sau)
        self.log_file = None
        
        # Khởi tạo tool unfollow
        # Dùng chung debug flag với toàn bộ tool (bật/tắt một nơi ở menu chính)
        # Log file sẽ được set sau khi tạo
        self.unfollow_tool = FacebookUnfollowTool(debug=debug, log_file=None)
        
        # Kết quả
        self.results = {
            'success': [],
            'failed': [],
            'skipped': []
        }
    
    def load_json_file(self):
        """Đọc file JSON chứa danh sách following"""
        try:
            if not os.path.exists(self.json_file_path):
                error_msg = f"{Colors.colorize('❌ File không tồn tại:', Colors.BRIGHT_RED, Colors.BOLD)} {Colors.colorize(self.json_file_path, Colors.BRIGHT_WHITE)}"
                print(error_msg)
                return None
            
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            success_msg = f"{Colors.colorize('✅ Đã đọc', Colors.BRIGHT_GREEN)} {Colors.colorize(str(len(data)), Colors.BRIGHT_YELLOW, Colors.BOLD)} {Colors.colorize('người từ file JSON', Colors.BRIGHT_GREEN)}"
            print(success_msg)
            return data
            
        except json.JSONDecodeError as e:
            error_msg = f"{Colors.colorize('❌ Lỗi parse JSON:', Colors.BRIGHT_RED, Colors.BOLD)} {Colors.colorize(str(e), Colors.BRIGHT_RED)}"
            print(error_msg)
            return None
        except Exception as e:
            error_msg = f"{Colors.colorize('❌ Lỗi đọc file:', Colors.BRIGHT_RED, Colors.BOLD)} {Colors.colorize(str(e), Colors.BRIGHT_RED)}"
            print(error_msg)
            return None
    
    def get_target_from_item(self, item):
        """
        Lấy target (URL hoặc UID) từ item trong JSON
        
        Batch mode: CHỈ dùng UID từ file (không resolve username).
        (Vì tool extractor đã có nút "Lấy UID" để fill UID sẵn trong JSON)
        """
        uid_val = item.get('uid')
        if uid_val is None:
            return None
        uid_str = str(uid_val).strip()
        return uid_str if uid_str.isdigit() else None
    
    def create_log_file(self):
        """Tạo file log để ghi kết quả"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"unfollow_log_{timestamp}.txt"
        
        try:
            # Sử dụng errors='replace' để tránh lỗi surrogate khi ghi file log
            self.log_file = open(log_filename, 'w', encoding='utf-8', errors='replace')
            self.log_file.write("="*80 + "\n")
            self.log_file.write("BATCH UNFOLLOW LOG - TẤT CẢ LOG\n")
            self.log_file.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.log_file.write(f"File JSON: {self.json_file_path}\n")
            self.log_file.write(f"Debug Mode: {'BẬT' if self.debug else 'TẮT'}\n")
            self.log_file.write(f"Verbose Mode: {'BẬT' if self.verbose else 'TẮT'}\n")
            self.log_file.write("="*80 + "\n\n")
            
            # Set log_file cho unfollow_tool để ghi tất cả log
            self.unfollow_tool.log_file = self.log_file
            
            return log_filename
        except Exception as e:
            print(f"⚠️ Không thể tạo file log: {str(e)}")
            return None
    
    def log_result(self, message):
        """Ghi log vào file và console (an toàn Unicode)"""
        if message is None:
            return
        
        # Chuẩn hóa để loại surrogate / ký tự không hợp lệ
        safe_message = safe_console_text(message)
        
        if self.log_file:
            self.log_file.write(safe_message + "\n")
            self.log_file.flush()
        
        if self.debug:
            print(safe_message)
    
    def run(self):
        """Chạy batch unfollow"""
        banner_line = Colors.colorize("="*80, Colors.BRIGHT_CYAN, Colors.BOLD)
        batch_title = Colors.colorize("BATCH UNFOLLOW TOOL", Colors.BRIGHT_YELLOW, Colors.BOLD)
        batch_author_raw = "BY LNMT x KST"
        batch_author = Colors.colorize(batch_author_raw, Colors.BRIGHT_MAGENTA, Colors.BOLD)
        batch_github = Colors.colorize("Github: https://github.com/languyenmanhtran", Colors.BRIGHT_CYAN)
        batch_bio = Colors.colorize("BIO   : https://languyenmanhtran.netlify.app", Colors.BRIGHT_CYAN)
        
        print("\n" + banner_line)
        print(banner_line)
        print(batch_title)
        # Hiệu ứng hacker cho dòng bản quyền trong batch
        hacker_reveal(batch_author_raw, color=Colors.BRIGHT_MAGENTA, style=Colors.BOLD, steps=14, delay=0.03)
        print(batch_github)
        print(batch_bio)
        print(banner_line)
        print(banner_line)
        
        # Đọc file JSON
        file_msg = Colors.colorize(f"\n📂 Đang đọc file:", Colors.BRIGHT_CYAN) + f" {Colors.colorize(self.json_file_path, Colors.BRIGHT_WHITE)}"
        print(file_msg)
        following_list = self.load_json_file()
        
        if not following_list:
            error_msg = Colors.colorize("❌ Không thể đọc file JSON!", Colors.BRIGHT_RED, Colors.BOLD)
            print(error_msg)
            return
        
        # Tạo log file
        log_filename = self.create_log_file()
        if log_filename:
            log_msg = Colors.colorize("📝 File log:", Colors.BRIGHT_GREEN) + f" {Colors.colorize(log_filename, Colors.BRIGHT_WHITE)}"
            print(log_msg)
        
        # Lấy thông tin user và token một lần (nếu chưa có)
        if not hasattr(self, 'user_info') or not self.user_info:
            loading_msg = Colors.colorize(f"\n🔍 Đang lấy thông tin user và token...", Colors.BRIGHT_CYAN, Colors.BOLD)
            print(loading_msg)
            user_info = self.unfollow_tool.get_user_info(self.cookie_string)
            
            if not user_info:
                error_msg = Colors.colorize("❌ Không thể lấy thông tin user hoặc token!", Colors.BRIGHT_RED, Colors.BOLD)
                print(error_msg)
                if self.log_file:
                    self.log_file.close()
                return
            
            self.user_info = user_info
        else:
            user_info = self.user_info
            success_msg = Colors.colorize(f"\n✅ Sử dụng thông tin user đã lấy trước đó", Colors.BRIGHT_GREEN)
            print(success_msg)
        
        # Hiển thị thông tin
        info_line = Colors.colorize("\n" + "="*80, Colors.BRIGHT_CYAN)
        info_header = Colors.colorize("📋 THÔNG TIN USER", Colors.BRIGHT_YELLOW, Colors.BOLD)
        
        print(info_line)
        print(info_header)
        print(info_line)
        
        name_label = Colors.colorize("👤 Tên:", Colors.BRIGHT_GREEN, Colors.BOLD)
        uid_label = Colors.colorize("🆔 UID:", Colors.BRIGHT_GREEN, Colors.BOLD)
        fb_dtsg_label = Colors.colorize("🔑 fb_dtsg:", Colors.BRIGHT_GREEN, Colors.BOLD)
        lsd_label = Colors.colorize("🔑 lsd:", Colors.BRIGHT_GREEN, Colors.BOLD)
        
        safe_name_batch = safe_console_text(user_info['name'])
        safe_uid_batch = safe_console_text(user_info['uid'])
        safe_fb_dtsg_batch = safe_console_text(user_info['fb_dtsg'][:30] + '...')
        safe_lsd_batch = safe_console_text(user_info['lsd'][:30] + '...')
        
        print(f"{name_label} {Colors.colorize(safe_name_batch, Colors.BRIGHT_WHITE)}")
        print(f"{uid_label} {Colors.colorize(safe_uid_batch, Colors.BRIGHT_WHITE)}")
        print(f"{fb_dtsg_label} {Colors.colorize(safe_fb_dtsg_batch, Colors.BRIGHT_WHITE)}")
        print(f"{lsd_label} {Colors.colorize(safe_lsd_batch, Colors.BRIGHT_WHITE)}")
        print(info_line)
        
        # Ghi vào log (hiển thị full token để dễ debug)
        self.log_result(f"\nTHÔNG TIN USER:")
        self.log_result(f"Tên: {user_info['name']}")
        self.log_result(f"UID: {user_info['uid']}")
        self.log_result(f"fb_dtsg: {user_info['fb_dtsg']}")
        self.log_result(f"lsd: {user_info['lsd']}")
        
        # Cảnh báo (không hỏi lại, tự động tiếp tục)
        warning_header = Colors.colorize(f"\n⚠️  CẢNH BÁO:", Colors.BRIGHT_YELLOW, Colors.BOLD)
        warning_text1 = f"   Bạn sắp hủy theo dõi {Colors.colorize(str(len(following_list)), Colors.BRIGHT_RED, Colors.BOLD)} người!"
        warning_text2 = f"   Thời gian ước tính: {Colors.colorize(f'{len(following_list) * self.delay_between_requests / 60:.1f} phút', Colors.BRIGHT_YELLOW)}"
        warning_text3 = f"   Delay giữa các request: {Colors.colorize(f'{self.delay_between_requests} giây', Colors.BRIGHT_YELLOW)}"
        
        print(warning_header)
        print(warning_text1)
        print(warning_text2)
        print(warning_text3)
        
        # Bắt đầu batch
        start_line = Colors.colorize("\n" + "="*80, Colors.BRIGHT_CYAN, Colors.BOLD)
        start_title = Colors.colorize("🚀 BẮT ĐẦU BATCH UNFOLLOW", Colors.BRIGHT_GREEN, Colors.BOLD)
        
        print(start_line)
        print(start_title)
        print(start_line + "\n")
        
        self.log_result(f"\nBắt đầu unfollow {len(following_list)} người...\n")
        
        total = len(following_list)
        success_count = 0
        failed_count = 0
        skipped_count = 0
        start_time = time.time()
        
        # Đa luồng: mỗi luồng xử lý đúng danh sách riêng, không trùng link
        index_lock = threading.Lock()
        print_lock = threading.Lock()
        counter = {'idx': 0}
        
        def worker(thread_id):
            # Mỗi luồng dùng 1 session riêng để tránh xung đột
            local_tool = FacebookUnfollowTool(debug=self.verbose, log_file=self.log_file)
            local_tool.session = requests.Session()
            
            nonlocal success_count, failed_count, skipped_count
            
            while True:
                with index_lock:
                    if counter['idx'] >= total:
                        return
                    counter['idx'] += 1
                    idx = counter['idx']
                    item = following_list[idx - 1]
                
                name = item.get('name', 'Unknown')
                target = self.get_target_from_item(item)
                
                # Lấy UID để hiển thị
                uid_display = None
                if item.get('uid') and str(item['uid']).isdigit():
                    uid_display = str(item['uid'])
                elif target and str(target).isdigit():
                    uid_display = str(target)
                
                # Hiệu ứng hacker cho từng người (giữ màn hình gọn bằng lock)
                base_line = f"[LNMTxKST]-> [{idx}/{total}] Đang unfollow UID: {uid_display or 'N/A'} | Name: {name}"
                with print_lock:
                    print()
                    hacker_reveal(base_line, color=Colors.BRIGHT_CYAN, style=Colors.BOLD, steps=16, delay=0.02)
                    # Sau hiệu ứng, in lại 1 dòng với màu chi tiết
                    prefix = Colors.colorize(f"[LNMTxKST]-> [{idx}/{total}]", Colors.BRIGHT_CYAN, Colors.BOLD)
                    name_col = Colors.colorize("Name:", Colors.BRIGHT_GREEN)
                    name_val = Colors.BRIGHT_WHITE + name + Colors.RESET
                    uid_col = Colors.colorize("UID:", Colors.BRIGHT_GREEN)
                    uid_val = Colors.colorize(uid_display or 'N/A', Colors.BRIGHT_MAGENTA)
                    colored_line = f"{prefix} Đang unfollow {uid_col} {uid_val} | {name_col} {name_val}"
                    print(colored_line)
                
                if not target:
                    with print_lock:
                        warning_msg = Colors.colorize(f"⚠️  Không có thông tin target, bỏ qua", Colors.BRIGHT_YELLOW)
                        print(warning_msg)
                    with index_lock:
                        self.results['skipped'].append({
                            'index': idx,
                            'name': name,
                            'reason': 'No target info'
                        })
                        skipped_count += 1
                    self.log_result(f"[{idx}/{total}] SKIPPED: {name} - Không có target")
                    continue
                
                if self.verbose:
                    with print_lock:
                        target_msg = f"   {Colors.colorize('Target:', Colors.CYAN)} {Colors.colorize(target, Colors.BRIGHT_WHITE)}"
                        print(target_msg)
                
                try:
                    start_unfollow = time.time()
                    # Dùng unfollow_with_tokens với token có sẵn
                    result = local_tool.unfollow_with_tokens(
                        user_info=user_info,
                        target_url=target,
                        silent=not self.verbose,  # Silent nếu không verbose
                        allow_username=False  # Batch: chỉ dùng UID trong file
                    )
                    
                    if result:
                        unfollow_time = datetime.now()
                        duration = time.time() - start_unfollow
                        
                        with print_lock:
                            print_success_table(item, target, unfollow_time,
                                                index=idx, total=total, duration=duration)
                        
                        with index_lock:
                            self.results['success'].append({
                                'index': idx,
                                'name': name,
                                'target': target,
                                'username': item.get('username', 'N/A'),
                                'uid': item.get('uid', 'N/A'),
                                'time': unfollow_time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                            success_count += 1
                        self.log_result(f"[{idx}/{total}] SUCCESS: {name} - {target} - {unfollow_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        failed_icon = Colors.colorize('❌', Colors.BRIGHT_RED, Colors.BOLD)
                        failed_label = Colors.colorize('THẤT BẠI:', Colors.BRIGHT_RED, Colors.BOLD)
                        failed_text = f"{failed_icon} {failed_label} Không thể hủy theo dõi {Colors.colorize(name, Colors.BRIGHT_WHITE)}"
                        with print_lock:
                            print(failed_text)
                        
                        with index_lock:
                            self.results['failed'].append({
                                'index': idx,
                                'name': name,
                                'target': target
                            })
                            failed_count += 1
                        self.log_result(f"[{idx}/{total}] FAILED: {name} - {target}")
                
                except Exception as e:
                    error_msg = f"{Colors.colorize('❌ LỖI:', Colors.BRIGHT_RED, Colors.BOLD)} {Colors.colorize(str(e), Colors.BRIGHT_RED)}"
                    with print_lock:
                        print(error_msg)
                    with index_lock:
                        self.results['failed'].append({
                            'index': idx,
                            'name': name,
                            'target': target,
                            'error': str(e)
                        })
                        failed_count += 1
                    self.log_result(f"[{idx}/{total}] ERROR: {name} - {target} - {str(e)}")
                
                # Delay giữa các request trên CÙNG 1 luồng (tránh spam quá nhanh)
                time.sleep(self.delay_between_requests)
        
        # Tạo và chạy các luồng
        threads = []
        for t_id in range(self.num_threads):
            t = threading.Thread(target=worker, args=(t_id + 1,), daemon=True)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Tổng kết với hiệu ứng
        total_time = time.time() - start_time
        total_min = int(total_time // 60)
        total_sec = int(total_time % 60)
        
        summary_line = Colors.colorize("\n" + "="*80, Colors.BRIGHT_CYAN, Colors.BOLD)
        summary_header = Colors.colorize("📊 TỔNG KẾT", Colors.BRIGHT_YELLOW, Colors.BOLD)
        
        # Hiệu ứng fade in cho tổng kết
        print()  # Dòng trống
        time.sleep(0.2)
        typing_effect(summary_line, 0.01)
        time.sleep(0.1)
        typing_effect(summary_header, 0.03)
        time.sleep(0.1)
        typing_effect(summary_line, 0.01)
        
        success_label = Colors.colorize("✅ Thành công:", Colors.BRIGHT_GREEN, Colors.BOLD)
        success_value = f"{Colors.colorize(f'{success_count}/{total}', Colors.BRIGHT_WHITE)} ({Colors.colorize(f'{success_count/total*100:.1f}%', Colors.BRIGHT_GREEN)})"
        
        failed_label = Colors.colorize("❌ Thất bại:", Colors.BRIGHT_RED, Colors.BOLD)
        failed_value = f"{Colors.colorize(f'{failed_count}/{total}', Colors.BRIGHT_WHITE)} ({Colors.colorize(f'{failed_count/total*100:.1f}%', Colors.BRIGHT_RED)})"
        
        skipped_label = Colors.colorize("⚠️  Bỏ qua:", Colors.BRIGHT_YELLOW, Colors.BOLD)
        skipped_value = f"{Colors.colorize(f'{skipped_count}/{total}', Colors.BRIGHT_WHITE)} ({Colors.colorize(f'{skipped_count/total*100:.1f}%', Colors.BRIGHT_YELLOW)})"
        
        time_label = Colors.colorize("⏱️  Thời gian:", Colors.BRIGHT_CYAN, Colors.BOLD)
        time_value = Colors.colorize(f"{total_min}ph {total_sec}s", Colors.BRIGHT_WHITE)
        
        print(f"{success_label} {success_value}")
        print(f"{failed_label} {failed_value}")
        print(f"{skipped_label} {skipped_value}")
        print(f"{time_label} {time_value}")
        
        if success_count > 0:
            avg_time = total_time / success_count
            avg_label = Colors.colorize("⚡ Trung bình:", Colors.BRIGHT_MAGENTA, Colors.BOLD)
            avg_value = Colors.colorize(f"{avg_time:.1f}s/người", Colors.BRIGHT_WHITE)
            print(f"{avg_label} {avg_value}")
        
        print(summary_line)
        
        # Ghi tổng kết vào log
        total_time = time.time() - start_time
        total_min = int(total_time // 60)
        total_sec = int(total_time % 60)
        
        self.log_result("\n" + "="*80)
        self.log_result("TỔNG KẾT")
        self.log_result("="*80)
        self.log_result(f"Tổng số: {total}")
        self.log_result(f"Thành công: {success_count} ({success_count/total*100:.1f}%)")
        self.log_result(f"Thất bại: {failed_count} ({failed_count/total*100:.1f}%)")
        self.log_result(f"Bỏ qua: {skipped_count} ({skipped_count/total*100:.1f}%)")
        self.log_result(f"Thời gian: {total_min}ph {total_sec}s")
        if success_count > 0:
            avg_time = total_time / success_count
            self.log_result(f"Trung bình: {avg_time:.1f}s/người")
        self.log_result("="*80)
        
        # Ghi chi tiết failed
        if self.results['failed']:
            self.log_result("\n\nDANH SÁCH THẤT BẠI:")
            self.log_result("-"*80)
            for item in self.results['failed']:
                self.log_result(f"[{item['index']}] {item['name']} - {item.get('target', 'N/A')}")
                if 'error' in item:
                    self.log_result(f"     Lỗi: {item['error']}")
        
        # Đóng file log
        if self.log_file:
            self.log_file.close()
            log_saved_msg = f"\n{Colors.colorize('📝 Đã lưu log vào:', Colors.BRIGHT_GREEN)} {Colors.colorize(log_filename, Colors.BRIGHT_WHITE)}"
            print(log_saved_msg)
        
        # Lưu kết quả JSON
        result_json_file = f"unfollow_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        try:
            with open(result_json_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            json_saved_msg = f"{Colors.colorize('📄 Đã lưu kết quả JSON vào:', Colors.BRIGHT_GREEN)} {Colors.colorize(result_json_file, Colors.BRIGHT_WHITE)}"
            print(json_saved_msg)
        except Exception as e:
            error_msg = f"{Colors.colorize('⚠️  Không thể lưu file JSON:', Colors.BRIGHT_YELLOW)} {Colors.colorize(str(e), Colors.BRIGHT_RED)}"
            print(error_msg)


if __name__ == "__main__":
    # Banner có màu với hiệu ứng
    clear_screen()
    # Dòng dấu "=" ngắn, gọn hơn
    banner_line = Colors.colorize("="*40, Colors.BRIGHT_CYAN, Colors.BOLD)
    title = Colors.colorize("FACEBOOK UNFOLLOW TOOL", Colors.BRIGHT_YELLOW, Colors.BOLD)
    author_raw = "BY LNMT x KST"
    author = Colors.colorize(author_raw, Colors.BRIGHT_MAGENTA, Colors.BOLD)
    github_line = Colors.colorize("Github: https://github.com/languyenmanhtran", Colors.BRIGHT_CYAN)
    bio_line = Colors.colorize("BIO   : https://languyenmanhtran.netlify.app", Colors.BRIGHT_CYAN)
    
    # Màn hình chào đơn giản
    print("\n" + banner_line)
    typing_effect(title, 0.03)
    # Hiệu ứng "hacker" cho dòng bản quyền LNMT x KST
    hacker_reveal(author_raw, color=Colors.BRIGHT_MAGENTA, style=Colors.BOLD, steps=18, delay=0.03)
    typing_effect(github_line, 0.02)
    typing_effect(bio_line, 0.02)
    typing_effect(banner_line, 0.01)
    time.sleep(0.3)
    
    # Menu bật/tắt debug
    debug_title = Colors.colorize("🔧 CÀI ĐẶT DEBUG:", Colors.BRIGHT_BLUE, Colors.BOLD)
    debug_tip1 = Colors.colorize("   💡 Debug mode:", Colors.CYAN) + " Hiển thị log chi tiết (thông tin request, response, tokens...)"
    debug_tip2 = Colors.colorize("   💡 Non-debug:", Colors.CYAN) + " Chỉ hiển thị kết quả (gọn gàng hơn)"
    
    # Hiển thị phần debug từ từ cho đẹp
    typing_effect(f"\n{debug_title}", 0.02)
    time.sleep(0.05)
    typing_effect(debug_tip1, 0.015)
    typing_effect(debug_tip2, 0.015)
    
    debug_prompt = Colors.colorize("\n🔍 Bật debug mode?", Colors.BRIGHT_YELLOW) + " (y/n, mặc định n): "
    debug_input = input(debug_prompt).strip().lower()
    debug_mode = debug_input in ['y', 'yes', 'có', 'co']
    
    # Hỏi có muốn tự động clear màn hình giữa các bước hay không
    clear_prompt = Colors.colorize("🧹 Mỗi bước có clear màn hình không?", Colors.BRIGHT_YELLOW) + " (y/n, mặc định y): "
    clear_input = input(clear_prompt).strip().lower()
    CLEAR_CONSOLE = False if clear_input in ['n', 'no', 'k', 'khong', 'không'] else True
    
    maybe_clear_screen()
    
    # Menu chọn chức năng
    print("\n" + banner_line)
    print(banner_line)
    print(title)
    print(author)
    print(banner_line)
    print(banner_line)
    
    debug_status = Colors.colorize("BẬT", Colors.BRIGHT_GREEN, Colors.BOLD) if debug_mode else Colors.colorize("TẮT", Colors.BRIGHT_RED, Colors.BOLD)
    print(f"\n{Colors.colorize('🔧 Debug mode:', Colors.BRIGHT_BLUE)} {debug_status}")
    
    func_title = Colors.colorize("\n📋 CHỌN CHỨC NĂNG:", Colors.BRIGHT_CYAN, Colors.BOLD)
    func1 = Colors.colorize("   1️⃣  Hủy theo dõi 1 người", Colors.BRIGHT_GREEN)
    func2 = Colors.colorize("   2️⃣  Hủy theo dõi theo file (Batch)", Colors.BRIGHT_GREEN)
    
    print(func_title)
    print(func1)
    print(func2)
    
    choice_prompt = Colors.colorize("\n👉 Chọn", Colors.BRIGHT_YELLOW) + " (1 hoặc 2): "
    choice = input(choice_prompt).strip()
    
    if choice not in ['1', '2']:
        error_msg = Colors.colorize("❌ Lựa chọn không hợp lệ!", Colors.BRIGHT_RED, Colors.BOLD)
        print(error_msg)
        exit(1)
    
    maybe_clear_screen()
    
    # Nhập cookie
    print("\n" + banner_line)
    print(banner_line)
    print(title)
    print(author)
    print(banner_line)
    print(banner_line)
    print(f"\n{Colors.colorize('🔧 Debug mode:', Colors.BRIGHT_BLUE)} {debug_status}")
    
    step1_title = Colors.colorize("\n📥 BƯỚC 1: Nhập Cookie Facebook", Colors.BRIGHT_CYAN, Colors.BOLD)
    tip_icon = Colors.colorize("   💡", Colors.CYAN)
    warning_icon = Colors.colorize("      ⚠️", Colors.BRIGHT_YELLOW, Colors.BOLD)
    warning_text = Colors.colorize("KHÔNG chia sẻ cookie này cho ai!", Colors.BRIGHT_RED, Colors.BOLD)
    
    print(step1_title)
    print(f"{tip_icon} Cách lấy cookie:")
    print(f"      1. Vào {Colors.colorize('https://facebook.com', Colors.BRIGHT_BLUE)}")
    print(f"      2. Bấm {Colors.colorize('F12', Colors.BRIGHT_YELLOW)} → {Colors.colorize('Application', Colors.BRIGHT_YELLOW)} → {Colors.colorize('Cookies', Colors.BRIGHT_YELLOW)} → {Colors.colorize('facebook.com', Colors.BRIGHT_YELLOW)}")
    print(f"      3. Tìm cookie ({Colors.colorize('c_user', Colors.BRIGHT_GREEN)}, {Colors.colorize('xs', Colors.BRIGHT_GREEN)}, {Colors.colorize('fr', Colors.BRIGHT_GREEN)}...)")
    print(f"      4. Copy và paste dưới đây")
    print(f"{warning_icon} {warning_text}")
    
    cookie_prompt = Colors.colorize("\n🍪 Nhập cookie", Colors.BRIGHT_YELLOW) + ": "
    cookie = input(cookie_prompt).strip()
    
    if not cookie:
        error_msg = Colors.colorize("❌ Cookie không được để trống!", Colors.BRIGHT_RED, Colors.BOLD)
        print(error_msg)
        exit(1)
    
    maybe_clear_screen()
    
    # Lấy thông tin user
    print("\n" + banner_line)
    print(banner_line)
    print(title)
    print(author)
    print(banner_line)
    print(banner_line)
    print(f"\n{Colors.colorize('🔧 Debug mode:', Colors.BRIGHT_BLUE)} {debug_status}")
    
    loading_msg = Colors.colorize("🔍 Đang lấy thông tin user và token", Colors.BRIGHT_CYAN, Colors.BOLD)
    print(f"\n{loading_msg}...")
    temp_tool = FacebookUnfollowTool(debug=debug_mode)
    
    # Hiệu ứng loading trong khi lấy thông tin
    loading_done = False
    
    def show_loading():
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while not loading_done:
            print(f'\r{spinner_chars[i % len(spinner_chars)]} {loading_msg}...', end='', flush=True)
            time.sleep(0.1)
            i += 1
    
    if not debug_mode:
        loading_thread = threading.Thread(target=show_loading, daemon=True)
        loading_thread.start()
    
    user_info = temp_tool.get_user_info(cookie)
    loading_done = True
    
    if not debug_mode:
        print('\r' + ' ' * 60 + '\r', end='')  # Xóa loading
        print(f"{Colors.colorize('✅', Colors.BRIGHT_GREEN)} {loading_msg} {Colors.colorize('thành công!', Colors.BRIGHT_GREEN)}")
    
    if not user_info:
        error_msg = Colors.colorize("❌ Không thể lấy thông tin user hoặc token!", Colors.BRIGHT_RED, Colors.BOLD)
        tip_msg = Colors.colorize("   💡", Colors.CYAN) + " Kiểm tra lại cookie hoặc thử lại sau"
        print(error_msg)
        print(tip_msg)
        exit(1)
    
    maybe_clear_screen()
    
    # Hiển thị thông tin user (không in lại banner để tránh thừa dòng)
    user_info_title = Colors.colorize("\n" + "="*80, Colors.BRIGHT_CYAN)
    user_info_header = Colors.colorize("📋 THÔNG TIN USER", Colors.BRIGHT_YELLOW, Colors.BOLD)
    
    print(user_info_title)
    print(user_info_header)
    print(user_info_title)
    
    name_label = Colors.colorize("👤 Tên:", Colors.BRIGHT_GREEN, Colors.BOLD)
    uid_label = Colors.colorize("🆔 UID:", Colors.BRIGHT_GREEN, Colors.BOLD)
    fb_dtsg_label = Colors.colorize("🔑 fb_dtsg:", Colors.BRIGHT_GREEN, Colors.BOLD)
    lsd_label = Colors.colorize("🔑 lsd:", Colors.BRIGHT_GREEN, Colors.BOLD)
    
    safe_name = safe_console_text(user_info['name'])
    safe_uid = safe_console_text(user_info['uid'])
    safe_fb_dtsg = safe_console_text(user_info['fb_dtsg'][:40] + '...')
    safe_lsd = safe_console_text(user_info['lsd'][:40] + '...')
    
    print(f"{name_label} {Colors.colorize(safe_name, Colors.BRIGHT_WHITE)}")
    print(f"{uid_label} {Colors.colorize(safe_uid, Colors.BRIGHT_WHITE)}")
    print(f"{fb_dtsg_label} {Colors.colorize(safe_fb_dtsg, Colors.BRIGHT_WHITE)}")
    print(f"{lsd_label} {Colors.colorize(safe_lsd, Colors.BRIGHT_WHITE)}")
    print(user_info_title)
    
    # Xử lý theo lựa chọn
    if choice == '1':
        # CHỨC NĂNG 1: Hủy theo dõi 1 người
        step2_title = Colors.colorize("\n📥 BƯỚC 2: Nhập thông tin người cần hủy theo dõi", Colors.BRIGHT_CYAN, Colors.BOLD)
        format_tip = Colors.colorize("   💡 Định dạng chấp nhận:", Colors.CYAN)
        
        print(step2_title)
        print(format_tip)
        print(f"      - {Colors.colorize('https://facebook.com/username', Colors.BRIGHT_BLUE)}")
        print(f"      - {Colors.colorize('facebook.com/username', Colors.BRIGHT_BLUE)}")
        print(f"      - {Colors.colorize('100095322046752', Colors.BRIGHT_GREEN)} (UID trực tiếp)")
        print(f"      - {Colors.colorize('https://www.facebook.com/profile/100095322046752/', Colors.BRIGHT_BLUE)}")
        
        target_prompt = Colors.colorize("\n🔗 Nhập URL/UID", Colors.BRIGHT_YELLOW) + ": "
        target = input(target_prompt).strip()
        
        if not target:
            error_msg = Colors.colorize("❌ URL/UID không được để trống!", Colors.BRIGHT_RED, Colors.BOLD)
            print(error_msg)
            exit(1)
        
        # Tạo log file cho single unfollow
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"unfollow_single_log_{timestamp}.txt"
        try:
            log_file = open(log_filename, 'w', encoding='utf-8')
            log_file.write("="*80 + "\n")
            log_file.write("SINGLE UNFOLLOW LOG - TẤT CẢ LOG\n")
            log_file.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Target: {target}\n")
            log_file.write(f"Debug Mode: {'BẬT' if debug_mode else 'TẮT'}\n")
            log_file.write("="*80 + "\n\n")
            
            # Set log_file cho temp_tool để ghi tất cả log
            temp_tool.log_file = log_file
            
            log_msg = Colors.colorize("📝 File log:", Colors.BRIGHT_GREEN) + f" {Colors.colorize(log_filename, Colors.BRIGHT_WHITE)}"
            print(log_msg)
        except Exception as e:
            print(f"⚠️ Không thể tạo file log: {str(e)}")
            log_file = None
        
        maybe_clear_screen()
        
        # Thực hiện unfollow
        result = False
        try:
            result = temp_tool.unfollow_single(cookie, target)
        except Exception as e:
            if log_file:
                try:
                    log_file.write(f"\n❌ Exception: {str(e)}\n")
                except:
                    pass
        finally:
            # Đóng file log (luôn luôn đóng, kể cả khi có exception)
            if log_file:
                try:
                    log_file.write("\n" + "="*80 + "\n")
                    result_status = 'THÀNH CÔNG' if result else 'THẤT BẠI'
                    log_file.write(f"Kết quả: {result_status}\n")
                    log_file.write("="*80 + "\n")
                    log_file.close()
                    log_saved_msg = f"\n{Colors.colorize('📝 Đã lưu log vào:', Colors.BRIGHT_GREEN)} {Colors.colorize(log_filename, Colors.BRIGHT_WHITE)}"
                    print(log_saved_msg)
                except Exception as e:
                    pass
        
        if result:
            # Hiệu ứng thành công với blink
            success_msg = "✅ Hoàn tất!"
            blink_text(success_msg, Colors.BRIGHT_GREEN, times=2, duration=0.3)
            print()
        else:
            # Hiệu ứng lỗi
            error_msg = "❌ Có lỗi xảy ra!"
            blink_text(error_msg, Colors.BRIGHT_RED, times=2, duration=0.3)
            print()
    
    elif choice == '2':
        # CHỨC NĂNG 2: Hủy theo dõi theo file
        step2_title = Colors.colorize("\n📥 BƯỚC 2: Nhập đường dẫn file JSON", Colors.BRIGHT_CYAN, Colors.BOLD)
        json_tip = Colors.colorize("   💡", Colors.CYAN) + " File JSON phải chứa danh sách following (từ tool extract)"
        
        print(step2_title)
        print(json_tip)
        
        json_prompt = Colors.colorize("\n📂 Nhập đường dẫn file JSON", Colors.BRIGHT_YELLOW) + " (hoặc Enter để dùng mẫu): "
        json_file = input(json_prompt).strip()
        
        if not json_file:
            # Tìm file JSON mới nhất trong thư mục hiện tại
            json_files = [f for f in os.listdir('.') if f.startswith('facebook_following_') and f.endswith('.json')]
            if json_files:
                json_file = sorted(json_files, key=os.path.getmtime, reverse=True)[0]
                info_msg = Colors.colorize(f"   ℹ️  Sử dụng file mới nhất:", Colors.CYAN) + f" {Colors.colorize(json_file, Colors.BRIGHT_GREEN)}"
                print(info_msg)
            else:
                error_msg = Colors.colorize("❌ Không tìm thấy file JSON!", Colors.BRIGHT_RED, Colors.BOLD)
                print(error_msg)
                exit(1)
        
        maybe_clear_screen()
        
        # Nhập delay
        print("\n" + banner_line)
        print(banner_line)
        print(title)
        print(author)
        print(banner_line)
        print(banner_line)
        print(f"\n{Colors.colorize('🔧 Debug mode:', Colors.BRIGHT_BLUE)} {debug_status}")
        print(f"{Colors.colorize('📂 File JSON:', Colors.BRIGHT_GREEN)} {Colors.colorize(json_file, Colors.BRIGHT_WHITE)}")
        
        step3_title = Colors.colorize("\n📥 BƯỚC 3: Cài đặt delay", Colors.BRIGHT_CYAN, Colors.BOLD)
        delay_tip = Colors.colorize("   💡", Colors.CYAN) + " Delay giữa các request để tránh bị Facebook chặn"
        
        print(step3_title)
        print(delay_tip)
        
        delay_prompt = Colors.colorize("\n⏳ Nhập delay", Colors.BRIGHT_YELLOW) + " (giây, mặc định 2): "
        delay_input = input(delay_prompt).strip()
        
        try:
            delay = int(delay_input) if delay_input else 2
            if delay < 1:
                delay = 1
                warning_msg = Colors.colorize("   ⚠️  Delay tối thiểu là 1 giây, đã đặt về 1", Colors.BRIGHT_YELLOW)
                print(warning_msg)
        except ValueError:
            delay = 2
            warning_msg = Colors.colorize("   ⚠️  Delay không hợp lệ, sử dụng mặc định: 2 giây", Colors.BRIGHT_YELLOW)
            print(warning_msg)
        
        maybe_clear_screen()
        
        # Nhập verbose mode (gộp chung với debug: bật debug = bật verbose)
        print("\n" + banner_line)
        print(banner_line)
        print(title)
        print(author)
        print(banner_line)
        print(banner_line)
        print(f"\n{Colors.colorize('🔧 Debug mode:', Colors.BRIGHT_BLUE)} {debug_status}")
        print(f"{Colors.colorize('📂 File JSON:', Colors.BRIGHT_GREEN)} {Colors.colorize(json_file, Colors.BRIGHT_WHITE)}")
        print(f"{Colors.colorize('⏳ Delay:', Colors.BRIGHT_GREEN)} {Colors.colorize(f'{delay} giây', Colors.BRIGHT_WHITE)}")
        
        step4_title = Colors.colorize("\n📥 BƯỚC 4: Chế độ hiển thị", Colors.BRIGHT_CYAN, Colors.BOLD)
        verbose_tip1 = Colors.colorize("   💡 Verbose:", Colors.CYAN) + " Theo debug mode (bật debug = verbose, tắt debug = non-verbose)"
        verbose_tip2 = Colors.colorize("   💡 Non-verbose:", Colors.CYAN) + " Tự động khi debug TẮT (ít log hơn, gọn hơn)"
        
        print(step4_title)
        print(verbose_tip1)
        print(verbose_tip2)
        
        # Gán verbose theo debug_mode, không hỏi thêm
        verbose = debug_mode
        
        maybe_clear_screen()
        
        print("\n" + banner_line)
        print(banner_line)
        print(title)
        print(author)
        print(banner_line)
        print(banner_line)
        
        info_header = Colors.colorize("\n📋 THÔNG TIN:", Colors.BRIGHT_YELLOW, Colors.BOLD)
        info_line = Colors.colorize("="*80, Colors.BRIGHT_CYAN)
        
        print(info_header)
        safe_name3 = safe_console_text(user_info['name'])
        safe_uid3 = safe_console_text(user_info['uid'])
        print(f"   {Colors.colorize('👤 User:', Colors.BRIGHT_GREEN)} {Colors.colorize(safe_name3, Colors.BRIGHT_WHITE)} ({Colors.colorize('UID:', Colors.CYAN)} {Colors.colorize(safe_uid3, Colors.BRIGHT_WHITE)})")
        print(f"   {Colors.colorize('📂 File JSON:', Colors.BRIGHT_GREEN)} {Colors.colorize(json_file, Colors.BRIGHT_WHITE)}")
        print(f"   {Colors.colorize('⏳ Delay:', Colors.BRIGHT_GREEN)} {Colors.colorize(f'{delay} giây', Colors.BRIGHT_WHITE)}")
        print(f"   {Colors.colorize('🔍 Debug:', Colors.BRIGHT_GREEN)} {debug_status}")
        verbose_status = Colors.colorize("Có", Colors.BRIGHT_GREEN, Colors.BOLD) if verbose else Colors.colorize("Không", Colors.BRIGHT_RED, Colors.BOLD)
        print(f"   {Colors.colorize('🔍 Verbose:', Colors.BRIGHT_GREEN)} {verbose_status}")
        print(info_line)
        
        # Hỏi số luồng (đa luồng 5-10 luồng)
        step5_title = Colors.colorize("\n📥 BƯỚC 5: Số luồng xử lý song song", Colors.BRIGHT_CYAN, Colors.BOLD)
        thread_tip = Colors.colorize("   💡", Colors.CYAN) + " Nhiều luồng hơn = nhanh hơn nhưng dễ bị Facebook để ý hơn (gợi ý 5-10)"
        print(step5_title)
        print(thread_tip)
        threads_prompt = Colors.colorize("\n🧵 Nhập số luồng", Colors.BRIGHT_YELLOW) + " (1-10, mặc định 5): "
        threads_input = input(threads_prompt).strip()
        try:
            num_threads = int(threads_input) if threads_input else 5
        except ValueError:
            num_threads = 5
        if num_threads < 1:
            num_threads = 1
        if num_threads > 10:
            num_threads = 10
            warn_threads = Colors.colorize("   ⚠️ Tối đa 10 luồng, đã đặt về 10", Colors.BRIGHT_YELLOW)
            print(warn_threads)
        
        maybe_clear_screen()
        
        print("\n" + banner_line)
        print(banner_line)
        print(title)
        print(author)
        print(banner_line)
        print(banner_line)
        
        info_header = Colors.colorize("\n📋 THÔNG TIN:", Colors.BRIGHT_YELLOW, Colors.BOLD)
        info_line = Colors.colorize("="*80, Colors.BRIGHT_CYAN)
        
        print(info_header)
        safe_name4 = safe_console_text(user_info['name'])
        safe_uid4 = safe_console_text(user_info['uid'])
        print(f"   {Colors.colorize('👤 User:', Colors.BRIGHT_GREEN)} {Colors.colorize(safe_name4, Colors.BRIGHT_WHITE)} ({Colors.colorize('UID:', Colors.CYAN)} {Colors.colorize(safe_uid4, Colors.BRIGHT_WHITE)})")
        print(f"   {Colors.colorize('📂 File JSON:', Colors.BRIGHT_GREEN)} {Colors.colorize(json_file, Colors.BRIGHT_WHITE)}")
        print(f"   {Colors.colorize('⏳ Delay:', Colors.BRIGHT_GREEN)} {Colors.colorize(f'{delay} giây', Colors.BRIGHT_WHITE)}")
        print(f"   {Colors.colorize('🔍 Debug:', Colors.BRIGHT_GREEN)} {debug_status}")
        verbose_status = Colors.colorize("Có", Colors.BRIGHT_GREEN, Colors.BOLD) if verbose else Colors.colorize("Không", Colors.BRIGHT_RED, Colors.BOLD)
        print(f"   {Colors.colorize('🔍 Verbose:', Colors.BRIGHT_GREEN)} {verbose_status}")
        print(f"   {Colors.colorize('🧵 Số luồng:', Colors.BRIGHT_GREEN)} {Colors.colorize(str(num_threads), Colors.BRIGHT_WHITE)}")
        print(info_line)
        
        # Khởi tạo và chạy batch
        batch_tool = BatchUnfollowTool(
            cookie_string=cookie,
            json_file_path=json_file,
            delay_between_requests=delay,
            debug=debug_mode,
            verbose=verbose,
            num_threads=num_threads
        )
        
        # Truyền user_info vào để không cần lấy lại
        batch_tool.user_info = user_info
        batch_tool.run()
        
        print("\n✅ Hoàn tất!\n")

