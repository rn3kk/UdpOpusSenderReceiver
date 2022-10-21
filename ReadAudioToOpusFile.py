import wave
from threading import Thread

import pyaudio
import pyogg


class ReadAudioToOpusFile(Thread):
    __terminate = False

    def __init__(self):
        Thread.__init__(self)

    def run(self) -> None:
        p = pyaudio.PyAudio()
        stream_in = p.open(input_device_index=1,
                           format=pyaudio.paInt16,
                           channels=1,
                           rate=48000,
                           input=True,
                           frames_per_buffer=960)

        file_name = "test_opus.opus"
        # opus_file = pyogg.OpusFile("test_opus.opus")

        opus_buffered_encoder = pyogg.OpusBufferedEncoder()
        opus_buffered_encoder.set_application("audio")
        opus_buffered_encoder.set_sampling_frequency(48000)
        opus_buffered_encoder.set_channels(1)
        opus_buffered_encoder.set_frame_size(20)  # milliseconds

        f = open('opus_stream', 'wb')
        # endcode stream
        count = 0
        while count < 3:
            pcm = stream_in.read(960, exception_on_overflow=False)
            encoded_packets = opus_buffered_encoder.buffered_encode(
                memoryview(bytearray(pcm)),  # FIXME
                flush=(count == 2)
            )
            if encoded_packets.__len__() > 0:
                s = encoded_packets.pop(0)[0].tobytes()
                f.write(s)
            count += 1
        f.close()


        # save to ogg file
        # ogg_opus_writer = pyogg.OggOpusWriter(
        #     file_name,
        #     opus_buffered_encoder
        # )
        # count = 0
        # while count < 100:
        #     pcm = stream_in.read(960, exception_on_overflow=False)
        #     ogg_opus_writer.write(memoryview(bytearray(pcm)))
        #     count += 1
        #
        # ogg_opus_writer.close()

        print("END")



    def set_terminate(self):
        self.__terminate = True

if __name__ == '__main__':
    r = ReadAudioToOpusFile()
    r.start()

    r.join()