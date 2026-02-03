#author#======================================
#file:DEFINE.py
#wangxiaochen CFR7445 2022.01.14
#=============================================
#  File: DEFINE.py
#  Copyright (c) 2026 MasterGui All rights reserved.
#  2026/2/3 23:27


#import libraries
import os
#=============================================

#key value define#============================
#软件配置------
software_verion = "0.9.9-Beta" #软件版本
software_title = "ATIS Generator (Ver " + software_verion + ") BY CFR7445" #设置软件名称
software_dir = os.getcwd() #获取软件绝对路径
# software_icon_path = software_dir + "\image\icon.ico" #设置软件图标
software_icon_path = "..\image\icon.ico" #设置软件图标
software_windows_size = "600x620" #设置初始窗口大小
#界面配置-----
gui_headline_pady = 20 #标题栏纵向间隔
gui_option_padx = 15 #选项框横向间隔
gui_option_pady = 5 #选项框纵向间隔
gui_combobox_width = 6 #多功能框宽度
gui_entry_width = 9 #输入框宽度
gui_button_width = 9 #按钮宽度
gui_button_pady = 25 #按钮纵向间隔
gui_button_padx = 8 #按钮横向间隔
gui_information_part_xsize = 600 #信息填写部分容器宽度
gui_information_part_ysize = 500 #信息填写部分容器高度
gui_button_part_xsize = 600 #按钮部分容器宽度
gui_button_part_ysize = 100 #按钮部分容器高度
gui_message_part_xsize = 550 #信息输出部分容器宽度
gui_message_part_ysize = 50 #信息输出容器高度
gui_frame_borderwidth = 0 #测试用，正常运行设为0
#语音配置------
voice_gender = 0 #声音选择，0 for male, 1 for female
voice_rate = 130 #音速设置，范围
voice_volume = 1.0 #音量设置，范围0~1
ATIS_broadcast_interval = 3 #秒
voice_language_chinese = 0
voice_language_english = 1
voice_output_dir = "output/mp3/"
voice_output_name = "ATIS.mp3"
#通播模式定义------
atis_mode_arr = 0 #进场通播模式
atis_mode_dep = 1 #离场通播模式
#常用量定义------
STRING_NULL = "" #空字符串
TRUE = 1
FALSE = 0
#定时器定义------
universal_timer_count_maximum = 360
#=============================================
