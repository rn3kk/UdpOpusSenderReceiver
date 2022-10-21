import socket
import time
from threading import Thread
from pyogg import OpusDecoder
import pyaudio as pyaudio

HOST = '0.0.0.0'


class UdpRtpServer(Thread):
    __port = 6992
    __terminate = False

    def __init__(self, port=6992):
        Thread.__init__(self)
        self.__port = port

    def __del__(self):
        print('~UdpRtpServer()')

    def set_terminate(self):
        print('set terminate True')
        self.__terminate = True

    def run(self):
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            print(p.get_device_info_by_index(i))

        stream_out = p.open(output_device_index=18,
                                   format=pyaudio.paInt16,
                                   channels=1,
                                   rate=48000,
                                   output=True,
                                   frames_per_buffer=960)

        print('UDP AudioServer is run')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = ('0.0.0.0', self.__port)
        server_socket.bind(addr)
        server_socket.settimeout(0.1)
        # server_socket.setblocking(False)
        print('UDPServer listen port ' + str(self.__port))
        count = 0
        opus_decoder = OpusDecoder()
        opus_decoder.set_channels(1)
        opus_decoder.set_sampling_frequency(48000)

        coutn = 0;
        f = open('opus.ogg', 'wb')
        while not self.__terminate:
            time.sleep(0.001)
            try:
                d = server_socket.recvfrom(256)
                print(d[0])
                mv = memoryview(d[0])
                pcm = opus_decoder.decode(bytearray(mv)).tobytes()
                stream_out.write(pcm)
                if coutn == 0:
                    f.write(mv)
                    coutn+=1
                    f.close()
                    exit(0)

            except socket.timeout:
                # print('udp read timeout')
                if self.__terminate:
                    break
                else:
                    continue
            except socket.error:
                print("Client Disconnected")
            except Exception as e:
                print(e)
        print('UDP AudioServer is end loop')



