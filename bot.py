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

# Daftar proxy dengan autentikasi (username:password)
PROXIES = [
    "198.23.239.134:6540:synthinks:boot2784",
    "207.244.217.165:6712:synthinks:boot2784",
    "107.172.163.27:6543:synthinks:boot2784",
    "64.137.42.112:5157:synthinks:boot2784",
    "173.211.0.148:6641:synthinks:boot2784",
    "161.123.152.115:6360:synthinks:boot2784",
    "23.94.138.75:6349:synthinks:boot2784",
    "154.36.110.199:6853:synthinks:boot2784",
    "173.0.9.70:5653:synthinks:boot2784",
    "173.0.9.209:5792:synthinks:boot2784"
]

# Fungsi untuk mendapatkan proxy secara acak
def get_random_proxy():
    proxy = random.choice(PROXIES)
    ip, port, user, password = proxy.split(":")
    return {
        "http": f"http://{user}:{password}@{ip}:{port}",
        "https": f"http://{user}:{password}@{ip}:{port}"
    }

# Fungsi untuk menampilkan banner
def display_banner():
    banner = f"""
    {Fore.GREEN} █████╗ {Fore.YELLOW}██████╗ {Fore.RED}███████╗{Fore.MAGENTA}███╗   ██╗{Fore.BLUE} █████╗     
    {Fore.GREEN}██╔══██╗{Fore.YELLOW}██╔══██╗{Fore.RED}██╔════╝{Fore.MAGENTA}████╗  ██║{Fore.BLUE}██╔══██╗    
    {Fore.GREEN}███████║{Fore.YELLOW}██████╔╝{Fore.RED}█████╗  {Fore.MAGENTA}██╔██╗ ██║{Fore.BLUE}███████║    
    {Fore.GREEN}██╔══██║{Fore.YELLOW}██╔══██╗{Fore.RED}██╔══╝  {Fore.MAGENTA}██║╚██╗██║{Fore.BLUE}██╔══██║    
    {Fore.GREEN}██║  ██║{Fore.YELLOW}██║  ██║{Fore.RED}███████╗{Fore.MAGENTA}██║ ╚████║{Fore.BLUE}██║  ██║    
    {Fore.GREEN}╚═╝  ╚═╝{Fore.YELLOW}╚═╝  ╚═╝{Fore.RED}╚══════╝{Fore.MAGENTA}╚═╝  ╚═══╝{Fore.BLUE}╚═╝  ╚═╝    
    —————————————————————————————————————————————————————————————————
    {Fore.CYAN}Channel : {Fore.WHITE}t.me/ugdairdrop
    """
    print(banner)

# Fungsi untuk membuat wallet baru
def generate_wallet():
    w3 = Web3()
    account = w3.eth.account.create()
    return account.address, account._private_key.hex()

# Fungsi untuk mengirim request dengan proxy
def send_join_request(wallet_address, referral_code):
    ua = UserAgent()
    url = "https://quest-api.arenavs.com/api/v1/users/initialize"
    payload = {"walletAddress": wallet_address, "referralCode": referral_code}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua.random
    }
    proxy = get_random_proxy()

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, proxies=proxy, timeout=20)
        return response
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}  ✗ Request error: {e}")
        return None

# Fungsi untuk menyimpan wallet ke file JSON
def save_wallet(wallet_data):
    try:
        with open("wallets.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(wallet_data)

    with open("wallets.json", "w") as file:
        json.dump(data, file, indent=4)
    print(f"{Fore.GREEN}Wallet berhasil disimpan di wallets.json")

# Main program
if __name__ == "__main__":
    display_banner()
    
    referral_code = input(f"{Fore.YELLOW}▶ Masukkan referral code: {Style.RESET_ALL}").strip()
    
    try:
        num_accounts = int(input(f"{Fore.YELLOW}⨽ Masukkan jumlah akun yang ingin dibuat: {Style.RESET_ALL}"))
        if num_accounts <= 0:
            raise ValueError("Jumlah akun harus lebih besar dari 0.")
    except ValueError as e:
        print(f"{Fore.RED}Input tidak valid: {e}")
        exit(1)
    
    for i in range(num_accounts):
        wallet_address, private_key = generate_wallet()

        time.sleep(random.uniform(2, 5))  # Delay acak sebelum request

        join_response = send_join_request(wallet_address, referral_code)

        if join_response and join_response.status_code in [200, 201]:
            join_data = join_response.json()
            print(f"{Fore.CYAN}Akun ke-{i + 1}: Berhasil bergabung. Wallet: {wallet_address[:12]}...")

            wallet_data = {
                "wallet_address": wallet_address,
                "private_key": private_key,
                "referral_code": referral_code
            }
            save_wallet(wallet_data)
        else:
            print(f"{Fore.RED}Akun ke-{i + 1}: Gagal bergabung. Response: {join_response.text if join_response else 'No Response'}")
        
        time.sleep(random.uniform(3, 7))  # Delay antar akun untuk menghindari deteksi bot

