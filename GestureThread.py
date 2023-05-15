import threading
import GestureOperations as go
import VoiceDetection as vd

class GestureThread(threading.Thread):
    def __init__(self, lefClickGesture, rightClickGesture, dragGesture, doubleClickGesture):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.gestureInstance = go.GestureOperations(lefClickGesture, rightClickGesture, dragGesture, doubleClickGesture)

    def run(self):
        try:
            while not self.stop_event.is_set():
                self.gestureInstance.start()

            self.gestureInstance.stop()
        except:
            print('hata')
        finally:
            self.gestureInstance.stop()

    def stop(self):
        self.stop_event.set()
        self.gestureInstance.stop()