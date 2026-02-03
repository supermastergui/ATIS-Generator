#author#======================================
#file:voice.py
#wangxiaochen CFR7445 2022.01.14
#Copyright (c) 2022 一天两根冰棍
#=============================================

#import libraries#============================
import pyttsx3
import librosa
from DEFINE import *
from LIBRARY import *
from ERROR import *
#=============================================

#key value define#============================
airport = "ZSAM"
information_code = "A"
UTC_time = "0800"
runway = "05"
runway_mode = "不指定(单跑道)"
wind_direction = "000"
wind_speed = "02"
wind_change = "010,070"
meteorological = STRING_NULL
cloud_height = "2100"
visibility = "9999"
temperature = "21"
dew_point = "-15"
QNH = "1021"
transition_altitude = "3000"
transition_level = "3600"
dep_frequency = "121.95"
del_frequency = "121.35"
string_to_voice = STRING_NULL
ATIS_voice_volume = voice_volume * 100
ATIS_voice_rate = voice_rate
ATIS_voice_file_length = librosa.get_duration(filename = voice_output_dir + voice_output_name)
ATIS_mode = atis_mode_dep
#=============================================

#function#====================================
#信息映射部分------
#机场映射函数，将ICAO映射为中文名称
#input : 语言(see LIBRARY.py,默认中文)
#return: 中文名or空字符串(转到错误处理)
def map_airport(language = voice_language_chinese):
    global airport
    for num in range(0 , len(airport_inuse)):
        if(airport == airport_inuse[num]):
            if(language == voice_language_chinese):
                return airport_inuse_chinese[num]
            elif(language == voice_language_english):
                return airport_inuse_english[num]
            else:
                error_handle(error_language_not_support)
                return STRING_NULL
        else:
            pass
    error_handle(error_airport_not_found)
    return STRING_NULL

#通播代码映射函数，将A~Z映射为读音解释法
#input : NULL
#return: 字母读音or空字符串(转到错误处理)
def map_letter_word(letter_input):
    for num in range(0, 26):
        if(information_code_inuse[num] == letter_input):
            return information_code_inuse_word[num]
        else:
            pass
    error_handle(error_information_code_not_found)
    return STRING_NULL

#数字映射函数，将阿拉伯数字映射为中文读音
#input : 0~9，语言(see LIBRARY.py,默认中文)
#return: 中文/英文读音or空字符串(转到错误处理)
def map_number(number_input, language = voice_language_chinese):
    for num in range(0, 10):
        if (number_input == num):
            if(language == voice_language_chinese):
                return number_inuse_chinese[num]
            elif(language == voice_language_english):
                return number_inuse_english[num]
            else:
                error_handle(error_language_not_support)
                return STRING_NULL
        else:
            pass
    error_handle(error_number_not_found)
    return STRING_NULL

#信息处理部分------
#字符串处理函数
#input : 待处理字符串，被转换内容（默认空），转换内容（默认空）， 语言（see LIBRARY.py,默认中文）
#output: 处理后读音字符串
def string_handle(string_input, string_identify = (), string_replace = () , language = voice_language_chinese):
    string_temp = STRING_NULL
    for char in string_input :
        if(ord(char) >=  48 and ord(char) <=  57): #for ASCII 0:0d48,9:0d57
            string_temp = string_temp + map_number(int(char), language)
        elif(ord(char) >= 65 and ord(char) <= 90): #for ASCII A:0d48,Z:0d57
            string_temp = string_temp + map_letter_word(char)
        else:
            for num in range(0, len(string_identify)):
                if(char == string_identify[num]):
                    string_temp = string_temp + string_replace[num]
                else:
                    pass
    return string_temp

