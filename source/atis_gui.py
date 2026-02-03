#author#======================================
#file:atis_gui.py
#wangxiaochen CFR7445 2022.01.14
#Copyright (c) 2022 一天两根冰棍
#=============================================

#import libraries#============================
import string
from tkinter.ttk import *
from tkinter import *
from DEFINE import *
from LIBRARY import *
import voice
from datetime import datetime
from pykeyboard import PyKeyboard
from threading import Timer
#=============================================

#key value define#============================
gui_windows = Tk() #创建根窗口
gui_keyboard = PyKeyboard()
gui_information_part = Frame(gui_windows, width = gui_information_part_xsize, height = gui_information_part_ysize, relief = "groove", borderwidth = gui_frame_borderwidth) #创建信息填写部分容器
gui_button_part = Frame(gui_windows, width = gui_button_part_xsize, height = gui_button_part_ysize, relief = "groove", borderwidth = gui_frame_borderwidth) #创建按钮部分容器
gui_message_part = Frame(gui_windows, width = gui_message_part_xsize, height = gui_message_part_ysize, relief = "groove", borderwidth = gui_frame_borderwidth) #创建按钮部分容器
airport = StringVar()
information_code = StringVar()
UTC_time = StringVar()
runway = StringVar()
runway_mode = StringVar()
wind_direction = StringVar()
wind_speed = StringVar()
wind_change = StringVar()
meteorological = StringVar()
cloud_height = StringVar()
visibility = StringVar()
temperature = StringVar()
dew_point = StringVar()
QNH = StringVar()
transition_altitude = StringVar()
transition_level = StringVar()
dep_frequency = StringVar()
del_frequency = StringVar()
ATIS_voice_volume = IntVar()
ATIS_voice_rate = IntVar()
message_output = StringVar()
airport.set(airport_inuse[0])
information_code.set(information_code_inuse[0])
UTC_time.set(UTC_time_inuse[0])
runway_mode.set(runway_mode_inuse_chinese[0])
atis_mode = atis_mode_dep
atis_broadcast_interval = ATIS_broadcast_interval
ATIS_voice_volume.set(voice.ATIS_voice_volume)
ATIS_voice_rate.set(voice.ATIS_voice_rate)
ptt_button_timer_count = 0
ptt_button_mode = IntVar()
ptt_button_mode.set(0)
atis_broadcast_flag = FALSE
atis_broadcast_count = 1
#=============================================

#function#====================================
def message_print(input_string):
    message_output.set(input_string)


def timer_handler():
    global ptt_button_timer_count
    global atis_broadcast_count
    global universal_timer

    if(atis_broadcast_flag == TRUE):
        ptt_button_timer_count = ptt_button_timer_count + 1
        atis_broadcast_count = atis_broadcast_count + 1
        print(ptt_button_timer_count)
        if(ptt_button_timer_count == int(voice.ATIS_voice_file_length + ATIS_broadcast_interval)):
            ptt_button_timer_count = 0
            press_PTT_button()
        else:
            pass
    else:
        if(ptt_button_timer_count != 0):
            ptt_button_timer_count = 0
        else:
            pass

    universal_timer = Timer(1, timer_handler)
    universal_timer.start()


universal_timer = Timer(1, timer_handler)


def start_universal_timer():
    universal_timer.start()


def cancel_universal_timer():
    universal_timer.cancel()


start_universal_timer()

def close_windows():
    cancel_universal_timer()
    gui_windows.destroy()

def all_information_update():
    voice.airport = airport.get()
    voice.information_code = information_code.get()
    voice.UTC_time = UTC_time.get()
    voice.runway = runway.get()
    voice.runway_mode = runway_mode.get()
    voice.wind_direction = wind_direction.get()
    voice.wind_speed = wind_speed.get()
    voice.wind_change = wind_change.get()
    voice.meteorological = meteorological.get()
    voice.cloud_height = cloud_height.get()
    voice.visibility = visibility.get()
    voice.temperature = temperature.get()
    voice.dew_point = dew_point.get()
    voice.QNH = QNH.get()
    voice.transition_altitude = transition_altitude.get()
    voice.transition_level = transition_level.get()
    voice.dep_frequency = dep_frequency.get()
    voice.del_frequency = del_frequency.get()

