#!/usr/bin/env python3
"""
POWER SCRIPT "Atankinsh" – Suite Pentest para Termux en Python
Creado por Felipe Monroy  ✦  Empresa: TOKINSH
Adaptado para pantallas pequeñas (móvil/tablet)
Licencia: Uso educacional / auditorías autorizadas
"""
import os
import sys
import subprocess
import time
import getpass
from pathlib import Path

# ANSI Colors
RED    = '\033[91m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
BLUE   = '\033[94m'
NC     = '\033[0m'

# Paths
HOME           = Path.home()
LOGDIR         = HOME / 'Tokinsh-logs'; LOGDIR.mkdir(exist_ok=True)
LOGFILE        = LOGDIR / f"{time.strftime('%F')}.log"
WORDDIR        = HOME / 'wordlists'; WORDDIR.mkdir(exist_ok=True)
M5PORT_DEFAULT = '/dev/ttyACM0'

# Stub for PC compatibility
def check_termux():
    return

# Utilities
def slow_print(text, delay=0.01):
    for c in text:
        sys.stdout.write(c); sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write('\n')

def progress_bar(duration=2.0, length=20):
    interval = duration / length
    for i in range(length + 1):
        bar = '█' * i + ' ' * (length - i)
        pct = int(i * 100 / length)
        sys.stdout.write(f"\r{RED}[{bar}]{NC} {pct}%")
        sys.stdout.flush(); time.sleep(interval)
    sys.stdout.write("\r" + " " * (length + 8) + "\r")

def pause():
    input('\n↵ Enter para continuar…')

def log_action(action: str):
    with open(LOGFILE, 'a') as f:
        f.write(f"[{time.strftime('%F %T')}] {action}\n")

def confirm_perm() -> bool:
    ans = input(f"{YELLOW}⚠️ Solo con permiso EXPRESO. ¿Continuar? (S/N) ➤ {NC}")
    return ans.strip().lower().startswith('s')

def ensure_wordlist():
    wl = WORDDIR / 'rockyou.txt'
    if wl.exists():
        return wl
    ans = input("No se encontró rockyou.txt. ¿Descargar (~14 MB)? (S/N) ➤ ")
    if not ans.strip().lower().startswith('s'):
        return None
    url = 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'
    subprocess.run(['curl', '-L', '-o', str(wl), url], check=True)
    slow_print(f"Descargado en {wl}")
    return wl

# Install dependencies (essentials only)
def install_deps():
    slow_print("\n🔄 Actualizando…")
    subprocess.run(['pkg', 'update', '-y'], check=False)
    slow_print("🛠️ Instalando paquetes esenciales…")
    essentials = ['curl', 'git', 'python', 'perl', 'ruby']
    for pkg in essentials:
        slow_print(f"Instalando {pkg}…")
        subprocess.run(['pkg', 'install', '-y', pkg], check=False)
    slow_print("✅ Esenciales instalados.")
    slow_print("⚙️ Para herramientas avanzadas: pkg install nmap nikto gobuster dnsenum mtr sqlmap metasploit hydra john hashcat exploitdb esptool rshell screen")
    slow_print("💎 Para wpscan: gem install wpscan --user-install")
    slow_print("🔗 Más info: https://wiki.termux.com/wiki/Package_Management")
    pause()

# Pentest functions
def nmap_scan():
    if not confirm_perm(): return
    tgt = input("Objetivo ➤ ")
    log_action(f"Nmap -> {tgt}")
    subprocess.run(['nmap', '-sV', '-T4', tgt])
    pause()

def nikto_scan():
    if not confirm_perm(): return
    url = input("URL ➤ ")
    log_action(f"Nikto -> {url}")
    subprocess.run(['nikto', '-h', url])
    pause()

def sqlmap_auto():
    if not confirm_perm(): return
    u = input("URL vuln ➤ ")
    log_action(f"SQLMap -> {u}")
    subprocess.run(['sqlmap', '-u', u, '--batch', '--banner'])
    pause()

def metasploit_launch():
    if not confirm_perm(): return
    log_action("Metasploit")
    subprocess.run(['msfconsole', '-q'])

def hydra_brute_services():
    if not confirm_perm(): return
    ip = input("IP ➤ ")
    srv = input("Servicio (ssh/ftp/…) ➤ ")
    users = input("Lista usuarios ➤ ")
    pwds = input("Lista passwords ➤ ")
    log_action(f"HydraSvc -> {srv} {ip}")
    subprocess.run(['hydra', '-L', users, '-P', pwds, ip, srv])
    pause()