#跑道处理函数
#input : 待处理跑道字符串，语言（see LIBRARY.py,默认中文） 
#output: 处理后读音字符串
#特殊字符识别: U:使用跑到;L:左;R:右;C:中;
def runway_handle(language = voice_language_chinese):
    string_temp = STRING_NULL
    for char in runway :
        if(ord(char) == 44): #for ASCII "," :0d44
            string_temp = string_temp + "。"
        elif(char == "U"):
            if(language == voice_language_chinese):
                string_temp = string_temp + "使用跑道:"
            elif(language == voice_language_english):
                string_temp = string_temp + "runway:"
            else:
                error_handle(error_language_not_support)
        elif(char == "L"):
            if(language == voice_language_chinese):
                string_temp = string_temp + "左"
            elif(language == voice_language_english):
                string_temp = string_temp + "left "
            else:
                error_handle(error_language_not_support)
        elif(char == "R"):
            if(language == voice_language_chinese):
                string_temp = string_temp + "右"
            elif(language == voice_language_english):
                 string_temp = string_temp + "right "
            else:
                error_handle(error_language_not_support)
        elif(char == "C"):
            if(language == voice_language_chinese):
                string_temp = string_temp + "中"
            elif(language == voice_language_english):
                string_temp = string_temp + "center "
            else:
                error_handle(error_language_not_support)
        else:
            string_temp = string_temp + map_number(number_input = int(char), language = language)
    return string_temp

#跑道模式处理函数
#input : 语言（see LIBRARY.py,默认中文） 
#output: 处理后的读音字符串or空字符串(转到错误处理)
def runway_mode_handle(language = voice_language_chinese):
    if(runway_mode == runway_mode_inuse_chinese[0]):
        return STRING_NULL
    else:
        if(language == voice_language_chinese):
            return runway_mode
        elif(language == voice_language_english):
            for num in range(0, len(runway_mode_inuse_chinese)):
                if(runway_mode == runway_mode_inuse_chinese[num]):
                    return runway_mode_inuse_english[num]
                else:
                    pass
            error_handle(error_runway_mode_not_found)
            return STRING_NULL
        else:
            error_handle(error_language_not_support)
            return STRING_NULL
            

#数字整体读法处理函数
#input : 待处理数字字符串, 语言（see LIBRARY.py,默认中文） 
#output: 处理后数字整体读音字符串
#特殊识别: 将添加百和千，个位及十位省略
def number_handle(number_input, language = voice_language_chinese):
    string_temp = STRING_NULL
    if(len(number_input) == 3):
        if(language == voice_language_chinese):
            string_temp = number_input[0] + "百"
        elif(language == voice_language_english):
            string_temp = map_number(number_input = int(number_input[0]), language = voice_language_english) + "hundred "
        else:
            error_handle(error_language_not_support)
    elif(len(number_input) == 4):
        if(number_input[1] == "0"):
            if(language == voice_language_chinese):
                string_temp = number_input[0] + "千"
            elif(language == voice_language_english):
                string_temp = map_number(number_input = int(number_input[0]), language = voice_language_english) + "thousand "
            else:
                error_handle(error_language_not_support)
        else:
            if(language == voice_language_chinese):
                string_temp = number_input[0] + "千" + number_input[1] + "百"
            elif(language == voice_language_english):
                string_temp = map_number(number_input = int(number_input[0]), language = voice_language_english) + "thousand " + map_number(number_input = int(number_input[1]), language = voice_language_english) + "hundred "
            else:
                error_handle(error_language_not_support)
    else:
        error_handle(error_string_length_not_match)
    return string_temp

#声音生成部分------
#中文基本信息语音生成函数
#input: NULL
#output: NULL
def speak_basic_information_chinese():
    global string_to_voice
    string_to_voice = string_to_voice + map_airport()
    string_to_voice = string_to_voice + "情报通播:" + map_letter_word(information_code) + ","
    string_to_voice = string_to_voice + string_handle(UTC_time) + "UTC。"

