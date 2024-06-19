import sublist3r
import requests
import argparse
import dns.resolver

def get_status_code(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def get_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            return rdata.target.to_text()
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return "Domain does not exist"
    except dns.resolver.Timeout:
        return "Timeout while resolving"
    except Exception as e:
        return f"Error: {str(e)}"

def save_results_to_file(results, output_file):
    if output_file.endswith('.csv'):
        with open(output_file, 'w') as file:
            file.write("Subdomain,HTTP Status,HTTPS Status,CNAME\n")
            for subdomain, http_status, https_status, cname in results:
                file.write(f"{subdomain},{http_status},{https_status},{cname}\n")
    elif output_file.endswith('.txt'):
        with open(output_file, 'w') as file:
            for subdomain, http_status, https_status, cname in results:
                file.write(f"Subdomain: {subdomain}\n")
                file.write(f"HTTP Status Code: {http_status}\n")
                file.write(f"HTTPS Status Code: {https_status}\n")
                file.write(f"CNAME: {cname}\n")
                file.write("----------------------------------------\n")
    else:
        print("Unsupported file format. Please use .csv or .txt")

def main():
    parser = argparse.ArgumentParser(description="Enhanced Subdomain Enumerator Script by Whitehat94")
    parser.add_argument('domain', help="Base domain (e.g., example.com)")
    parser.add_argument('-o', '--output', help="Output file to save results (supports .csv and .txt)", required=False)
    args = parser.parse_args()

    base_domain = args.domain
    output_file = args.output

    print("    ***************************************")
    print("    *         Enhanced Subdomain           *")
    print("    *          Enumerator Script           *")
    print("    *           by Whitehat94              *")
    print("    ***************************************\n")

    print(f"Enter the base domain (e.g., example.com): {base_domain}\n")
    print(f"Enumerating subdomains for {base_domain}...\n")

    subdomains = sublist3r.main(base_domain, 40, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)

    if not subdomains:
        print("No subdomains found.")
        return

    results = []

    print("Subdomains found:\n")
    for subdomain in subdomains:
        http_status = get_status_code(f"http://{subdomain}")
        https_status = get_status_code(f"https://{subdomain}")
        cname = get_cname(subdomain)
        results.append((subdomain, http_status, https_status, cname))

        print(f"Subdomain: {subdomain}")
        print(f"HTTP Status Code: {http_status}")
        print(f"HTTPS Status Code: {https_status}")
        print(f"CNAME: {cname}")
        print("----------------------------------------\n")

    if output_file:
        save_results_to_file(results, output_file)
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
