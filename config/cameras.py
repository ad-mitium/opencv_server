camera_list = {
    '1':'http://192.168.0.123:81/stream' ,
    '2':'http://192.168.0.124:81/stream' ,
    '3':'http://192.168.0.125:81/stream' ,
    '4':'http://192.168.0.126:81/stream'
}

# Only change these if your device supports it

ae_level = ['-2','-1','0','1','2']  

framesize = ['11','9']  # 1280x720, 800x600

hor_mirror = ['1']   # Set horizontal mirror on
vert_flip = ['1']   # Set vertical flip on
black_point = ['1']   # Set black point correction on
white_balance = ['1']   # Set to sunny white balance

special_effect = ['0','2']  #Set special effect to None or Gray scale

quality = ['4']     # Set image quality to best

aec = ['1']     # Enable auto exposure compensation
gain_ceiling = ['0','1','2']    # Range for AEC gain
dcw = ['0']
