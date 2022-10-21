import socket
from threading import Thread

import pyaudio
from pyogg import OpusEncoder


class UdpOpusSender(Thread):
    __port = 6992
    __terminate = False

    def __init__(self):
        Thread.__init__(self)

    def run(self) -> None:
        opus_encoder = OpusEncoder()
        opus_encoder.set_channels(1)
        opus_encoder.set_application('audio')
        opus_encoder.set_sampling_frequency(int(48000))
        opus_encoder.set_max_bytes_per_frame(60)


        p = pyaudio.PyAudio()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        stream_in = p.open(input_device_index=1,
                                  format=pyaudio.paInt16,
                                  channels=1,
                                  rate=48000,
                                  input=True,
                                  frames_per_buffer=960)
        adrs = ("192.168.0.215", 6992)
        f = open('opus.ogg', 'rb')
        b = f.read()
        # s.sendto(b, adrs)
        # exit(0)
        while not self.__terminate:
            pcm = stream_in.read(960, exception_on_overflow=False)
            opus_bytes = opus_encoder.encode(pcm)
            s.sendto(opus_bytes, adrs)
            print(opus_bytes.__len__(), opus_bytes.tobytes())

    def set_terminate(self):
        self.__terminate = True