#中文运行信息语音生成函数
#input: NULL
#output: NULL
def speak_running_information_chinese():
    global string_to_voice
    if(ATIS_mode == atis_mode_dep):
        string_to_voice = string_to_voice + "起飞跑道:" + runway_handle() + ","
    elif(ATIS_mode == atis_mode_arr):
        string_to_voice = string_to_voice + "跑道:" + runway_handle() + ","
    string_to_voice = string_to_voice + runway_mode_handle() + "。"

#中文天气信息语音生成函数
#input: NULL
#output: NULL
def speak_weather_information_chinese():
    global string_to_voice
    #风向风速
    if(wind_speed == "00" or wind_speed == "0" or (len(wind_direction) == 0 and len(wind_speed) == 0)):
        string_to_voice = string_to_voice + "地面静风，"
    elif(wind_direction == "VRB" or wind_direction == "000" or \
         wind_direction == "00" or wind_direction == "0" or len(wind_direction) == 0):
        string_to_voice = string_to_voice + "地面不定风" + string_handle(wind_speed) + "米每秒，"
    else:
        string_to_voice = string_to_voice + "风向" + string_handle(wind_direction) + "度，风速" + string_handle(wind_speed) + "米每秒，"
    #风向变化
    if(len(wind_change) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "风向变化" + string_handle(string_input = wind_change, string_identify = (",",), string_replace = ("度到",)) + "度，"
    #云低高度
    if(len(cloud_height) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "云底高度" + number_handle(cloud_height) + "米，"
    #能见度
    if(len(visibility) == 0):
        pass
    else:
        if(visibility == "9999"):
            string_to_voice = string_to_voice + "能见度大于10公里，"
        elif(visibility == "CAVOK"):
            string_to_voice = string_to_voice + "开悟-OK，"
        else:
            string_to_voice = string_to_voice + "能见度" + number_handle(visibility) + "米，"
    #温度
    if(len(temperature) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "温度" + \
            string_handle(string_input = temperature, string_identify = ("-",), string_replace = ("零下",)) + "摄氏度，"
    #露点
    if(len(dew_point) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "露点" + \
            string_handle(string_input = dew_point, string_identify = ("-",), string_replace = ("零下",)) + "摄氏度，"
    #修正海压
    if(len(QNH) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "修正海压" + string_handle(QNH) + "百帕，"
    #过渡高度
    if(len(transition_altitude) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "过渡高度" + number_handle(transition_altitude) + "米，"
    #过渡高度层
    if(len(transition_level) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "过渡高度层" + number_handle(transition_level) + "米，"

#中文管制信息语音生成函数
#input: NULL
#output: NULL
def speak_control_information_chinese():
    global string_to_voice
    if(len(del_frequency) > 4 and len(del_frequency) < 8):
        if(ATIS_mode == atis_mode_dep):
            string_to_voice = string_to_voice + "放行频率" + \
                string_handle(string_input = del_frequency[0:len(del_frequency)], string_identify = ("."), string_replace = ("点"),) + ","
        elif(ATIS_mode == atis_mode_arr):
            string_to_voice = string_to_voice + "塔台频率" + \
                string_handle(string_input = del_frequency[0:len(del_frequency)], string_identify = ("."), string_replace = ("点"),) + ","  
    elif(len(del_frequency) == 0):
        pass
    else:
        error_handle(error_string_length_not_match)
    if(len(dep_frequency) > 4 and len(dep_frequency) < 8):
        if(ATIS_mode == atis_mode_dep):
            string_to_voice = string_to_voice + "离场频率" + \
                string_handle(string_input = dep_frequency[0:len(dep_frequency)], string_identify = (".",), string_replace = ("点",)) + ","
        elif(ATIS_mode == atis_mode_arr):
            string_to_voice = string_to_voice + "进近频率" + \
                string_handle(string_input = dep_frequency[0:len(dep_frequency)], string_identify = (".",), string_replace = ("点",)) + ","
    elif(len(dep_frequency) == 0):
        pass
    else:
        error_handle(error_string_length_not_match)
    string_to_voice = string_to_voice + "首次与管制员联络时报告您已收到通播" + map_letter_word(information_code) + "。"

#英文基本信息语音生成函数
#input: NULL
#output: NULL
def speak_basic_information_english():
    global string_to_voice
    string_to_voice = string_to_voice + map_airport(language = voice_language_english)
    string_to_voice = string_to_voice + "information:" + map_letter_word(information_code) + ","
    string_to_voice = string_to_voice + string_handle(string_input = UTC_time, language = voice_language_english) + "UTC。"

#英文运行信english
#input: NULL
#output: NULL
def speak_running_information_english():
    global string_to_voice
    if(ATIS_mode == atis_mode_dep):
        string_to_voice = string_to_voice + "departure runway:" + runway_handle(language = voice_language_english) + ","
    elif(ATIS_mode == atis_mode_arr):
        string_to_voice = string_to_voice + "runway:" + runway_handle(language = voice_language_english) + ","
    string_to_voice = string_to_voice + runway_mode_handle(language = voice_language_english) + "。"

#英文天气信息语音生成函数
#input: NULL
#output: NULL
def speak_weather_information_english():
    global string_to_voice
    #风向风速
    if(wind_speed == "00" or wind_speed == "0" or (len(wind_direction) == 0 and len(wind_speed) == 0)):
        string_to_voice = string_to_voice + "wind clam,"
    elif(wind_direction == "VRB" or wind_direction == "000" or \
         wind_direction == "00" or wind_direction == "0" or len(wind_direction) == 0):
        string_to_voice = string_to_voice + "wind variable " + string_handle(string_input = wind_speed, language = voice_language_english) + "meter per second，"
    else:
        string_to_voice = string_to_voice + "wind " + string_handle(string_input = wind_direction, language = voice_language_english) + "degree at " + string_handle(string_input = wind_speed, language = voice_language_english) + "meter per second，"
    #风向变化
    if(len(wind_change) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "wind vary from " + string_handle(string_input = wind_change, string_identify = (",",), string_replace = ("degree to ",), language = voice_language_english) + "degree，"
    #能见度
    if(len(visibility) == 0):
        pass
    else:
        if(visibility == "9999"):
            string_to_voice = string_to_voice + "visibility above ten thousand meters，"
        elif(visibility == "CAVOK"):
            string_to_voice = string_to_voice + "开悟-OK，"
        else:
            string_to_voice = string_to_voice + "visibility:" + number_handle(number_input = visibility, language = voice_language_english) + "meters,"
    #云低高度
    if(len(cloud_height) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "cloud height:" + number_handle(number_input = cloud_height, language = voice_language_english) + "meters，"
    #温度
    if(len(temperature) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "temperature:" + \
            string_handle(string_input = temperature, string_identify = ("-",), string_replace = ("minus ",), language = voice_language_english) + "centigrade，"
    #露点
    if(len(dew_point) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "dew point:" + \
            string_handle(string_input = dew_point, string_identify = ("-",), string_replace = ("minus ",), language = voice_language_english) + "centigrade，"
    #修正海压
    if(len(QNH) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "QNH:" + string_handle(string_input = QNH, language = voice_language_english) + "hectopascal，"
    #过渡高度
    if(len(transition_altitude) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "transition altitude:" + number_handle(number_input = transition_altitude, language = voice_language_english) + "meters，"
    #过渡高度层
    if(len(transition_level) == 0):
        pass
    else:
        string_to_voice = string_to_voice + "transition level:" + number_handle(number_input = transition_level, language = voice_language_english) + "meters，"

#英文管制信息语音生成函数
#input: NULL
#output: NULL
def speak_control_information_english():
    global string_to_voice
    if(len(del_frequency) > 4 and len(del_frequency) < 8):
        if(ATIS_mode == atis_mode_dep):
            string_to_voice = string_to_voice + "delivery frequency:" + \
                string_handle(string_input = del_frequency[0:len(del_frequency)], string_identify = ("."), string_replace = ("point ",), language = voice_language_english) + ","
        elif(ATIS_mode == atis_mode_arr):
            string_to_voice = string_to_voice + "tower frequency:" + \
                string_handle(string_input = del_frequency[0:len(del_frequency)], string_identify = ("."), string_replace = ("point ",), language = voice_language_english) + ","           
    elif(len(del_frequency) == 0):
        pass
    else:
        error_handle(error_string_length_not_match)
    if(len(dep_frequency) > 4 and len(dep_frequency) < 8):
        if(ATIS_mode == atis_mode_dep):
            string_to_voice = string_to_voice + "departure frequency:" + \
                string_handle(string_input = dep_frequency[0:len(dep_frequency)], string_identify = ("."), string_replace = ("point ",), language = voice_language_english) + ","
        elif(ATIS_mode == atis_mode_arr):
            string_to_voice = string_to_voice + "approach frequency:" + \
                string_handle(string_input = dep_frequency[0:len(dep_frequency)], string_identify = ("."), string_replace = ("point ",), language = voice_language_english) + ","
    elif(len(dep_frequency) == 0):
        pass
    else:
        error_handle(error_string_length_not_match)
    string_to_voice = string_to_voice + "advice on initial contact you have information:" + map_letter_word(information_code) + "。"

#声音播放部分------
#中文ATIS语音字符串添加函数
#input : NULL
#output: NULL
def speak_information_chinese():
    speak_basic_information_chinese() #将基本信息语音加入待转换语音字符串
    speak_running_information_chinese() #将运行信息语音加入待转换语音字符串
    speak_weather_information_chinese() #将天气信息语音加入待转换语音字符串
    speak_control_information_chinese() #将管制信息语音加入待转换语音字符串

#英文ATIS语音字符串添加函数
#input : NULL
#output: NULL
def speak_information_english():
    speak_basic_information_english() #将基本信息语音加入待转换语音字符串
    speak_running_information_english() #将运行信息语音加入待转换语音字符串
    speak_weather_information_english() #将天气信息语音加入待转换语音字符串
    speak_control_information_english() #将管制信息语音加入待转换语音字符串

#ATIS试听函数
#input: NULL
#output: NULL
def ATIS_audition():
    global string_to_voice
    global ATIS_voice_file_length
    string_to_voice = STRING_NULL #清空待转换语音字符串
    speak_information_chinese()
    speak_information_english()
    engine.say(string_to_voice) #将语音任务加入队列
    engine.runAndWait() #执行队列

def ATIS_to_file():
    global string_to_voice
    global ATIS_voice_file_length
    string_to_voice = STRING_NULL #清空待转换语音字符串
    speak_information_chinese()
    speak_information_english()
    engine.save_to_file(string_to_voice, voice_output_dir + voice_output_name) #将语音任务加入队列    
    engine.runAndWait() #播放队列
    ATIS_voice_file_length = librosa.get_duration(filename = voice_output_dir + voice_output_name)
    print("音频时长修改为",int(ATIS_voice_file_length),"秒")
#=============================================

#operation#===================================
engine = pyttsx3.init() #初始化语音库
engine.setProperty('rate', voice_rate) # setting up new voice rate
engine.setProperty('volume', voice_volume) # setting up volume level  between 0 and 1
voices = engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[voice_gender].id) #changes voices. 0 for male, 1 for female
#engine.runAndWait() #用于测试
#=============================================

def set_ATIS_voice_engine_volume(value):
    global ATIS_voice_volume
    global engine
    ATIS_voice_volume = float(value)
    engine.setProperty('volume', ATIS_voice_volume / 100) # setting up volume level  between 0 and 1

def set_ATIS_voice_engine_rate(value):
    global ATIS_voice_rate
    global engine
    ATIS_voice_rate = value
    engine.setProperty('rate', ATIS_voice_rate)