def update_utc_information_code():
    time_temp = datetime.utcnow()
    if(len(str(time_temp.hour)) == 1):
        UTC_time.set("0" + str(time_temp.hour) + "00")
    else:
        UTC_time.set(str(time_temp.hour) + "00")
    information_code.set(information_code_inuse[time_temp.hour])

def listen_ATIS_voice():
    message_print("正在试听ATIS...")
    all_information_update()
    voice.ATIS_audition()
    message_print("试听ATIS结束。")

def generate_ATIS_voice_file():
    all_information_update()
    voice.ATIS_to_file()
    message_print("导出音频，"+"单次播报ATIS时长为"+ str(int(voice.ATIS_voice_file_length))+ "秒。")

def set_voice_rate(value):
    voice.set_ATIS_voice_engine_rate(ATIS_voice_rate.get())
    message_print("ATIS音频速率设置为" + str(ATIS_voice_rate.get()))

def set_voice_volume(value):
    voice.set_ATIS_voice_engine_volume(ATIS_voice_volume.get())
    message_print("ATIS音频音量设置为" + str(ATIS_voice_volume.get()))

def press_PTT_button():
    gui_keyboard.tap_key(gui_keyboard.function_keys[1])
    message_print("按下按键，频率内已经开始播报ATIS。")


def start_play_ATIS():
    global atis_broadcast_flag
    global atis_broadcast_count
    if(ptt_button_mode.get() == 0):
        atis_broadcast_count = 1
        atis_broadcast_flag = TRUE
        press_PTT_button()
    elif(ptt_button_mode.get() == 1):
        gui_keyboard.press_key(gui_keyboard.function_keys[1])
        print("ssss")
        message_print("按下按键，频率内已经开始播报ATIS。")
    else:
        pass

def stop_play_ATIS():
    global atis_broadcast_flag
    global atis_broadcast_count
    if(ptt_button_mode.get() == 0):
        atis_broadcast_count = 1
        atis_broadcast_flag = FALSE
        message_print("将在本次ATIS播报完成后停止播报ATIS。")
    elif(ptt_button_mode.get() == 1):
        gui_keyboard.release_key(gui_keyboard.function_keys[1])
        message_print("松开按键，已停止播报ATIS。")
    else:
        pass

def destroy_frame():
    for widget in gui_information_part.winfo_children():
        widget.destroy()

    for widget in gui_button_part.winfo_children():
        widget.destroy()

