#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023
 
import requests

def check_debug_status():
    if session['enabled_debug'] == False:
        verbose = debug_level['0']
        # print ('INFO: Debug level set to: ',verbose,' and session is: ',session['enabled_debug'])
        # print (f'Session data:\n    ',session)
    else:
        verbose = debug_level['1']
        print ('DEBUG: Debug level set to ',verbose,' and session is: ',session['enabled_debug'])
        print (f'DEBUG:   Session data:\n         ',session)
    return verbose


def strip_url(url): 
    from urllib.parse import urlparse

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])

    parts = urlparse(url)
    domain_addr = parts.scheme + '://' + parts.netloc.split(':')[0] 
    if verbose == 'DEBUG':
        print ('DEBUG: Camera IP address: ',domain_addr)
    return domain_addr

def set_ae_exposure(ae_dir): 
    from time import sleep

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])

    if not session['camera_id'] == 'stop':
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        print('INFO: Curent ae_level: ',session['ae_level'],' direction: ', ae_dir,' New ae_level: ', end=' ')
        
        if ae_dir == '0':
            ae_val = '0'
        else:
            ae_val = int(session['ae_level']) + int(ae_dir)
        
        # if verbose == 'DEBUG':
            # print ('DEBUG: AE val: ',ae_val, end=' ') 
            # print(type(ae_val) , type(session['ae_level']))
        
        if str(ae_val) in ae_level_range:
            url = url_stripped + '/control?var=ae_level&val='+str(ae_val)
            session['ae_level'] = str(ae_val)
            print (ae_val)
            # if verbose == 'DEBUG':
            #     print('DEBUG:  URL: ',url,' level: ',session['ae_level'], end='')
            get_request = requests.get(url)
            get_status_code = get_request.status_code
            # if verbose == 'DEBUG':
            #     print (' status code: ',get_request.status_code)
        else:
            print (f'\nERROR: Value out of range: ',ae_val, end=' ')
            url = 'No request made, AE value out of range ' # No url if you don't make a request
            get_status_code = 'No request made, AE value out of range ' # No status code if you don't make a request
            if ae_val > 2:      # Put ae_val back in range for DEBUG display purposes, wasn't changed in session['ae_level']
                ae_val = 2
            elif ae_val < -2:
                ae_val = -2
            if verbose == 'DEBUG':
                print(f'\nDEBUG:  AE level reset to: ',ae_val)
            else:
                print(' AE level reset to: ',ae_val)


        if verbose == 'DEBUG':
            print ("DEBUG: AE set to: ",ae_val,' URL: ',url, ' level: ',session['ae_level'],' status code: ',get_status_code) 
        # sleep(2)

def set_black_point(bpc_mode): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])

    url = url_stripped + '/control?var=bpc&val='+str(bpc_mode)
    get_request = requests.get(url)
    if verbose == 'DEBUG':
        print ("DEBUG: Black point correction set to: ",bpc_mode, end=' ')
        print (' status code: ',get_request.status_code)

def set_flip_image(mirror_mode): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])

    hmirror_adjust = url_stripped + '/control?var=hmirror&val='+str(mirror_mode)
    get_request = requests.get(hmirror_adjust)
    if verbose == 'DEBUG':
        print ('DEBUG: Horizontal mirror: ',get_request.status_code, end=' ')

    vfliup_adjust = url_stripped + '/control?var=vflip&val='+str(mirror_mode)
    get_request = requests.get(vfliup_adjust)
    if verbose == 'DEBUG':
        print ('Vertical flip: ',get_request.status_code)
        print ("DEBUG: Image mirror set to: ",mirror_mode)

def set_frame_size(frame_size): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])

    url = url_stripped + '/control?var=framesize&val='+str(frame_size)
    get_request = requests.get(url)
    if verbose == 'DEBUG':
        print ("DEBUG: Frame size set to: ",frame_size, "Resolution: ", end=' ')
        if frame_size == '11':
            print('1280 x 720', end=' ')
        else:
            print('800 x 600', end=' ')
        print (' status code: ',get_request.status_code)

def set_white_balance(wb_mode): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])

    url = url_stripped + '/control?var=wb_mode&val='+str(wb_mode)
    get_request = requests.get(url)
    if verbose == 'DEBUG':
        print ("DEBUG: WB set to: ",wb_mode, end=' ')
        print (' status code: ',get_request.status_code)

def get_frames(cam_id,stop_capture=False): 
    import cv2

    video = cv2.VideoCapture(cam_list[str(cam_id)])

    while True:
        success, frame = video.read()
        if not success:
            print('ERROR: Error getting video frame')
            break
        elif stop_capture:
            video.ReleaseCapture()
            break
        else:
            ret_status, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    import sys
    from sessions import session
    sys.path.append('config')   # allows for finding ffmpeg_options.py
    from cameras import camera_list as cam_list
    from cameras import ae_level as ae_level_range
    from cameras import framesize, white_balance
    from network import host
    from network import debug_level
    import network as network

    verbose = check_debug_status()
    print (verbose, session['enabled_debug'])
    # print (verbose)

else:
    from lib.sessions import session
    from config.cameras import camera_list as cam_list
    from config.cameras import ae_level as ae_level_range
    from config.cameras import framesize, white_balance
    from config.network import host
    from config.network import debug_level
    import config.network as network

    verbose = check_debug_status()
    # print (verbose, session['enabled_debug'])
    # print (verbose)
