import json
import requests
from web3 import Web3
import time
import random
import threading
from colorama import Fore, Style, init
from fake_useragent import UserAgent

# Inisialisasi colorama
init(autoreset=True)

# Fungsi untuk animasi spinner
def spinner_animation():
    spinner = ['|', '/', '-', '\\']
    i = 0
    while not getattr(threading.current_thread(), "stop", False):
        print(f"\r{Fore.CYAN}{spinner[i % len(spinner)]} {Style.RESET_ALL}Sedang memproses...", end="")
        i += 1
        time.sleep(0.1)

# Fungsi untuk menampilkan banner
def display_banner():
    banner = f"""
    {Fore.GREEN} █████╗ {Fore.YELLOW}██████╗ {Fore.RED}███████╗{Fore.MAGENTA}███╗   ██╗{Fore.BLUE} █████╗     {Fore.WHITE}██╗   ██╗███████╗
    {Fore.GREEN}██╔══██╗{Fore.YELLOW}██╔══██╗{Fore.RED}██╔════╝{Fore.MAGENTA}████╗  ██║{Fore.BLUE}██╔══██╗    {Fore.WHITE}██║   ██║██╔════╝
    {Fore.GREEN}███████║{Fore.YELLOW}██████╔╝{Fore.RED}█████╗  {Fore.MAGENTA}██╔██╗ ██║{Fore.BLUE}███████║    {Fore.WHITE}██║   ██║███████╗
    {Fore.GREEN}██╔══██║{Fore.YELLOW}██╔══██╗{Fore.RED}██╔══╝  {Fore.MAGENTA}██║╚██╗██║{Fore.BLUE}██╔══██║    {Fore.WHITE}╚██╗ ██╔╝╚════██║
    {Fore.GREEN}██║  ██║{Fore.YELLOW}██║  ██║{Fore.RED}███████╗{Fore.MAGENTA}██║ ╚████║{Fore.BLUE}██║  ██║     {Fore.WHITE}╚████╔╝ ███████║
    {Fore.GREEN}╚═╝  ╚═╝{Fore.YELLOW}╚═╝  ╚═╝{Fore.RED}╚══════╝{Fore.MAGENTA}╚═╝  ╚═══╝{Fore.BLUE}╚═╝  ╚═╝      {Fore.WHITE}╚═══╝  ╚══════╝
    —————————————————————————————————————————————————————————————————
    {Fore.CYAN}Channel : {Fore.WHITE}t.me/ugdairdrop
    {Fore.MAGENTA}Jangan lupa bergabung di channel kami untuk update terbaru! 🚀
    """
    print(banner)

# Fungsi untuk menghasilkan wallet address baru menggunakan web3
def generate_wallet():
    w3 = Web3()
    account = w3.eth.account.create()
    return account.address, account._private_key.hex()

# Fungsi untuk inisialisasi user dengan fake user-agent
def send_join_request(wallet_address, referral_code):
    ua = UserAgent()
    url = "https://quest-api.arenavs.com/api/v1/users/initialize"
    payload = {"walletAddress": wallet_address, "referralCode": referral_code}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua.random  # Menambahkan fake user-agent
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response

# Fungsi untuk menyelesaikan tugas dengan fake user-agent
def complete_task(task_id, user_id, token):
    ua = UserAgent()
    url = f"https://quest-api.arenavs.com/api/v1/tasks/{task_id}/complete/{user_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": ua.random  # Menambahkan fake user-agent
    }
    response = requests.post(url, headers=headers)
    return response

# Fungsi untuk memeriksa status penyelesaian tugas dengan fake user-agent
def check_completed_tasks(wallet_address, token):
    ua = UserAgent()
    url = f"https://quest-api.arenavs.com/api/v1/users/{wallet_address}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": ua.random  # Menambahkan fake user-agent
    }
    response = requests.get(url, headers=headers)
    return response

# Main program
if __name__ == "__main__":
    # Tampilkan banner
    display_banner()
    
    # Input referral code secara manual
    referral_code = input(f"{Fore.YELLOW}▶ Masukkan referral code: {Style.RESET_ALL}").strip()
    
    # Input jumlah akun yang ingin dibuat
    try:
        num_accounts = int(input(f"{Fore.YELLOW}⨽ Masukkan jumlah akun yang ingin dibuat: {Style.RESET_ALL}"))
        if num_accounts <= 0:
            raise ValueError(f"{Fore.RED}Jumlah akun harus lebih besar dari 0.")
    except ValueError as e:
        print(f"{Fore.RED}Input tidak valid: {e}")
        exit(1)
    
    for i in range(num_accounts):
        # Generate wallet address baru
        wallet_address, private_key = generate_wallet()
        
        # Tampilkan spinner selama proses berlangsung
        spinner_thread = threading.Thread(target=spinner_animation)
        spinner_thread.start()
        
        # Delay acak sebelum pembuatan akun
        time.sleep(random.uniform(2, 5))
        
        # Kirim request untuk inisialisasi user
        join_response = send_join_request(wallet_address, referral_code)
        
        # Hentikan spinner
        spinner_thread.stop = True
        spinner_thread.join()
        print("\r", end="")  # Bersihkan spinner
        
        if join_response.status_code not in [200, 201]:
            print(f"{Fore.RED}Akun ke-{i + 1}: Gagal bergabung.")
            continue
        
        # Ekstrak data dari respons
        join_data = join_response.json()
        token = join_data.get("token")
        user_id = join_data["user"]["id"]
        
        print(f"{Fore.CYAN}Akun ke-{i + 1}: Berhasil bergabung. Wallet: {wallet_address[:12]}...")
        
        # Loop untuk menyelesaikan semua 4 tugas
        for task_id in range(1, 5):
            # Delay acak untuk menghindari deteksi bot
            time.sleep(random.uniform(2, 5))  # Delay antara 2-5 detik
            
            # Kirim request untuk menyelesaikan tugas
            task_response = complete_task(task_id, user_id, token)
            if task_response.status_code in [200, 201]:
                print(f"{Fore.GREEN}  ✓ Tugas {task_id}: Selesai.")
            else:
                print(f"{Fore.RED}  ✗ Tugas {task_id}: Gagal.")
        
        # Cek status penyelesaian tugas
        time.sleep(random.uniform(2, 5))  # Delay sebelum pengecekan
        check_response = check_completed_tasks(wallet_address, token)
        if check_response.status_code == 200:
            completed_tasks = check_response.json().get("completedTasks", [])
            print(f"{Fore.YELLOW}  ⇌ Total tugas selesai: {len(completed_tasks)}")
        else:
            print(f"{Fore.RED}  ✗ Gagal memeriksa tugas.")