def hydra_web_form():
    if not confirm_perm(): return
    wl = ensure_wordlist()
    dom = input("Dominio ➤ ")
    ruta = input("Ruta login ➤ ")
    ufield = input("Campo usuario ➤ ")
    pfield = input("Campo pass ➤ ")
    ferr = input("Error text ➤ ")
    users = str(WORDDIR / 'users.txt')
    pwds = str(wl) if wl else ''
    cmd = ['hydra', '-L', users, '-P', pwds, dom, 'http-post-form', f"{ruta}:{ufield}=^USER^&{pfield}=^PASS^:F={ferr}"]
    slow_print(f"Ejecutando: {' '.join(cmd)}")
    log_action(f"HydraForm -> {dom}{ruta}")
    subprocess.run(cmd)
    pause()

def dirb_scan():
    if not confirm_perm(): return
    url = input("URL ➤ ")
    log_action(f"Dirb -> {url}")
    subprocess.run(['dirb', url])
    pause()

def gobuster_dir():
    if not confirm_perm(): return
    url = input("URL ➤ ")
    log_action(f"Gobuster -> {url}")
    subprocess.run(['gobuster', 'dir', '-u', url, '-w', '/usr/share/wordlists/dirb/common.txt'])
    pause()

def theharvester_osint():
    dom = input("Dominio ➤ ")
    log_action(f"Harvester -> {dom}")
    subprocess.run(['theHarvester', '-d', dom, '-b', 'all', '-f', str(LOGDIR / f"{dom}_harv.html")])
    pause()

def whois_lookup():
    d = input("Dom/IP ➤ ")
    log_action(f"Whois -> {d}")
    subprocess.run(['whois', d])
    pause()

def dns_enum():
    d = input("Dom ➤ ")
    log_action(f"DNSenum -> {d}")
    subprocess.run(['dnsenum', d])
    pause()

def tracer_mtr():
    h = input("Host ➤ ")
    log_action(f"MTR -> {h}")
    subprocess.run(['mtr', '-rwzbc', '5', h])
    pause()

def john_crack():
    wl = ensure_wordlist()
    f = input("Hashes file ➤ ")
    log_action(f"John -> {f}")
    subprocess.run(['john', f])
    pause()

def hashcat_crack():
    wl = ensure_wordlist()
    f = input("Hashes ➤ ")
    w = input("Wordlist ➤ ") or str(wl)
    log_action(f"Hashcat -> {f}")
    subprocess.run(['hashcat', '-a', '0', f, w])
    pause()

def aircrack_audit():
    if os.geteuid() != 0:
        slow_print("Necesitas root para Aircrack.")
        pause()
        return
    log_action("Aircrack")
    subprocess.run(['airmon-ng', 'start', 'wlan0'])
    c = input("Canal ➤ ")
    subprocess.run(['airodump-ng', '--channel', c, 'wlan0mon'])
    pause()

def http_requests():
    if not confirm_perm(): return
    url = input("URL ➤ ")
    num = int(input("N° peticiones ➤ "))
    log_action(f"HTTP flood {num} -> {url}")
    procs = []
    for i in range(1, num+1):
        procs.append(subprocess.Popen(['curl', '-s', '-o', '/dev/null', url]))
        sys.stdout.write(f"\r{i}/{num}"); sys.stdout.flush()
    for p in procs: p.wait()
    slow_print("Completo.")
    pause()

def searchsploit_find():
    k = input("Exploit search ➤ ")
    log_action(f"searchsploit {k}")
    subprocess.run(['searchsploit', k])
    pause()

# M5Stack helpers
def m5_install():
    slow_print("\nInstalando M5Stack…")
    subprocess.run(['pkg', 'install', '-y', 'esptool', 'pyserial'], check=False)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'mpremote', 'adafruit-ampy'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    slow_print("✅ Listo.")
    pause()

def m5_flash_micropython():
    if not confirm_perm(): return
    p = input(f"Port [{M5PORT_DEFAULT}] ➤ ") or M5PORT_DEFAULT
    slow_print("Flasheando firmware…")
    fw = HOME / 'micropython_m5core2.bin'
    subprocess.run(['curl', '-L', '-o', str(fw), 'https://static-cdn.m5stack.com/resource/firmware/core2/CORE2_20230421-v1.20.1.bin'], check=True)
    log_action(f"M5Flash -> {p}")
    subprocess.run(['esptool.py', '--chip', 'esp32', '--port', p, 'erase_flash'], check=True)
    subprocess.run(['esptool.py', '--chip', 'esp32', '--port', p, '--baud', '460800', 'write_flash', '-z', '0x1000', str(fw)], check=True)
    slow_print("✅ Flasheado.")
    pause()

