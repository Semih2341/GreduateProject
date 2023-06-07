import Metamotion as mm
import VoiceDetection as ok
import threading
import Gestures
import GestureThread as gt
import VoiceThread as vt
import multiprocessing as mp
import gui
counter = 0
didSaidLock = False
stop_sound_thread = False
stop_mouse_thread = False

def MouseLock():
    stop_mouse_thread !=stop_mouse_thread


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
    # voiceDropButtonName = "bırak"
    # voiceHoldButtonName = "tut"
    # voiceLeftButtonName = "domates"
    # voiceRightButtonName = "salam"
    # voiceDoubleClickButtonName = "çift tıkla"

    # VoiceThreadDenemeNew = ok.VoiceDetection(rightVoice=voiceRightButtonName,
    #                                               leftVoice=voiceLeftButtonName,
    #                                               holdVoice=voiceHoldButtonName,
    #                                               dropVoice=voiceDropButtonName,
    #                                               doubleVoice=voiceDoubleClickButtonName)
    # newVoiceThread = mp.Process(target=VoiceThreadDenemeNew.start)
    # newVoiceThread.start()
    # sleep(10)
    # newVoiceThread.kill()
    # print("kapadı")
    # VoiceThreadDenemeNew2 = ok.VoiceDetection(rightVoice="sucuk",
    #                                               leftVoice=voiceLeftButtonName,
    #                                               holdVoice=voiceHoldButtonName,
    #                                               dropVoice=voiceDropButtonName,
    #                                               doubleVoice=voiceDoubleClickButtonName)
    # newVoiceThread2 = mp.Process(target=VoiceThreadDenemeNew2.start)
    # newVoiceThread2.start()
    # sleep(30)
    # newVoiceThread2.kill()

    GUI = gui.GUIPages()
    # GUI.MoveHeadToRightPG()
    GUI.GesturePopUpPG()
    # voiceMenuThread = threading.Thread(target=GUI.VoicePopUpPG())
    # voiceMenuThread.start()
    # voiceMenuThread.join()
    # mouseThread = threading.Thread(target=Mouse)
    # mouseThread.start()
    # soundThread.join()
    # mouseThread.join()
    # MetaMotion = mm.Metamotion()
    # MetaMotion.configure_device()
    # MetaMotion.start_acc_gyro()
    # sleep(30)

    # gestureThreadInstance.start()


