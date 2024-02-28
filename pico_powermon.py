import os
import time
import wifi
import ipaddress
import socketpool
import microcontroller
import board
import analogio
import adafruit_ntp

vsense = analogio.AnalogIn(board.A2)
def get_voltage():
    return (vsense.value * 3.3 * 6.025) / 65536 # 6.025 is the voltage divider ratio

#  IP address of the destination for our reports
relaypi_addr = "192.168.2.29"
relaypi = ipaddress.IPv4Address(relaypi_addr)
udpport = 7312

#  use a static IP address configuration
ipv4 = ipaddress.IPv4Address("192.168.2.30")
netmask = ipaddress.IPv4Address("255.255.255.0")
gateway = ipaddress.IPv4Address("192.168.2.1")
wifi.radio.set_ipv4_address(ipv4=ipv4, netmask=netmask, gateway=gateway)

#  connect to SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("My IP address:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)   # i.e., UDP
ntp = adafruit_ntp.NTP(pool, tz_offset=0)

while (get_voltage() < 11.5):
    print(f"Voltage low: {get_voltage():.1f}")
    time.sleep(1)

powerup_time = time.mktime(ntp.datetime)
print(f"Powered up at {powerup_time}")

while True:
    try:
        # literally ping the relaypi
        pingtime = wifi.radio.ping(relaypi)
        if pingtime:
            print("Ping time to relaypi = %f ms" % (pingtime*1000))
        else:
            print("Failed to ping relaypi in 0.5 seconds")
        # send a datagram to the relaypi
        udp_message = bytes(f'PowerMon GH_Rigrunner {powerup_time} {get_voltage():.1f}\n', "utf-8")
        print(f"sending {udp_message}")
        sock.sendto(udp_message, (relaypi_addr,udpport))

        time.sleep(1)
    # pylint: disable=broad-except
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
