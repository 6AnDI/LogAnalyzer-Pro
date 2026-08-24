import re
from collections import defaultdict

def analyze_auth_logs(file_path, threshold=3):
    failed_attempts = defaultdict(int)
    # Regex pattern to match failed SSH login attempts and extract the IP address
    fail_pattern = re.compile(r"Failed password for.*from\s+([\d\.]+)")
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = fail_pattern.search(line)
                if match:
                    ip_address = match.group(1)
                    failed_attempts[ip_address] += 1
                    
        # Filter IPs that exceed the brute-force threshold
        flagged_threats = []
        for ip, count in failed_attempts.items():
            if count >= threshold:
                flagged_threats.append({"ip": ip, "failures": count})
                
        return flagged_threats
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []