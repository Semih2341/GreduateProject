import Metamotion as mm
from time import sleep
import Onuunkod as ok
import threading
import Gestures
import GestureThread as gt
import VoiceThread as vt
import gui
counter = 0
didSaidLock = False

stop_sound_thread = False
stop_mouse_thread = False

def MouseLock():
    stop_mouse_thread !=stop_mouse_thread




def Mouse():
    while True:
        MetaMotion = mm.Metamotion()
        MetaMotion.configure_device()
        MetaMotion.start_acc_gyro()
        if stop_sound_thread:
            print("MouseDurdu")
            break



    # sleep(10)

    # MetaMotion.disconnect_device()
if __name__ == "__main__":


    # gestureThreadInstance = gt.GestureThread(lefClickGesture=Gestures.Gestures.LEFTBLINK,
    #                                          rightClickGesture=Gestures.Gestures.RIGHTBLINK,
    #                                          dragGesture=Gestures.Gestures.MOUTHOPEN,
    #                                          doubleClickGesture=Gestures.Gestures.BOTHEYEBLINK)
    # gestureThreadInstance.stop()
    # gestureThreadInstance.start()
    # gui.MoveHeadToRightPG()
    # gui.MoveHeadToLeftPG()
    # gui.CloseRightEyePG()
    # gui.CloseLeftEyePG()
    # GUI = gui.GUIPages()
    # GUI.GesturePopUpPG()
    GUI = gui.GUIPages()
    voiceMenuThread = threading.Thread(target=GUI.VoicePopUpPG())
    voiceMenuThread.start()
    voiceMenuThread.join()
    # mouseThread = threading.Thread(target=Mouse)
    # mouseThread.start()
    # soundThread.join()
    # mouseThread.join()

    # gestureThreadInstance.start()


