#It is used to copy the mac address of a random one of the connected devices on the open network.

from scapy.all import ARP, Ether, srp
import random
import optparse
import subprocess

def get_random_mac(target_ip):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)
    ans, unans = srp(pkt, timeout=3, verbose=0)


    available_macs = []
    for result in ans:
        pair = result[1]
        mac = pair.sprintf("%Ether.src%")
        ip = pair.sprintf("%ARP.psrc%")
        if not ip.endswith(".1"):
            available_macs.append(mac)

    if available_macs:
        return random.choice(available_macs)
    else:
        return None

parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Arayüzü belirtin")
parser.add_option("-r", "--ipaddress", dest="target_ip", help="Hedef IP adresini girin")

options, args = parser.parse_args()
interface = options.interface
target_ip = options.target_ip


prev_mac = subprocess.check_output(["ifconfig", interface]).decode().split("ether ")[1].split(" ")[0]

random_mac = get_random_mac(target_ip)
if random_mac:
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", random_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("Önceki MAC adresi:", prev_mac)
    print("Yeni MAC adresi:", random_mac)
else:
    print("Uygun MAC adresi bulunamadı.")