def m5_upload_script():
    if not confirm_perm(): return
    p = input(f"Port [{M5PORT_DEFAULT}] ➤ ") or M5PORT_DEFAULT
    f = input("Script .py ➤ ")
    if not os.path.isfile(f): slow_print("No existe."); pause(); return
    log_action(f"M5Upload -> {f} on {p}")
    subprocess.run(['mpremote', 'connect', p, 'fs', 'put', f, ':main.py'], check=True)
    slow_print("✅ Uploaded.")
    subprocess.run(['mpremote', 'connect', p, 'reset'], check=True)
    pause()

def m5_serial():
    p = input(f"Port [{M5PORT_DEFAULT}] ➤ ") or M5PORT_DEFAULT
    slow_print("Serial mode (Ctrl-a a to exit)…")
    subprocess.run(['screen', p, '115200'], check=False)

# About us
def show_about():
    os.system('cls' if os.name=='nt' else 'clear')
    slow_print(f"{BLUE}Sobre nosotros{NC}\n")
    slow_print("• Felipe Monroy (felipehiy)")
    slow_print("• Fundador de TOKINSH")
    slow_print("• Suite Atankinsh v1.0 móvil")
    slow_print("• No responsables de usos ilegales")
    slow_print("• WhatsApp +31 6 19386274")
    pause()

# Welcome & menus
def welcome_screen():
    os.system('cls' if os.name=='nt' else 'clear')
    slow_print(f"{YELLOW}ATANKINSH v1.0 – TOKINSH{NC}\n")
    ascii_art = r"""
 .--------. .--------. .--------.
|  TOKIN  | |   v1   | |  ATANK |
 '--------' '--------' '--------'
"""
    print(RED + ascii_art + NC)
    slow_print("Cargando Atankinsh...")
    progress_bar()
    slow_print(f"{GREEN}Empresa: TOKINSH{NC}")
    slow_print(f"{YELLOW}⚠️ Solo con permiso expreso{NC}\n")
    if not input("TyC? (S/N) ➤ ").strip().lower().startswith('s'):
        sys.exit(0)

def login_menu():
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        slow_print(f"{GREEN}Atankinsh — Login{NC}\n")
        print("1) Iniciar sesión\n2) Instalar deps\n3) Sobre\n4) Salir")
        o = input("➤ ")
        if o == '1':
            c = getpass.getpass("Código ➤ ")
            if c == '01020304': slow_print("OK"); time.sleep(0.5); return
            slow_print("Mal");
        elif o == '2': install_deps()
        elif o == '3': show_about()
        elif o == '4': sys.exit(0)

def main_menu():
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        slow_print(f"{BLUE}Atankinsh Suite{NC}\n")
        print("1) Nmap 2) Nikto 3) SQLMap 4) MSF 5) HydraSvc 6) HydraWeb 7) Dirb 8) Gobuster 9) John 10) Hashcat 11) WPScan 12) Whois 13) DNSenum 14) MTR 15) Harv 16) HTTP 17) sploit 18) Air 19) M5Env 20) M5Flash 21) M5Up 22) M5Ser 0) Exit")
        c = input("➤ ")
        actions = {
            '1': nmap_scan, '2': nikto_scan, '3': sqlmap_auto, '4': metasploit_launch,
            '5': hydra_brute_services, '6': hydra_web_form, '7': dirb_scan, '8': gobuster_dir,
            '9': john_crack, '10': hashcat_crack, '11': lambda: (slow_print("WPScan pte."), pause()),
            '12': whois_lookup, '13': dns_enum, '14': tracer_mtr, '15': theharvester_osint,
            '16': http_requests, '17': searchsploit_find, '18': aircrack_audit,
            '19': m5_install, '20': m5_flash_micropython, '21': m5_upload_script, '22': m5_serial,
            '0': lambda: sys.exit(0)
        }
        fn = actions.get(c)
        if fn:
            fn()

if __name__ == '__main__':
    check_termux()
    welcome_screen()
    login_menu()
    main_menu()