#离场通播菜单------
def dep_ATIS_gui():
    destroy_frame()
    
    #初始化变量
    global atis_mode
    global airport
    global information_code
    global UTC_time
    global runway
    global runway_mode
    global wind_direction
    global wind_speed
    global wind_change
    global meteorological
    global cloud_height
    global visibility
    global temperature
    global dew_point
    global QNH
    global transition_altitude
    global transition_level
    global dep_frequency
    global dep_frequency
    atis_mode = atis_mode_dep
    voice.ATIS_mode = atis_mode

    #基本信息填写部分
    basic_txt   = Label(gui_information_part, text = "基本信息", font = "楷体 14", justify = "center") #基本信息标题
    basic_txt.grid(row = 1, column = 1, columnspan = 6, pady = gui_headline_pady) #基本信息标题位置设置
    aiport_txt = Label(gui_information_part, text = "机场：", font = "黑体 10", justify = "right")
    information_txt = Label(gui_information_part, text = "通播代码：", font = "黑体 10", justify = "right")
    global_time_txt = Label(gui_information_part, text = "世界时间(UTC)：", font = "黑体 10", justify = "right")
    aiport_txt.grid(row = 2, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    information_txt.grid(row = 2, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    global_time_txt.grid(row = 2, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = airport, values = airport_inuse, width = gui_combobox_width).grid(row = 2, column = 2, sticky = W, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = information_code, values = information_code_inuse, width = gui_combobox_width).grid(row = 2, column = 4, sticky = W, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = UTC_time, values = UTC_time_inuse, width = gui_combobox_width).grid(row = 2, column = 6, sticky = W, pady = gui_option_pady)
    
    #运行信息填写部分
    running_txt = Label(gui_information_part, text = "运行信息", font = "楷体 14", justify = "right") #运行信息标题
    running_txt.grid(row = 3, column = 1, columnspan = 6, pady = gui_headline_pady) #运行信息标题位置设置
    runway_txt = Label(gui_information_part, text = "起飞跑道：", font = "黑体 10", justify = "right")
    runway_mode_txt = Label(gui_information_part, text = "运行模式：", font = "黑体 10", justify = "right")
    runway_txt.grid(row = 4, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    runway_mode_txt.grid(row = 4, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = runway, width = gui_entry_width).grid(row = 4, column = 2, sticky = W, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = runway_mode, values = runway_mode_inuse_chinese, width = 24).grid(row = 4, column = 4, columnspan = 3, sticky = W, pady = gui_option_pady)
    
    #气象信息填写部分
    weather_txt = Label(gui_information_part, text = "气象信息", font = "楷体 14", justify = "center") #气象信息标题
    weather_txt.grid(row = 5, column = 1, columnspan = 6, pady = gui_headline_pady) #气象信息标题位置设置
    wind_direction_txt = Label(gui_information_part, text = "风向：", font = "黑体 10", justify = "right")
    wind_speed_txt = Label(gui_information_part, text = "风速：", font = "黑体 10", justify = "right")
    wind_change_txt = Label(gui_information_part, text = "风向变化：", font = "黑体 10", justify = "right")
    meteorological_txt = Label(gui_information_part, text = "气象：", font = "黑体 10", justify = "right")
    cloud_height_txt = Label(gui_information_part, text = "云底高度：", font = "黑体 10", justify = "right")
    visibility_txt = Label(gui_information_part, text = "能见度：", font = "黑体 10", justify = "right")
    temperature_txt = Label(gui_information_part, text = "温度：", font = "黑体 10", justify = "right")
    dew_point_txt = Label(gui_information_part, text = "露点：", font = "黑体 10", justify = "right")
    QNH_txt = Label(gui_information_part, text = "修正海压：", font = "黑体 10", justify = "right")
    transition_altitude_txt = Label(gui_information_part, text = "过渡高度：", font = "黑体 10", justify = "right")
    transition_level_txt = Label(gui_information_part, text = "过渡高度层：", font = "黑体 10", justify = "right")
    wind_direction_txt.grid(row = gui_combobox_width, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    wind_speed_txt.grid(row = gui_combobox_width, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    wind_change_txt.grid(row = gui_combobox_width, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    meteorological_txt.grid(row = 7, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    cloud_height_txt.grid(row = 7, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    visibility_txt.grid(row = 8, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    temperature_txt.grid(row = 8, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    dew_point_txt.grid(row = 8, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    QNH_txt.grid(row = 9, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    transition_altitude_txt.grid(row = 9, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    transition_level_txt.grid(row = 9, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = wind_direction, width = gui_entry_width).grid(row = 6, column = 2, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = wind_speed, width = gui_entry_width).grid(row = 6, column = 4, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = wind_change, width = gui_entry_width).grid(row = 6, column = 6, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = meteorological, width = gui_entry_width + 15).grid(row = 7, column = 2, sticky = W, pady = gui_option_pady, columnspan = 6)
    Entry(gui_information_part, textvariable = cloud_height, width = gui_entry_width).grid(row = 7, column = 6, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = visibility, width = gui_entry_width).grid(row = 8, column = 2, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = temperature, width = gui_entry_width).grid(row = 8, column = 4, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = dew_point, width = gui_entry_width).grid(row = 8, column = 6, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = QNH, width = gui_entry_width).grid(row = 9, column = 2, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = transition_altitude, width = gui_entry_width).grid(row = 9, column = 4, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = transition_level, width = gui_entry_width).grid(row = 9, column = 6, sticky = W, pady = gui_option_pady)

    #管制信息填写部分
    control_txt = Label(gui_information_part, text = "管制信息", font = "楷体 14", justify = "center") #管制信息标题
    control_txt.grid(row = 11, column = 1, columnspan = 6, pady = gui_headline_pady) #管制信息位置设置
    del_frequency_txt = Label(gui_information_part, text = "放行频率：", font = "黑体 10", justify = "right")
    dep_frequency_txt = Label(gui_information_part, text = "离场频率：", font = "黑体 10", justify = "right")
    del_frequency_txt.grid(row = 12, column = 1, sticky = W, padx = gui_option_padx)
    dep_frequency_txt.grid(row = 12, column = 3, sticky = W, padx = gui_option_padx)
    Entry(gui_information_part, textvariable = del_frequency, width = gui_entry_width).grid(row = 12, column = 2, sticky = W)
    Entry(gui_information_part, textvariable = dep_frequency, width = gui_entry_width).grid(row = 12, column = 4, sticky = W)

    #功能按钮
    Button(gui_button_part, text = "更新代码", width = gui_button_width, command = update_utc_information_code).grid(row = 1, column = 1, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "试听通播", width = gui_button_width, command = listen_ATIS_voice).grid(row = 1, column = 2, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "播放通播", width = gui_button_width, command = start_play_ATIS).grid(row = 1, column = 3, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "停止通播", width = gui_button_width, command = stop_play_ATIS).grid(row = 1, column = 4, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "导出音频", width = gui_button_width, command = generate_ATIS_voice_file).grid(row = 1, column = 5, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "获取天气", width = gui_button_width).grid(row = 1, column = 6, pady = gui_button_pady, padx = gui_button_padx)


#进场通播菜单------
def arr_ATIS_gui():
    destroy_frame()
    
    #初始化变量
    global atis_mode
    global airport
    global information_code
    global UTC_time
    global runway
    global runway_mode
    global wind_direction
    global wind_speed
    global wind_change
    global meteorological
    global cloud_height
    global visibility
    global temperature
    global dew_point
    global QNH
    global transition_altitude
    global transition_level
    global dep_frequency
    global dep_frequency
    atis_mode = atis_mode_arr
    voice.ATIS_mode = atis_mode

    #基本信息填写部分
    basic_txt   = Label(gui_information_part, text = "基本信息", font = "楷体 14", justify = "center") #基本信息标题
    basic_txt.grid(row = 1, column = 1, columnspan = 6, pady = gui_headline_pady) #基本信息标题位置设置
    aiport_txt = Label(gui_information_part, text = "机场：", font = "黑体 10", justify = "right")
    information_txt = Label(gui_information_part, text = "通播代码：", font = "黑体 10", justify = "right")
    global_time_txt = Label(gui_information_part, text = "世界时间(UTC)：", font = "黑体 10", justify = "right")
    aiport_txt.grid(row = 2, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    information_txt.grid(row = 2, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    global_time_txt.grid(row = 2, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = airport, values = airport_inuse, width = gui_combobox_width).grid(row = 2, column = 2, sticky = W, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = information_code, values = information_code_inuse, width = gui_combobox_width).grid(row = 2, column = 4, sticky = W, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = UTC_time, values = UTC_time_inuse, width = gui_combobox_width).grid(row = 2, column = 6, sticky = W, pady = gui_option_pady)
    
    #运行信息填写部分
    running_txt = Label(gui_information_part, text = "运行信息", font = "楷体 14", justify = "right") #运行信息标题
    running_txt.grid(row = 3, column = 1, columnspan = 6, pady = gui_headline_pady) #运行信息标题位置设置
    runway_txt = Label(gui_information_part, text = "落地跑道：", font = "黑体 10", justify = "right")
    runway_mode_txt = Label(gui_information_part, text = "运行模式：", font = "黑体 10", justify = "right")
    runway_txt.grid(row = 4, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    runway_mode_txt.grid(row = 4, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = runway, width = gui_entry_width).grid(row = 4, column = 2, sticky = W, pady = gui_option_pady)
    Combobox(gui_information_part, textvariable = runway_mode, values = runway_mode_inuse_chinese, width = 24).grid(row = 4, column = 4, columnspan = 3, sticky = W, pady = gui_option_pady)
    
    #气象信息填写部分
    weather_txt = Label(gui_information_part, text = "气象信息", font = "楷体 14", justify = "center") #气象信息标题
    weather_txt.grid(row = 5, column = 1, columnspan = 6, pady = gui_headline_pady) #气象信息标题位置设置
    wind_direction_txt = Label(gui_information_part, text = "风向：", font = "黑体 10", justify = "right")
    wind_speed_txt = Label(gui_information_part, text = "风速：", font = "黑体 10", justify = "right")
    wind_change_txt = Label(gui_information_part, text = "风向变化：", font = "黑体 10", justify = "right")
    meteorological_txt = Label(gui_information_part, text = "气象：", font = "黑体 10", justify = "right")
    cloud_height_txt = Label(gui_information_part, text = "云底高度：", font = "黑体 10", justify = "right")
    visibility_txt = Label(gui_information_part, text = "能见度：", font = "黑体 10", justify = "right")
    temperature_txt = Label(gui_information_part, text = "温度：", font = "黑体 10", justify = "right")
    dew_point_txt = Label(gui_information_part, text = "露点：", font = "黑体 10", justify = "right")
    QNH_txt = Label(gui_information_part, text = "修正海压：", font = "黑体 10", justify = "right")
    transition_altitude_txt = Label(gui_information_part, text = "过渡高度：", font = "黑体 10", justify = "right")
    transition_level_txt = Label(gui_information_part, text = "过渡高度层：", font = "黑体 10", justify = "right")
    wind_direction_txt.grid(row = gui_combobox_width, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    wind_speed_txt.grid(row = gui_combobox_width, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    wind_change_txt.grid(row = gui_combobox_width, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    meteorological_txt.grid(row = 7, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    cloud_height_txt.grid(row = 7, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    visibility_txt.grid(row = 8, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    temperature_txt.grid(row = 8, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    dew_point_txt.grid(row = 8, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    QNH_txt.grid(row = 9, column = 1, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    transition_altitude_txt.grid(row = 9, column = 3, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    transition_level_txt.grid(row = 9, column = 5, sticky = W, padx = gui_option_padx, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = wind_direction, width = gui_entry_width).grid(row = 6, column = 2, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = wind_speed, width = gui_entry_width).grid(row = 6, column = 4, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = wind_change, width = gui_entry_width).grid(row = 6, column = 6, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = meteorological, width = gui_entry_width + 15).grid(row = 7, column = 2, sticky = W, pady = gui_option_pady, columnspan = 6)
    Entry(gui_information_part, textvariable = cloud_height, width = gui_entry_width).grid(row = 7, column = 6, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = visibility, width = gui_entry_width).grid(row = 8, column = 2, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = temperature, width = gui_entry_width).grid(row = 8, column = 4, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = dew_point, width = gui_entry_width).grid(row = 8, column = 6, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = QNH, width = gui_entry_width).grid(row = 9, column = 2, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = transition_altitude, width = gui_entry_width).grid(row = 9, column = 4, sticky = W, pady = gui_option_pady)
    Entry(gui_information_part, textvariable = transition_level, width = gui_entry_width).grid(row = 9, column = 6, sticky = W, pady = gui_option_pady)

    #管制信息填写部分
    control_txt = Label(gui_information_part, text = "管制信息", font = "楷体 14", justify = "center") #管制信息标题
    control_txt.grid(row = 11, column = 1, columnspan = 6, pady = gui_headline_pady) #管制信息位置设置
    del_frequency_txt = Label(gui_information_part, text = "塔台频率：", font = "黑体 10", justify = "right")
    dep_frequency_txt = Label(gui_information_part, text = "进近频率：", font = "黑体 10", justify = "right")
    del_frequency_txt.grid(row = 12, column = 1, sticky = W, padx = gui_option_padx)
    dep_frequency_txt.grid(row = 12, column = 3, sticky = W, padx = gui_option_padx)
    Entry(gui_information_part, textvariable = del_frequency, width = gui_entry_width).grid(row = 12, column = 2, sticky = W)
    Entry(gui_information_part, textvariable = dep_frequency, width = gui_entry_width).grid(row = 12, column = 4, sticky = W)

    #功能按钮
    Button(gui_button_part, text = "更新代码", width = gui_button_width, command = update_utc_information_code).grid(row = 1, column = 1, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "试听通播", width = gui_button_width, command = listen_ATIS_voice).grid(row = 1, column = 2, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "播放通播", width = gui_button_width, command = start_play_ATIS).grid(row = 1, column = 3, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "停止通播", width = gui_button_width, command = stop_play_ATIS).grid(row = 1, column = 4, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "导出音频", width = gui_button_width, command = generate_ATIS_voice_file).grid(row = 1, column = 5, pady = gui_button_pady, padx = gui_button_padx)
    Button(gui_button_part, text = "获取天气", width = gui_button_width).grid(row = 1, column = 6, pady = gui_button_pady, padx = gui_button_padx)


#设置菜单------
def menu_setting_gui():
    global ATIS_voice_rate
    destroy_frame()
    volume_bar = Scale(gui_information_part, from_ = 0, to = 100, orient = HORIZONTAL, length = 500, command = set_voice_volume, tickinterval = 10, label = "ATIS 播放音量", variable = ATIS_voice_volume)
    volume_bar.grid(row = 2, column = 1, columnspan = 1, pady = gui_headline_pady)
    rate_bar = Scale(gui_information_part, from_ = 0, to = 250, orient = HORIZONTAL, length = 500, command = set_voice_rate, tickinterval = 50, label = "ATIS 播放音速", variable = ATIS_voice_rate)
    rate_bar.grid(row = 4, column = 1, columnspan = 1, pady = gui_headline_pady)
    ptt_mode_checkbutton = Checkbutton(gui_information_part, variable = ptt_button_mode, text = "PTT按键连续按下模式")
    ptt_mode_checkbutton.grid(row = 5, column = 1, columnspan = 1, pady = gui_headline_pady)
    volume_bar.set(voice.ATIS_voice_volume)
    rate_bar.set(voice.ATIS_voice_rate)
#=============================================

#operation#===================================
#windows------
gui_windows.title(software_title) #设置窗口标题
gui_windows.iconbitmap(software_icon_path) #设置软件图标
gui_windows.geometry(software_windows_size) #设置窗口大小
#menu------
gui_menu = Menu(gui_windows) #在根窗口创建菜单
gui_menu.add_command(label = "离场通播", command = dep_ATIS_gui) #添加菜单
gui_menu.add_command(label = "进场通播", command = arr_ATIS_gui) #添加菜单
gui_menu.add_command(label = "软件设置", command = menu_setting_gui) #添加菜单
#gui_menu.add_command(label = "语音登录", command = menu_login_gui) #添加菜单
gui_windows.config(menu = gui_menu) #显示菜单
gui_information_part.pack(anchor = "center") #放置信息填写部分容器
gui_button_part.pack(anchor = "center") #放置按钮部分容器
gui_message_part.pack(anchor = "center") #放置信息输出部分容器
dep_ATIS_gui() #显示初始界面，离场ATIS设置界面
gui_mess = Message(gui_message_part, anchor = "center", relief = "groove", textvariable = message_output, width = 300)
gui_mess.pack(expand = 1, anchor = "center", side = "right", padx = 5, pady = 5)
message_print("软件启动完成。")
gui_windows.protocol("WM_DELETE_WINDOW", close_windows)
#保持窗口------
gui_windows.mainloop()
#=============================================