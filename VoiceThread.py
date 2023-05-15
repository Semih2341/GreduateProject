import threading
import VoiceDetection as vd



class VoiceThread(threading.Thread):
    def __init__(self, rightVoice, leftVoice, holdVoice, dropVoice, doubleVoice):
        threading.Thread.__init__(self)
        self.stop_event_voice = threading.Event()
        self.voiceInstance = vd.VoiceDetection(rightVoice, leftVoice, holdVoice, dropVoice, doubleVoice)


    def run(self):
        try:
            while not self.stop_event_voice.set():
                self.voiceInstance.start()

            self.voiceInstance.stop()
        except:
            print("hata")
        finally:
            self.voiceInstance.stop()

    def stop(self):
        self.stop_event_voice.set()
        # self.voiceInstance.stop()


