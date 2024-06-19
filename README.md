# Enhanced Subdomain Enumerator

Enhanced Subdomain Enumerator is a Python script that allows you to enumerate subdomains for a given domain and retrieve their HTTP status codes, HTTPS status codes, and CNAME records. It uses the Sublist3r tool for subdomain enumeration and makes HTTP requests to each subdomain to retrieve status codes. Additionally, it resolves CNAME records for each subdomain.

## Features
- Enumerate subdomains for a given domain
- Retrieve HTTP status codes and HTTPS status codes for each subdomain
- Resolve CNAME records for each subdomain
- Save results to a CSV or TXT file

## Installation
1. Clone this repository:
   git clone https://github.com/whitehat1994/Enhanced_Sublister.git

2. cd Enhanced_Sublister
3. pip install -r requirements.txt

## Usage
python enhanced_sublister.py <domain> [-o OUTPUT]
    * <domain>: Base domain (e.g., example.com)
    * -o, --output OUTPUT: Output file to save results (optional)

## Example:
python enhanced_sublister.py example.com -o results.csv

# Output Format
The script outputs the subdomain enumeration results to the console and optionally saves them to a file. If saved to a file, the results are stored in either CSV or TXT format based on the file extension provided.

## CSV
Subdomain,HTTP Status,HTTPS Status,CNAME
subdomain1.example.com,200,200,example.com

## Text
Subdomain: subdomain1.example.com
HTTP Status Code: 200
HTTPS Status Code: 200
CNAME: example.com
----------------------------------------
