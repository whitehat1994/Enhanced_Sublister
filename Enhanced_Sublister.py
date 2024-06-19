import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the specific warning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

import argparse
import sublist3r
import requests
import dns.resolver
import os
import csv

def get_status_code(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException:
        return "Error"

def get_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            return rdata.target.to_text()
    except dns.resolver.NXDOMAIN:
        return "NXDOMAIN"
    except dns.resolver.NoAnswer:
        return "No CNAME record"
    except Exception:
        return "Error"

def main():
    parser = argparse.ArgumentParser(description='Enhanced Subdomain Enumerator Script by Whitehat94')
    parser.add_argument('domain', help='Base domain (e.g., example.com)')
    parser.add_argument('-o', '--output', help='Output file to save results (supports .csv and .txt)', default=None)
    args = parser.parse_args()

    base_domain = args.domain
    output_file = args.output

    print("    ***************************************")
    print("    *         Enhanced Subdomain           *")
    print("    *          Enumerator Script           *")
    print("    *           by Whitehat94              *")
    print("    ***************************************")
    print()
    print(f"Enumerating subdomains for {base_domain}...")
    print()

    # Pass 'None' as the savefile parameter to sublist3r.main
    subdomains = sublist3r.main(base_domain, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)

    if not subdomains:
        print(f"No subdomains found for {base_domain}")
        return

    results = []
    for subdomain in subdomains:
        http_status = get_status_code(f'http://{subdomain}')
        https_status = get_status_code(f'https://{subdomain}')
        cname = get_cname(subdomain)
        
        results.append({
            'Subdomain': subdomain,
            'HTTP Status Code': http_status,
            'HTTPS Status Code': https_status,
            'CNAME': cname
        })
        
        print(f"Subdomain: {subdomain}")
        print(f"HTTP Status Code: {http_status}")
        print(f"HTTPS Status Code: {https_status}")
        print(f"CNAME: {cname}")
        print("----------------------------------------")

    if output_file:
        file_ext = os.path.splitext(output_file)[1]
        if file_ext == '.csv':
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['Subdomain', 'HTTP Status Code', 'HTTPS Status Code', 'CNAME']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    writer.writerow(result)
        elif file_ext == '.txt':
            with open(output_file, 'w') as txtfile:
                for result in results:
                    txtfile.write(f"Subdomain: {result['Subdomain']}\n")
                    txtfile.write(f"HTTP Status Code: {result['HTTP Status Code']}\n")
                    txtfile.write(f"HTTPS Status Code: {result['HTTPS Status Code']}\n")
                    txtfile.write(f"CNAME: {result['CNAME']}\n")
                    txtfile.write("----------------------------------------\n")
        else:
            print(f"Unsupported file format: {file_ext}")

if __name__ == "__main__":
    main()
