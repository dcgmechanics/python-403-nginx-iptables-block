import re
import subprocess

# Function to read nginx access log file and extract IP addresses with 403 response code
def extract_403_ips(log_file_path):
    ip_regex = r'(\d+\.\d+\.\d+\.\d+)'
    response_code = ' 403 '

    # Open the log file and extract IP addresses with 403 response code
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.readlines()
            filtered_ips = set()
            for line in log_content:
                if response_code in line:
                    match = re.search(ip_regex, line)
                    if match:
                        filtered_ips.add(match.group())
        return filtered_ips
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return set()

# Function to add IP addresses to IP Tables block list
def add_ips_to_iptables(ip_addresses):
    for ip_address in ip_addresses:
        subprocess.run(['iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'])
        print(f"Blocked IP Address: {ip_address}")

if __name__ == "__main__":
    nginx_access_log_file = "/var/log/nginx/access.log"  # Change this to your nginx access log file path
    ip_addresses_403 = extract_403_ips(nginx_access_log_file)

    if ip_addresses_403:
        add_ips_to_iptables(ip_addresses_403)
    else:
        print("No IP addresses with 403 response code found in the nginx access log.")
