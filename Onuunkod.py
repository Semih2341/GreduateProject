import speech_recognition as sr
import pyautogui
import main
from time import sleep


createListenObject = sr.Recognizer()


# Ses kaydını başlatma ve birinci ve ikinci sesli komutları algılama
class VoiceDetection:
    def __init__(self, rightVoice, leftVoice, holdVoice, dropVoice):
        self.commandRight = rightVoice
        self.commandLeft = leftVoice
        self.commandHold = holdVoice
        self.commandDrop = dropVoice

    # def DetectCommandRight(self):
    #     try:
    #         with sr.Microphone() as source:
    #             print("Lütfen right komutu söyleyin:")
    #             audio = createListenObject.listen(source, None, 2)
    #             self.commandRight = createListenObject.recognize_google(audio, language="tr-tr")
    #             print('Komut 1: {}'.format(self.commandRight))
    #     except:
    #         print("zaman aşımı")
    # def DetectCommandLeft(self):
    #     with sr.Microphone() as source:
    #         print("Lütfen left komutu söyleyin:")
    #         audio = createListenObject.listen(source, None, 2)
    #         self.commandLeft = createListenObject.recognize_google(audio, language="tr-tr")
    #         print('Komut 2: {}'.format(self.commandLeft))
    #
    # def DetectHoldCommand(self):
    #     with sr.Microphone() as source:
    #         print("Lütfen hold komutu söyleyin:")
    #         audio = createListenObject.listen(source, None, 2)
    #         self.commandHold = createListenObject.recognize_google(audio, language="tr-tr")
    #         print('Komut 3: {}'.format(self.commandHold))
    #
    # def DetectCommandDrop(self):
    #     with sr.Microphone() as source:
    #         print("Lütfen drop komutu söyleyin:")
    #         audio = createListenObject.listen(source, None, 2)
    #         self.commandDrop = createListenObject.recognize_google(audio, language="tr-tr")
    #         print('Komut 3: {}'.format(self.commandDrop))


    def DetectVoice(self):
        try:
            with sr.Microphone() as source:
                audio = createListenObject.listen(source, None, 2)  # Ses kaydını başlat
                text = createListenObject.recognize_google(audio, language="tr-tr")  # Tanıma işlemi
                return text
        except sr.RequestError:
            print("İnternet bağlantısı yok.")
        except sr.UnknownValueError:
            print("Ses anlaşılamadı.")


    def Starter(self):
        print("denmee")
        voicedetection = VoiceDetection(rightVoice=self.commandRight, leftVoice=self.commandLeft,
                                        holdVoice=self.commandHold, dropVoice=self.commandDrop)
        # voicedetection.DetectCommandRight()
        # voicedetection.DetectCommandLeft()
        # voicedetection.DetectHoldCommand()
        # voicedetection.DetectCommandDrop()
        while True:
            command = voicedetection.DetectVoice()

            if command == voicedetection.commandRight:
                sleep(0.1)
                pyautogui.rightClick()
                # main.MouseLock()
                print("Sağ Tıklama gerçekleştirildi.")
            elif command == voicedetection.commandLeft:
                sleep(0.1)
                pyautogui.leftClick()
                print("Sol Tıklama gerçekleştirildi.")
            elif command == voicedetection.commandHold:
                sleep(0.1)
                pyautogui.mouseDown
                print("Sol Tıklama gerçekleştirildi.")
            elif command == voicedetection.commandDrop:
                sleep(0.1)
                pyautogui.mouseUp
                print("Sol Tıklama gerçekleştirildi.")
            elif command == "programdan çık":
                break
            else:
                print("Geçersiz komut. Tekrar deneyiniz")

# if __name__ == "__main__":
