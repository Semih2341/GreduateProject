import speech_recognition as sr
import pyautogui
from time import sleep


createListenObject = sr.Recognizer()


# Ses kaydını başlatma ve birinci ve ikinci sesli komutları algılama
class VoiceDetection:
    def __init__(self):
        self.command1 = ""
        self.command2 = ""
        self.command3 = ""
        self.command4 = ""

    def DetectCommandRight(self):
        with sr.Microphone() as source:
            print("Lütfen right komutu söyleyin:")
            audio = createListenObject.listen(source)
            self.command1 = createListenObject.recognize_google(audio, language="tr-tr")
            print('Komut 1: {}'.format(self.command1))

    def DetectCommandLeft(self):
        with sr.Microphone() as source:
            print("Lütfen left komutu söyleyin:")
            audio = createListenObject.listen(source)
            self.command2 = createListenObject.recognize_google(audio, language="tr-tr")
            print('Komut 2: {}'.format(self.command2))

    def DetectHoldCommand(self):
        with sr.Microphone() as source:
            print("Lütfen hold komutu söyleyin:")
            audio = createListenObject.listen(source)
            self.command3 = createListenObject.recognize_google(audio, language="tr-tr")
            print('Komut 3: {}'.format(self.command3))

    def DetectCommandDrop(self):
        with sr.Microphone() as source:
            print("Lütfen drop komutu söyleyin:")
            audio = createListenObject.listen(source)
            self.command4 = createListenObject.recognize_google(audio, language="tr-tr")
            print('Komut 3: {}'.format(self.command4))


    def DetectVoice(self):
        try:
            with sr.Microphone() as source:
                audio = createListenObject.listen(source)  # Ses kaydını başlat
                text = createListenObject.recognize_google(audio, language="tr-tr")  # Tanıma işlemi
                return text
        except sr.RequestError:
            print("İnternet bağlantısı yok.")
        except sr.UnknownValueError:
            print("Ses anlaşılamadı.")




if __name__ == "__main__":
    voicedetection = VoiceDetection()
    voicedetection.DetectCommandRight()
    voicedetection.DetectCommandLeft()
    voicedetection.DetectHoldCommand()
    voicedetection.DetectCommandDrop()
    while True:
        command = voicedetection.DetectVoice()

        if command == voicedetection.command1:
            sleep(0.1)
            pyautogui.rightClick()
            print("Sağ Tıklama gerçekleştirildi.")
        elif command == voicedetection.command2:
            sleep(0.1)
            pyautogui.leftClick()
            print("Sol Tıklama gerçekleştirildi.")
        elif command == voicedetection.command3:
            sleep(0.1)
            pyautogui.drop
            print("Sol Tıklama gerçekleştirildi.")
        elif command == voicedetection.command4:
            sleep(0.1)
            pyautogui.mouseUp
            print("Sol Tıklama gerçekleştirildi.")
        elif command == "programdan çık":
            break
        else:
            print("Geçersiz komut. Tekrar deneyiniz")
