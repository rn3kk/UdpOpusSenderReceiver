import signal

from UdpOpusReceiver import UdpRtpServer
from UdpOpusSender import UdpOpusSender


# udp = UdpRtpServer()
udp = UdpOpusSender()
udp.start()


def handler(signum, frame):
    print('set terminate is True')
    udp.set_terminate()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    udp.join()

