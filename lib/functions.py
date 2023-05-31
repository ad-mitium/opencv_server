#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023
 
import requests

def check_debug_status(print_session=True):
    if session['enabled_debug'] == False:
        show_debug_info = debug_level['0']
        # print ('INFO: Debug level set to: ',show_debug_info,' and session is: ',session['enabled_debug'])
        # print (f'Session data:\n    ',session)
    else:
        show_debug_info = debug_level['1']
        print ('DEBUG: Debug level set to ',show_debug_info,' and session is: ',session['enabled_debug'])
        if print_session:
            print_session_data()
    return show_debug_info

def print_session_data():
    print (f'DEBUG:   Session data:\n         ',session)
    return 0

def set_defaults(cam_id, reset=False, show_debug_info = False):     # Handles initialization and reset
    show_debug_info = check_debug_status(False)

    if show_debug_info == 'DEBUG': 
        print ('DEBUG: Set Defaults Cam ID: ',cam_id, end=' ')

    if reset:
        session.update(ae_level=sess_defaults['0'][0],bpc=sess_defaults['0'][1],fs_size=sess_defaults['0'][2],
            white_balance=sess_defaults['0'][3])  # Change all declared values to default values 
        sess_defaults[cam_id]=sess_defaults['0']
        if show_debug_info == 'DEBUG': 
            print (f'\n','RESET:   Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id], end=' ')
    else:
        session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
            white_balance=sess_defaults[cam_id][3])  # Change all declared values to default values 

    if show_debug_info == 'DEBUG':      # follow on for previious print statement
        print ('AE Val: ',session['ae_level'],'AE Dir: ', session['ae_direction'] )

    if show_debug_info == 'DEBUG': 
        if reset: 
            print('DEBUG: Resetting stream to default values')
        else:
            print('DEBUG: Changing stream to previous values')
        print_session_data()
        print ('DEBUG:   Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
    else:
        print('INFO: Stream has been reset to default values')

    set_ae_exposure(session['ae_level']) # <--- This causes exposure creep
    set_black_point(session['bpc'])
    set_frame_size(session['fs_size'])
    set_white_balance(session['white_balance'])
    return show_debug_info

def update_cam(cam_id, reset=False, show_debug_info = False):   # Handles updating changed values
    # show_debug_info = check_debug_status(False)

    # print ('Update Cam: ',show_debug_info)
    if show_debug_info == 'DEBUG': 
        print ('DEBUG: Updating Cam ID: ',cam_id, end=' ')

    session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
        white_balance=sess_defaults[cam_id][3])  # Change all declared values to default values 

    if show_debug_info == 'DEBUG':  # Follow on for previous print statement
        print ('AE Val: ',session['ae_level'],'AE Dir: ', session['ae_direction'] )

    # show_debug_info = check_debug_status(False)

    if show_debug_info == 'DEBUG': 
        print('DEBUG: Changing stream to previous values')
        print_session_data()
        print ('DEBUG:   Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
    else:
        print('INFO: Stream has been reset to default values')

    set_ae_exposure(None,session['ae_level'],show_debug_info) # None forces a "set level" instead of changing exposure direction
    set_black_point(session['bpc'],show_debug_info)
    set_frame_size(session['fs_size'],show_debug_info)
    set_white_balance(session['white_balance'],show_debug_info)
    return show_debug_info

def write_session_data(cam_id, ae_val, bpc_mode, frame_size, wb_mode, show_debug_info = False):
    if show_debug_info == 'DEBUG': 
        print ('DEBUG: Write session data: AE Val: ',ae_val,' Cam ID: ',cam_id)
    sess_defaults[cam_id][0], sess_defaults[cam_id][1], sess_defaults[cam_id][2], sess_defaults[cam_id][3] = ae_val, bpc_mode, frame_size, wb_mode

    if show_debug_info == 'DEBUG': 
        print('DEBUG: Writing camera session values')
        print ('DEBUG:   Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
        # print (f'DEBUG:   Camera session data:\n         ',sess_defaults)    
    # else:
    #     print('INFO: Stream has been reset to default values')

    return 0

def get_session_data(cam_id, ae_val, bpc_mode, frame_size, wb_mode, show_debug_info = False):
    # session.update(ae_direction=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
    #     white_balance=sess_defaults[cam_id][3])  

    if show_debug_info == 'DEBUG': 
        print('DEBUG: Getting camera session values')
        print ('DEBUG:   Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
    # else:
    #     print('INFO: Stream has been reset to default values')

    return 0


def strip_url(url, show_debug_info = False): 
    from urllib.parse import urlparse

    # show_debug_info = check_debug_status()
    # print (show_debug_info, session['enabled_debug'])

    parts = urlparse(url)
    domain_addr = parts.scheme + '://' + parts.netloc.split(':')[0] 
    if show_debug_info == 'DEBUG':
        print ('DEBUG: Camera IP address: ',domain_addr)
    return domain_addr

def set_ae_exposure(ae_dir, ae_val = 'NaN',show_debug_info = False): 
    from time import sleep

    # show_debug_info = check_debug_status()
    # print (show_debug_info, session['enabled_debug'])
    if show_debug_info == 'DEBUG': 
        print ("DEBUG: IN AE: Camera ID: " ,session['camera_id'])

    if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        print('INFO: Curent ae_level: ',session['ae_level'],' direction: ', ae_dir, end=' ')
        if ae_dir == '0':
            ae_val = '0'
        elif ae_dir == None:    # Force an overwrite of AE level instead of direction change
            if type(ae_val) == int:    # ae_val is now assigned a value provided during function call
                print(f'\nINFO: Force set AE value to: ', ae_val, end=' ')
            else:
                print(f'\nERROR: ae_val is NaN', ae_val, type(ae_val), end=' ')
                ae_val = int(ae_val)
        else:
            ae_val = int(session['ae_level']) + int(ae_dir)
        
        if str(ae_val) in ae_level_range:
            url = url_stripped + '/control?var=ae_level&val='+str(ae_val)
            session['ae_level'] = str(ae_val)
            print (' New ae_level: ',ae_val)      # Part of previous INFO output
            # if show_debug_info == 'DEBUG':
            #     print('DEBUG:  URL: ',url,' level: ',session['ae_level'], end='')
            get_request = requests.get(url)
            get_status_code = get_request.status_code
            # if show_debug_info == 'DEBUG':
            #     print (' status code: ',get_request.status_code)
        else:
            print (f'\nERROR: Value out of range: ',ae_val, end=' ')
            url = 'No request made, AE value out of range ' # No url if you don't make a request
            get_status_code = 'No request made, AE value out of range ' # No status code if you don't make a request
            if ae_val > 2:      # Put ae_val back in range for DEBUG display purposes, wasn't changed in session['ae_level']
                ae_val = 2
            elif ae_val < -2:
                ae_val = -2
            if show_debug_info == 'DEBUG':
                print(f'\nDEBUG:  AE level reset to: ',ae_val)
                print_session_data()
            else:
                print(' AE level reset to: ',ae_val)

        if show_debug_info == 'DEBUG': 
            print ("DEBUG: IN AE, AFTER REQUEST SENT: Camera ID: " ,session['camera_id'])

        write_session_data(session['camera_id'], ae_val, session['bpc'], session['fs_size'], session['white_balance'], show_debug_info)

        if show_debug_info == 'DEBUG':
            print ("DEBUG: AE set to: ",ae_val,' URL: ',url, ' level: ',session['ae_level'],' status code: ',get_status_code) 
        # sleep(2)
    # else:
    #     print('INFO: Status is: ',session['camera_id'])

def set_black_point(bpc_mode, show_debug_info = False): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    # show_debug_info = check_debug_status()
    # print (show_debug_info, session['enabled_debug'])

    if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
        url = url_stripped + '/control?var=bpc&val='+str(bpc_mode)
        get_request = requests.get(url)
        if show_debug_info == 'DEBUG':
            print ("DEBUG: Black point correction set to: ",bpc_mode, end=' ')
            print (' status code: ',get_request.status_code)
            print_session_data()
        write_session_data(session['camera_id'], session['ae_level'], bpc_mode, session['fs_size'], session['white_balance'], show_debug_info)

def set_flip_image(mirror_mode, show_debug_info = False): 
    if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        # show_debug_info = check_debug_status()
        # print (show_debug_info, session['enabled_debug'])

        hmirror_adjust = url_stripped + '/control?var=hmirror&val='+str(mirror_mode)
        get_request = requests.get(hmirror_adjust)
        if show_debug_info == 'DEBUG':
            print ('DEBUG: Horizontal mirror: ',get_request.status_code, end=' ')

        vfliup_adjust = url_stripped + '/control?var=vflip&val='+str(mirror_mode)
        get_request = requests.get(vfliup_adjust)
        if show_debug_info == 'DEBUG':
            print ('Vertical flip: ',get_request.status_code)
            print ("DEBUG: Image mirror set to: ",mirror_mode)
            print_session_data()

def set_frame_size(frame_size, show_debug_info = False): 
    if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        # show_debug_info = check_debug_status()
        # print (show_debug_info, session['enabled_debug'])

        url = url_stripped + '/control?var=framesize&val='+str(frame_size)
        get_request = requests.get(url)
        if show_debug_info == 'DEBUG':
            print ("DEBUG: Frame size set to: ",frame_size, " Resolution: ", end=' ')
            if frame_size == '11':
                print('1280 x 720', end=' ')
            else:
                print('800 x 600', end=' ')
            print (' status code: ',get_request.status_code)
            print_session_data()
        write_session_data(session['camera_id'], session['ae_level'], session['bpc'], frame_size, session['white_balance'], show_debug_info)

def set_white_balance(wb_mode, show_debug_info = False): 
    if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        # show_debug_info = check_debug_status()
        # print (show_debug_info, session['enabled_debug'])

        url = url_stripped + '/control?var=wb_mode&val='+str(wb_mode)
        get_request = requests.get(url)
        if show_debug_info == 'DEBUG':
            print ("DEBUG: WB set to: ",wb_mode, end=' ')
            print (' status code: ',get_request.status_code)
            print_session_data()
        write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], wb_mode, show_debug_info)

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
    from sessions import session, sess_defaults
    sys.path.append('config')   # allows for finding ffmpeg_options.py
    from cameras import camera_list as cam_list
    from cameras import ae_level as ae_level_range
    from cameras import framesize, white_balance
    from network import host
    from network import debug_level
    import network as network

    show_debug_info = check_debug_status()
    print (show_debug_info, session['enabled_debug'])

else:
    from lib.sessions import session, sess_defaults
    from config.cameras import camera_list as cam_list
    from config.cameras import ae_level as ae_level_range
    from config.cameras import framesize, white_balance
    from config.network import host
    from config.network import debug_level
    import config.network as network

    # show_debug_info = check_debug_status()
    # print (show_debug_info, session['enabled_debug'])
    # print (show_debug_info)
