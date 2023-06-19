import scipy.signal
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numpy
import pyautogui
import math
import MouseLock
class Metamotion:

    METAMOTION_ADDRESS = "E7:DA:B1:97:93:7C"
    metawear = None
    gyro = None
    acc = None
    x_cordinate_list = []
    y_cordinate_list = []
    screen_Width = 0
    screen_Height = 0
    x_list = []
    y_list = []
    pyautogui.FAILSAFE = False
    counter = 0
    currX, currY = pyautogui.position()
    def __init__(self):
        self.connect_device(self.METAMOTION_ADDRESS)
        self.accCallback = FnVoid_VoidP_DataP(self.acc_data_handler)
        self.gyroCallback = FnVoid_VoidP_DataP(self.gyro_data_handler)
        self.screen_Width = pyautogui.size()[0]
        self.screen_Height = pyautogui.size()[1]
        self.mouseLock = False

    def connect_device(self, adddress):
        self.metawear = MetaWear(adddress)
        self.metawear.connect()
        print("Connected to " + self.metawear.address + " over " + ("USB" if self.metawear.usb.is_connected else "BLE"))

    def disconnect_device(self):
        if self.metawear is not None:
            # stop acc
            libmetawear.mbl_mw_acc_stop(self.metawear.board)
            libmetawear.mbl_mw_acc_disable_acceleration_sampling(self.metawear.board)

            # stop gyro
            libmetawear.mbl_mw_gyro_bmi160_stop(self.metawear.board)
            libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(self.metawear.board)

            # unsubscribe acc
            self.acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.metawear.board)
            libmetawear.mbl_mw_datasignal_unsubscribe(self.acc)

            # unsubscribe gyro
            self.gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.metawear.board)
            libmetawear.mbl_mw_datasignal_unsubscribe(self.gyro)

            # disconnect
            libmetawear.mbl_mw_debug_disconnect(self.metawear.board)

    def configure_device(self):
        if self.metawear is not None:
            print("Configuring device")
            libmetawear.mbl_mw_settings_set_connection_parameters(self.metawear.board, 7.5, 7.5, 0, 6000)
            sleep(1.5)

            # config gyro ASLINDA ACC OLARAK ÇALIŞIYOR
            libmetawear.mbl_mw_acc_bmi160_set_odr(self.metawear.board, AccBmi160Odr._400Hz)  # BMI 160 specific call
            libmetawear.mbl_mw_acc_bosch_set_range(self.metawear.board, AccBoschRange._4G)
            libmetawear.mbl_mw_acc_write_acceleration_config(self.metawear.board)

            # # config acc ASLINDA GYRO OLARAK ÇALIŞIYOR
            # libmetawear.mbl_mw_gyro_bmi160_set_range(self.metawear.board, GyroBoschRange._2000dps)
            # libmetawear.mbl_mw_gyro_bmi160_set_odr(self.metawear.board, GyroBoschOdr._200Hz)
            # libmetawear.mbl_mw_gyro_bmi160_write_config(self.metawear.board)

            # get acc signal and subscribe
            self.acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.metawear.board)
            libmetawear.mbl_mw_datasignal_subscribe(self.acc, None, self.gyroCallback)

            # get gyro signal and subscribe
            self.gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.metawear.board)
            libmetawear.mbl_mw_datasignal_subscribe(self.gyro, None, self.accCallback)
            print("configured.")

    def start_acc_gyro(self):
        print("Starting Accelerometer and Gyro...")
        # start acc
        libmetawear.mbl_mw_acc_start(self.metawear.board)

        # start gyro
        libmetawear.mbl_mw_gyro_bmi160_start(self.metawear.board)
        print("Acclerometer and gyro started.")

    def read_acc(self):
        print(libmetawear.mbl_mw_datasignal_read(self.gyro))

    def acc_data_handler(self, ctx, data):
        #sadas
        pass

    def gyro_data_handler(self, ctx, data):
        # print("GYRO X: {} Y: {}".format(self.BULL_SHIT(data)[0], self.BULL_SHIT(data)[1]))
        gyrodata = self.BULL_SHIT(data)
        self.x_list.append(gyrodata[0])
        self.y_list.append(gyrodata[1])

        if len(self.x_list) == 31 and len(self.y_list) == 31:
            self.x_list = list(savgol_filter(self.x_list, 30, 1))
            self.y_list = list(savgol_filter(self.y_list, 30, 1))

            for i in self.x_list:
                self.x_cordinate_list.append(int(numpy.interp(self.x_list[int(i)], [-0.50, 0.50], [0, self.screen_Width])))
                self.y_cordinate_list.append(int(numpy.interp(self.y_list[int(i)], [-0.50, 0.50], [0, self.screen_Height])))
            self.x_cordinate_list = list(savgol_filter(self.x_cordinate_list, 30, 1))
            self.y_cordinate_list = list(savgol_filter(self.y_cordinate_list, 30, 1))

            xCoordinate = int(sum(self.x_cordinate_list)/len(self.x_cordinate_list))
            yCoordinate = int(sum(self.y_cordinate_list)/len(self.y_cordinate_list))


            print('x: {} y: {}'.format(xCoordinate, yCoordinate))
            self.currX, self.currY = pyautogui.position()


            if abs(xCoordinate - self.currX) > 18 or abs(yCoordinate - self.currY) > 18:

                if not MouseLock.voiceMouseLock:
                    print(MouseLock.voiceMouseLock)
                    pyautogui.moveTo(xCoordinate, yCoordinate, duration=0.1)
                    self.xOldCoordinate = xCoordinate
                    self.yOldCoordinate = yCoordinate

            self.x_cordinate_list.clear()
            self.y_cordinate_list.clear()
            self.x_list.clear()
            self.y_list.clear()

        # self.counter = self.counter+1
        # print(self.counter)

    def BULL_SHIT(self,data):
        xAxis = float(str(parse_value(data)).split(" ")[2].replace(",", ""))
        yAxis = float(str(parse_value(data)).split(" ")[5].replace(",", ""))
        return xAxis, yAxis