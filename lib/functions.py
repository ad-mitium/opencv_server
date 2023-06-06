#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023
 
import requests

def check_debug_status(print_session=True):
    if session['enabled_debug'] == False:
        show_debug_info = debug_level['0']
        # print ('INFO:   Debug level set to: ',show_debug_info,' and session is: ',session['enabled_debug'])
        # print (f'Session data:\n    ',session)
    else:
        show_debug_info = debug_level['1']
        print ('DEBUG:   Debug level set to ',show_debug_info,' and session is: ',session['enabled_debug'])
        if print_session:
            print_session_data()
    return show_debug_info

def print_session_data():
    print (f'DEBUG:     Session data:\n         ',session)
    return 0

def initialize_cams(show_debug_info=False):
    if show_debug_info == 'DEBUG': 
        print ('DEBUG:   Initializing cameras...')
        # print (session,f'\n',sess_defaults)
    for cam_id in sess_defaults.keys():
        session['camera_id']=cam_id     # Change camera ID or you'll overwrite the same one over and over
        session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
            white_balance=sess_defaults[cam_id][3],flip=sess_defaults[cam_id][4],ae_compensation=sess_defaults[cam_id][5],
            gain_ceiling=sess_defaults[cam_id][6],quality=sess_defaults[cam_id][7])  # Change all declared values to default values 
        if show_debug_info == 'DEBUG': 
            if not cam_id == '0':       # Don't show '0', as it is not being written
                print ('DEBUG:   Defaults set for Cam ID: ',cam_id)
            # print ('         ',session)
        if not cam_id == '0':       # Don't overwrite default values
            set_ae_exposure(None,int(session['ae_level']),show_debug_info,True) 
            set_black_point(session['bpc'])
            set_frame_size(session['fs_size'])
            set_white_balance(session['white_balance'])
            set_flip_image(session['flip'])
            set_aec(session['ae_compensation'])
            set_gain_ceiling(session['gain_ceiling'])
            set_quality(session['quality'])
            if not cam_id == '0':
                write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'])
                if show_debug_info == 'DEBUG':
                    print ('DEBUG:   Initial writing of session defaults completed for Camera: ', cam_id)
    if show_debug_info == 'DEBUG': 
        print ('DEBUG:   Cameras initialized',f'\n',sess_defaults)
    else:
        print('INFO:   Stream for Cameras have been initialized to default values')


