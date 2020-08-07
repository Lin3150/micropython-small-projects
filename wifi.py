# 在这里写上你的代码 :-)
import network


def connect_network():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network")
        wlan.connect("Redmi K30 Pro", "ui456987")
        while not wlan.isconnected():
            pass
    print("network config", wlan.ifconfig())
    print("connected")


def main():
    connect_network()


if __name__ == "__main__":
    main()