def set_defaults(cam_id, reset=False, show_debug_info = False):     # Handles initialization and reset
    show_debug_info = check_debug_status(False)

    if show_debug_info == 'DEBUG': 
        print ('DEBUG:   Set Defaults Cam ID: ',cam_id, end='')

    if reset:
        session.update(ae_level=sess_defaults['0'][0],bpc=sess_defaults['0'][1],fs_size=sess_defaults['0'][2],
            white_balance=sess_defaults['0'][3],flip=sess_defaults[cam_id][4],ae_compensation=sess_defaults[cam_id][5],
            gain_ceiling=sess_defaults[cam_id][6],quality=sess_defaults[cam_id][7])  # Change all declared values to default values 
        sess_defaults[cam_id]=sess_defaults['0']
        if show_debug_info == 'DEBUG': 
            print (f'\r')
            print ('RESET:   Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
    else:
        session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
            white_balance=sess_defaults[cam_id][3])  # Change all declared values to default values 

    if show_debug_info == 'DEBUG':      # follow on for previious print statement, suppressed when reset
        if not reset:
            print (' AE Val: ',session['ae_level'],'AE Dir: ', session['ae_direction'] )

    if show_debug_info == 'DEBUG': 
        if reset: 
            print('DEBUG:    Resetting stream to default values')
        else:
            print('DEBUG:    Changing stream to previous values')
        print_session_data()
        print ('DEBUG:    Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
    # else:
    #     print('INFO:    Stream has been reset to default values')

    set_ae_exposure(None,int(session['ae_level']),show_debug_info,True) 
    set_black_point(session['bpc'])
    set_frame_size(session['fs_size'])
    set_white_balance(session['white_balance'])
    set_flip_image(session['flip'])
    set_aec(session['ae_compensation'])
    set_gain_ceiling(session['gain_ceiling'])
    set_quality(session['quality'])

    if reset: 
        print('INFO:    Stream for Camera {} has been reset to default values'.format(cam_id))
    else:
        print('INFO:    Stream for Camera {} has been changed to previous values'.format(cam_id))

    return show_debug_info

def update_cam(cam_id, reset=False, show_debug_info = False):   # Handles updating changed values
    if not cam_id == '0':
        # show_debug_info = check_debug_status(False)

        # print ('Update Cam: ',show_debug_info)
        if show_debug_info == 'DEBUG': 
            if not cam_id == 'Multi':
                print ('DEBUG:   Updating Cam ID: ',cam_id)
            else:
                print ('DEBUG:   Updating multiple Cam IDs')

        if not cam_id == 'Multi':
            session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
                white_balance=sess_defaults[cam_id][3],flip=sess_defaults[cam_id][4],ae_compensation=sess_defaults[cam_id][5],
                    gain_ceiling=sess_defaults[cam_id][6],quality=sess_defaults[cam_id][7])  # Change all declared values to default values 
        else:       # Make updates for multiple views
            for cam_id in sess_defaults.keys():
                if not cam_id == '0': 
                    if not cam_id == 'Multi':       # Don't overwrite default values
                        session['camera_id']=cam_id     # Change camera ID or you'll overwrite the same one over and over
                        session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
                            white_balance=sess_defaults[cam_id][3],flip=sess_defaults[cam_id][4],ae_compensation=sess_defaults[cam_id][5],
                            gain_ceiling=sess_defaults[cam_id][6],quality=sess_defaults[cam_id][7])  # Change all declared values to default values 
                        if show_debug_info == 'DEBUG': 
                            print ('DEBUG:   Previous settings loaded for Cam ID: ',cam_id, sess_defaults[cam_id])
                            # print ('         ',session)
                        set_ae_exposure(None,int(session['ae_level']),show_debug_info,True) 
                        set_black_point(session['bpc'])
                        set_frame_size('11')
                        set_white_balance(session['white_balance'])
                        set_flip_image(session['flip'])
                        set_aec(session['ae_compensation'])
                        set_gain_ceiling(session['gain_ceiling'])
                        set_quality(session['quality'])
                        write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'])
                    if show_debug_info == 'DEBUG':
                        print ('DEBUG:   Initial writing of session defaults completed for Camera: ', cam_id)
                else:
                    print('ERROR:  Cannot update Camera ID ',cam_id)
            print(sess_defaults)

        if show_debug_info == 'DEBUG':  # Follow on for previous print statement
            if not cam_id == 'Multi' or not cam_id == '0':
                print ('AE Val: ',session['ae_level'],'AE Dir: ', session['ae_direction'] )

        if show_debug_info == 'DEBUG': 
            print('DEBUG:   Changing stream to previous values')
            print_session_data()
            if not cam_id == 'Multi':
                print ('DEBUG:     Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])

        set_ae_exposure(None,int(session['ae_level']),show_debug_info) # None forces a "set level" instead of changing exposure direction
        set_black_point(session['bpc'],show_debug_info)
        set_frame_size(session['fs_size'],show_debug_info)
        set_white_balance(session['white_balance'],show_debug_info)
        set_flip_image(session['flip'],show_debug_info)
        set_aec(session['ae_compensation'])
        set_gain_ceiling(session['gain_ceiling'])
        set_quality(session['quality'])

        print('INFO:    Stream for Camera {} has been updated'.format(cam_id))
    else:
        print('ERROR:  Cannot update Camera ID ',cam_id)

    return show_debug_info

def write_session_data(cam_id, ae_val, bpc_mode, frame_size, wb_mode, flip, show_debug_info = False):
    if not cam_id == '0':    # Never overwrite '0'
        if show_debug_info == 'DEBUG': 
            print ('DEBUG:   Write session data: AE Val: ',ae_val,' Cam ID: ',cam_id)
        sess_defaults[cam_id][0], sess_defaults[cam_id][1], sess_defaults[cam_id][2], sess_defaults[cam_id][3], sess_defaults[cam_id][4] = ae_val, bpc_mode, frame_size, wb_mode, flip

        if show_debug_info == 'DEBUG': 
            print('DEBUG:   Writing camera session values')
            print ('DEBUG:     Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
            # print (f'DEBUG:     Camera session data:\n         ',sess_defaults)    
        # else:
        #     print('INFO:    Stream has been reset to default values')
    else:
        print('ERROR:  Cannot overwrite default values for ID ',cam_id)
    return 0

def get_session_data(cam_id, ae_val, bpc_mode, frame_size, wb_mode, show_debug_info = False):
    # session.update(ae_direction=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
    #     white_balance=sess_defaults[cam_id][3])  

    if show_debug_info == 'DEBUG': 
        print('DEBUG:   Getting camera session values')
        print ('DEBUG:     Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
    # else:
    #     print('INFO:    Stream has been reset to default values')

    return 0

def strip_url(url, show_debug_info = False): 
    from urllib.parse import urlparse

    # show_debug_info = check_debug_status()
    # print (show_debug_info, session['enabled_debug'])

    parts = urlparse(url)
    domain_addr = parts.scheme + '://' + parts.netloc.split(':')[0] 
    if show_debug_info == 'DEBUG':
        print ('DEBUG:   Camera IP address: ',domain_addr)
    return domain_addr

def send_url_command(url,show_debug_info = False):
    # import urllib3

    try:
        get_request = requests.get(url,timeout=5)   # Increase timeout to 5 seconds
        if get_request.status_code == 200:
            get_status_code = get_request.status_code
        if show_debug_info == 'DEBUG':
            print (' status code: ',get_status_code)
        get_request.raise_for_status()
    except requests.exceptions.Timeout:
        print()
        print('ERROR:   GET request has timed out')
        get_status_code = 'Timeout'
    # except urllib3.exceptions.NewConnectionError:
    #    print()
    #     print('ERROR:   GET request could not find host: ',url)
    #     get_status_code = 'No host' 
    # except urllib3.connection.HTTPConnection:
    #    print()
    #     print('ERROR:   GET request could not connect to host: ',url)
    #     get_status_code = 'ConnError' 
    except requests.exceptions.ConnectionError:
        print()
        print('ERROR:   GET request unable to connect to host: ',url)
        get_status_code = 'ConnError'
    finally:
        pass
    return get_status_code

def set_ae_exposure(ae_dir, ae_val = 'NaN',show_debug_info = False, suppress = False): 
    # from time import sleep
    if not session['camera_id'] == '0':    # Never go to '0'

        # show_debug_info = check_debug_status()
        # print (show_debug_info, session['enabled_debug'])
        if show_debug_info == 'DEBUG': 
            print ("DEBUG:     IN AE: Camera ID: " ,session['camera_id'])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            if show_debug_info == 'DEBUG':
                print('DEBUG:     Curent ae_level: ',session['ae_level'],' direction: ', ae_dir, end='')
            elif not suppress:
                print('INFO:      Curent ae_level: ',session['ae_level'],' direction: ', ae_dir, end='')
            if ae_dir == '0':
                ae_val = '0'
            elif ae_dir == None:    # Force an overwrite of AE level instead of direction change
                if type(ae_val) == int:    # ae_val is now assigned a value provided during function call
                    if show_debug_info == 'DEBUG':
                        print(f'\r')
                        print('DEBUG:     Camera has changed: {} Force set AE value to: '.format(session['camera_id']), ae_val, end='')
                    elif not suppress:
                        print(f'\r')
                        print('INFO:      Camera has changed: Force set AE value to: ', ae_val, end='')
                else:
                    print(f'\r')
                    print('ERROR:   ae_val is NaN', ae_val, type(ae_val), end='')
                    ae_val = int(ae_val)
            else:
                ae_val = int(session['ae_level']) + int(ae_dir)
            
            if str(ae_val) in ae_level_range:
                url = url_stripped + '/control?var=ae_level&val='+str(ae_val)
                session['ae_level'] = str(ae_val)
                print ('  New ae_level: ',ae_val,end='')      # Part of previous INFO output
                # if show_debug_info == 'DEBUG':
                #     print('DEBUG:     URL: ',url,' level: ',session['ae_level'], end='')

                status_code = send_url_command(url,show_debug_info)

                if not show_debug_info == 'DEBUG':
                    print()     # Force newline
            else:
                print (f'\rERROR:   Value out of range: ',ae_val, end=' ')
                url = 'No request made, AE value out of range ' # No url if you don't make a request
                get_status_code = 'No request made, AE value out of range ' # No status code if you don't make a request
                if ae_val > 2:      # Put ae_val back in range for DEBUG display purposes, wasn't changed in session['ae_level']
                    ae_val = 2
                elif ae_val < -2:
                    ae_val = -2
                if show_debug_info == 'DEBUG':
                    print(f'\r','DEBUG:     AE level reset to: ',ae_val)
                    print_session_data()
                else:
                    print(' AE level reset to: ',ae_val)

            if show_debug_info == 'DEBUG': 
                print ("DEBUG:     IN AE, AFTER REQUEST SENT: Camera ID: " ,session['camera_id'])

            if show_debug_info == 'DEBUG':
                print ("DEBUG:     AE set to: ",ae_val,' URL: ',url, ' level: ',session['ae_level'],' status code: ',status_code) 
            write_session_data(session['camera_id'], ae_val, session['bpc'], session['fs_size'], session['white_balance'], session['flip'], show_debug_info)

            # sleep(2)
        # else:
        #     print('INFO:      Status is: ',session['camera_id'])

def set_black_point(bpc_mode, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        # show_debug_info = check_debug_status()
        # print (show_debug_info, session['enabled_debug'])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=bpc&val='+str(bpc_mode)
            status_code = send_url_command(url,show_debug_info)
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Black point correction set to: ",bpc_mode, end=' ')
                print (' status code: ',status_code)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], bpc_mode, session['fs_size'], session['white_balance'], session['flip'], show_debug_info)

def set_flip_image(mirror_mode, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            # show_debug_info = check_debug_status()
            # print (show_debug_info, session['enabled_debug'])

            hmirror_adjust_url = url_stripped + '/control?var=hmirror&val='+str(mirror_mode)
            h_status_code = send_url_command(hmirror_adjust_url,show_debug_info)
            # get_request = requests.get(hmirror_adjust)
            if show_debug_info == 'DEBUG':
                print ('DEBUG:     Image flip: Horizontal mirror: ',h_status_code, end=' ')

            vfliup_adjust_url = url_stripped + '/control?var=vflip&val='+str(mirror_mode)
            v_status_code = send_url_command(vfliup_adjust_url,show_debug_info)
            # get_request = requests.get(vfliup_adjust)
            if show_debug_info == 'DEBUG':
                print (' Vertical flip: ',v_status_code)
                print ('DEBUG:   Cam ID: ',session['camera_id'],' Image mirror set to: ',mirror_mode)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'],mirror_mode, show_debug_info)

def set_frame_size(frame_size, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            # show_debug_info = check_debug_status()
            # print (show_debug_info, session['enabled_debug'])

            url = url_stripped + '/control?var=framesize&val='+str(frame_size)
            status_code = send_url_command(url,show_debug_info)
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Frame size set to: ",frame_size, " Resolution: ", end=' ')
                if frame_size == '11':
                    print('1280 x 720', end=' ')
                else:
                    print('800 x 600', end=' ')
                print (' status code: ',status_code)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], frame_size, session['white_balance'], session['flip'], show_debug_info)

def set_white_balance(wb_mode, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            # show_debug_info = check_debug_status()
            # print (show_debug_info, session['enabled_debug'])

            url = url_stripped + '/control?var=wb_mode&val='+str(wb_mode)
            status_code = send_url_command(url,show_debug_info)
            if show_debug_info == 'DEBUG':
                print ("DEBUG:    White Balance set to: ",wb_mode, end=' ')
                print (' status code: ',status_code)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], wb_mode, session['flip'], show_debug_info)

def set_gain_ceiling(gain_ceiling, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        # show_debug_info = check_debug_status()
        # print (show_debug_info, session['enabled_debug'])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=gainceiling&val='+str(gain_ceiling)
            status_code = send_url_command(url,show_debug_info)
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Gain ceiling set to: ",gain_ceiling, end=' ')
                print (' status code: ',status_code)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'], show_debug_info)

def set_aec(ae_compensation, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=aec&val='+str(ae_compensation)
            status_code = send_url_command(url,show_debug_info)
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Auto exposure compensation set to: ",ae_compensation, end=' ')
                print (' status code: ',status_code)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'], show_debug_info)

def set_quality(quality, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=quality&val='+str(quality)
            status_code = send_url_command(url,show_debug_info)
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Image quality is set to: ",quality, end=' ')
                print (' status code: ',status_code)
                print_session_data()
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'], show_debug_info)

def get_frames(cam_id,stop_capture=False): 
    import cv2

    video = cv2.VideoCapture(cam_list[str(cam_id)])

    while True:
        success, frame = video.read()
        if not success:
            print('ERROR:  Error getting video frame for Camera ID',cam_id)
            break
        elif stop_capture:
            video.ReleaseCapture()
            break
        else:
            ret_status, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_multi_frames(cam_id_1,cam_id_2,cam_id_3,cam_id_4,stop_capture=False,show_debug_info=False): 
    import cv2, numpy

    if show_debug_info == 'DEBUG': 
        print ("DEBUG:   Multi-cam: Force reset resolution of cameras")

    for cam_id in sess_defaults.keys():     # Force all cameras to the same resolution
        if not cam_id == '0':       # Don't overwrite default values
            session['camera_id']=cam_id     # Change camera ID or you'll overwrite the same one over and over
            session.update(fs_size=sess_defaults[cam_id][2])
            set_frame_size('11')
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'], show_debug_info)
        if show_debug_info == 'DEBUG': 
            print ('DEBUG:   Frame size reset for Cam ID: ',cam_id)

    video1 = cv2.VideoCapture(cam_list[str(cam_id_1)])
    video2 = cv2.VideoCapture(cam_list[str(cam_id_2)])
    video3 = cv2.VideoCapture(cam_list[str(cam_id_3)])
    video4 = cv2.VideoCapture(cam_list[str(cam_id_4)])

    while True:
        success_1, frame_1 = video1.read()
        success_2, frame_2 = video2.read()
        success_3, frame_3 = video3.read()
        success_4, frame_4 = video4.read()

        if not success_1:
            print('ERROR:  Error getting video frame for Camera ID',cam_id_1)
            break
        elif not success_2:
            print('ERROR:  Error getting video frame for Camera ID',cam_id_2)
            break
        h_concat_row_1 = numpy.concatenate((frame_1,frame_2), axis=1)
        if not success_3:
            print('ERROR:  Error getting video frame for Camera ID',cam_id_3)
            break
        elif not success_4:
            print('ERROR:  Error getting video frame for Camera ID',cam_id_4)
            break
        h_concat_row_2 = numpy.concatenate((frame_3,frame_4), axis=1)
        v_concat = numpy.concatenate((h_concat_row_1,h_concat_row_2), axis=0)

        frame = v_concat

        if stop_capture:
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
    sys.path.append('config')   # allows for finding config folder
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
