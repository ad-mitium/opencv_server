#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023
 
import requests
from time import strftime

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
    print (f'DEBUG:     Session data:\n',session)
    return 0

def initialize_cams(show_debug_info=False):
    action = 'init'
    cam_online_status={}
 
    if show_debug_info == 'DEBUG': 
        print ('DEBUG:   Initializing cameras...')
        # print (session,f'\n',sess_defaults)
    else:
        print ('INFO:    Initializing cameras...')

    # Test connection to see if camera is online
    for cam_ids,url in cam_list.items():
        url_stripped = strip_url(cam_list[str(cam_ids)])
        get_cam_status=send_url_command(url_stripped,show_debug_info)
        cam_online_status[int(cam_ids)]=get_cam_status
        if get_cam_status == 200:
            session['online_status'] = True
            if show_debug_info == 'DEBUG': 
                if not cam_id == '0':       # Don't show '0', as it is not being written
                    print('DEBUG:   ',cam_ids,'session_online:',session['online_status'])
        else:
            session['online_status'] = False
            if show_debug_info == 'DEBUG': 
                if not cam_id == '0':       # Don't show '0', as it is not being written
                    print('DEBUG:   ',cam_ids,'session_online:',session['online_status'])
            

    for cam_id in sess_defaults.keys():
        if not cam_id == '0':       # Don't assign '0', as it is not being written
            print ('INFO:    Initializing camera', cam_id)
            session['camera_id']=cam_id     # Change camera ID or you'll overwrite the same one over and over
            session.update(ae_level=sess_defaults[cam_id][0],bpc=sess_defaults[cam_id][1],fs_size=sess_defaults[cam_id][2],
                white_balance=sess_defaults[cam_id][3],flip=sess_defaults[cam_id][4],ae_compensation=sess_defaults[cam_id][5],
                ae_dsp=sess_defaults[cam_id][6],gain_ceiling=sess_defaults[cam_id][7],quality=sess_defaults[cam_id][8])  # Change all declared values to default values 
        # if not cam_id == '0':       # Don't output '0', as it is not being written
        #     print("[ Cam:",cam_session[str(cam_id)]['camera_id']," ae:", cam_session[str(cam_id)]['ae_level']," wb:", cam_session[str(cam_id)]['white_balance']," bpc:", cam_session[str(cam_id)]['bpc']," flip mode:", cam_session[str(cam_id)]['flip']," status:", session['online_status'],"] ")
        if not cam_id == '0':       # Don't overwrite default values
            if show_debug_info == 'DEBUG': 
                print ('DEBUG:   Defaults set for Cam ID: ',cam_id)
                print ('DEBUG:   ',cam_ids,'session_online:',session['online_status'])
            # Initialize camera if it is online
            if cam_online_status[cam_id] == 200 :
                set_ae_exposure(cam_id,None,int(session['ae_level']),show_debug_info,True,action) 
                set_black_point(cam_id, session['bpc'])
                set_frame_size(cam_id, session['fs_size'])
                set_white_balance(cam_id, session['white_balance'])
                set_flip_image(cam_id, session['flip'])
                set_aec(cam_id, session['ae_compensation'])
                set_aec_dsp(cam_id, session['ae_dsp'])
                set_gain_ceiling(cam_id, session['gain_ceiling'])
                set_quality(cam_id, session['quality'])
                set_DCW(cam_id)
            else:
                print ('INFO:    Stream for Camera {} has not been updated because it is offline'.format(cam_id))
            # if not cam_id == '0':
            write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'])
            if show_debug_info == 'DEBUG':
                print ('DEBUG:   Initial writing of session defaults completed for Camera: ', cam_id)
            print("[ Cam:",cam_session[str(cam_id)]['camera_id']," ae:", cam_session[str(cam_id)]['ae_level']," wb:", cam_session[str(cam_id)]['white_balance']," bpc:", cam_session[str(cam_id)]['bpc']," flip mode:", cam_session[str(cam_id)]['flip']," status:", cam_online_status[cam_id],"] ")
    if show_debug_info == 'DEBUG': 
        print ('DEBUG:   Cameras initialized',f'\n',sess_defaults)
    else:
        print('INFO:    Stream for Cameras have been initialized to default values')
    session['camera_id']='1'     # Reassign camera ID back to 1 after initializing

def set_reset(cam_id, show_debug_info = False):     # Handles initialization and reset
    if not cam_id == '0':

        # show_debug_info = check_debug_status(False)
        suppress = True
        action = cam_id

        # Test connection to see if camera is online
        url_stripped = strip_url(cam_list[str(cam_id)])
        get_cam_status=send_url_command(url_stripped,show_debug_info)
        if get_cam_status == 200:
            session['online_status'] = True
        else:
            session['online_status'] = False

        if show_debug_info == 'DEBUG': 
            print ('DEBUG:   Resetting settings for Cam ID: ',cam_id)
            print ('DEBUG:    Current settings for Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])

        session.update(camera_id=cam_id,ae_level=sess_defaults['0'][0],bpc=sess_defaults['0'][1],fs_size=sess_defaults['0'][2],
            white_balance=sess_defaults['0'][3],flip=sess_defaults[int(cam_id)][4],ae_compensation=sess_defaults[int(cam_id)][5],
            ae_dsp=sess_defaults[int(cam_id)][6],gain_ceiling=sess_defaults[int(cam_id)][7],quality=sess_defaults[int(cam_id)][8])  # Change all declared values to default values 
        sess_defaults[cam_id]=sess_defaults['0']

        if show_debug_info == 'DEBUG': 
            print('DEBUG:    Session has been updated to default values')
            print_session_data()
            # print(sess_defaults)

        if  session['online_status'] == True: 
            set_ae_exposure(cam_id,None,int(session['ae_level']),show_debug_info,suppress,action) 
            set_black_point(cam_id, session['bpc'],show_debug_info)
            set_frame_size(cam_id, session['fs_size'],show_debug_info)
            set_white_balance(cam_id, session['white_balance'],show_debug_info)
            set_flip_image(cam_id, session['flip'],show_debug_info)
            set_aec(cam_id, session['ae_compensation'],show_debug_info)
            set_aec_dsp(cam_id, session['ae_dsp'])
            set_gain_ceiling(cam_id, session['gain_ceiling'],show_debug_info)
            set_quality(cam_id, session['quality'],show_debug_info)
        else:
            print ('INFO:    Stream for Camera {} has not been reset because it is offline'.format(cam_id))

        if show_debug_info == 'DEBUG': 
            print ('DEBUG:   Defaults reset for Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
            print(sess_defaults)
        else:
            print ('INFO:    Stream for Camera {} has been reset to default values'.format(cam_id))

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
            # Test connection to see if camera is online
            url_stripped = strip_url(cam_list[str(cam_id)])
            get_cam_status=send_url_command(url_stripped,show_debug_info)
            if get_cam_status == 200:
                session['online_status'] = True
            else:
                session['online_status'] = False

            session.update(camera_id=cam_id,ae_level=cam_session[cam_id]['ae_level'],bpc=cam_session[cam_id]['bpc'],fs_size=cam_session[cam_id]['fs_size'],
                white_balance=cam_session[cam_id]['white_balance'],flip=cam_session[cam_id]['flip'],ae_compensation=cam_session[cam_id]['ae_compensation'],
                    ae_dsp=cam_session[cam_id]['ae_dsp'],gain_ceiling=cam_session[cam_id]['gain_ceiling'],quality=cam_session[cam_id]['quality'])  # Change all declared values to stored values 
            if show_debug_info == 'DEBUG': 
                print('DEBUG:   Status of camera connection is {}'.format(session['online_status']))
                print('DEBUG:   Changing stream to previous values')
                print_session_data()
                if not cam_id == 'Multi':
                    print ('DEBUG:     Camera session data:    [{}]'.format(cam_id),cam_session[cam_id])

            if session['online_status'] :
                set_ae_exposure(cam_id,None,int(session['ae_level']),show_debug_info) # None forces a "set level" instead of changing exposure direction
                set_black_point(cam_id, session['bpc'],show_debug_info)
                set_frame_size(cam_id, session['fs_size'],show_debug_info)
                set_white_balance(cam_id, session['white_balance'],show_debug_info)
                set_flip_image(cam_id, session['flip'],show_debug_info)
                set_aec(cam_id, session['ae_compensation'])
                set_aec_dsp(cam_id, session['ae_dsp'])
                set_gain_ceiling(cam_id, session['gain_ceiling'])
                set_quality(cam_id, session['quality'])
            else:
                print ('INFO:    Stream for Camera {} has not been updated because it is offline'.format(cam_id))

            if not show_debug_info == 'DEBUG': 
                print('INFO:    Stream for Camera {} has been updated'.format(cam_id))
        else:       # Make updates for multiple views
            suppress = True
            action = cam_id
            for cam_id_for in sess_defaults.keys():

                # print('Cam_id_for before if 0 test=',cam_id_for)
                if not cam_id_for == '0': 
                    if not cam_id_for == 'Multi':       # Don't overwrite default values
                        # Test connection to see if camera is online
                        url_stripped = strip_url(cam_list[str(cam_id_for)])
                        get_cam_status=send_url_command(url_stripped,show_debug_info)
                        if get_cam_status == 200:
                            session['online_status'] = True
                        else:
                            session['online_status'] = False

                        # print('Cam_id_for after Multi test=',cam_id_for,'session camera id',session['camera_id'] )
                        session['camera_id']=cam_id_for     # Change camera ID or you'll overwrite the same one over and over
                        # print('Cam_id_for after reassignment=',cam_id_for,'session camera id',session['camera_id'] )
                        session.update(ae_level=sess_defaults[cam_id_for][0],bpc=sess_defaults[cam_id_for][1],fs_size=sess_defaults[cam_id_for][2],
                            white_balance=sess_defaults[cam_id_for][3],flip=sess_defaults[cam_id_for][4],ae_compensation=sess_defaults[cam_id_for][5],
                            ae_dsp=sess_defaults[cam_id_for][6],gain_ceiling=sess_defaults[cam_id_for][7],quality=sess_defaults[cam_id_for][8])  # Change all declared values to default values 
                        if show_debug_info == 'DEBUG': 
                            print ('DEBUG:   Status of camera connection is {}'.format(session['online_status']))
                            print ('DEBUG:   Previous settings loaded for Cam ID: ',cam_id_for, sess_defaults[cam_id_for])
                        # print('Cam_id_for before set_ae_exp=',cam_id_for,'session camera id',session['camera_id'], 'Cam_ID=',cam_id)

                        # if session['online_status'] :
                        #     set_ae_exposure(cam_id_for,None,int(session['ae_level']),show_debug_info,suppress,action)
                        #     set_black_point(cam_id_for, session['bpc'])
                        #     set_frame_size(cam_id_for, '11')
                        #     set_white_balance(cam_id_for, session['white_balance'])
                        #     set_flip_image(cam_id_for, session['flip'])
                        #     set_aec(cam_id_for, session['ae_compensation'])
                        #     set_gain_ceiling(cam_id_for, session['gain_ceiling'])
                        #     set_quality(cam_id_for, session['quality'])
                        #     write_session_data(session['camera_id'], session['ae_level'], session['bpc'], session['fs_size'], session['white_balance'], session['flip'])
                    if show_debug_info == 'DEBUG':
                        print ('DEBUG:   Initial writing of session defaults completed for Camera: ', cam_id_for)
            if show_debug_info == 'DEBUG':
                print(f'DEBUG:   In multi mode\n',sess_defaults)
    else:
        print('ERROR:  Cannot update Camera ID ',cam_id)

    return show_debug_info

def write_session_data(cam_id, ae_val, bpc_mode, frame_size, wb_mode, flip, show_debug_info = False, suppress = False):
    if not cam_id == '0':    # Never overwrite '0'
        if not suppress:
            if show_debug_info == 'DEBUG': 
                print ('DEBUG:   Current Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
                # print_session_data()
        cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'] = str(ae_val), bpc_mode, frame_size, wb_mode, flip

        if not suppress:
            if show_debug_info == 'DEBUG': 
                print ("[ Cam:",cam_session[str(cam_id)]['camera_id']," ae:", cam_session[str(cam_id)]['ae_level']," wb:", cam_session[str(cam_id)]['white_balance']," bpc:", cam_session[str(cam_id)]['bpc']," flip mode:", cam_session[str(cam_id)][' flip'],"status:", session['online_status'], end=" ] ")
                print('DEBUG:   Writing camera session values')
                # print (f'DEBUG:     Camera session data:\n         ',sess_defaults)    
        # else:
        #     print('INFO:    Stream has been reset to default values')
        write_success = 0
    else:
        if not suppress:
            print('ERROR:  Cannot overwrite default values for ID ',cam_id)
        write_success = 1
    return write_success

def get_session_data(cam_id, show_debug_info = False):      # only used with get_multi_frames
    session.update(camera_id=cam_id,ae_direction=cam_session[str(cam_id)]['ae_level'],bpc=cam_session[str(cam_id)]['bpc'], white_balance=cam_session[str(cam_id)]['white_balance'], flip = cam_session[str(cam_id)]['flip']) 

    if show_debug_info == 'DEBUG': 
        print('DEBUG:   Getting camera session values')
        print ('DEBUG:     Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])

    return 0

def strip_url(url, show_debug_info = False): 
    from urllib.parse import urlparse

    parts = urlparse(url)
    domain_addr = parts.scheme + '://' + parts.netloc.split(':')[0] 
    if show_debug_info == 'DEBUG':
        print ('DEBUG:   Camera IP address: ',domain_addr)
    return domain_addr

def send_url_command(url,show_debug_info = False, suppress = True):
    import urllib3
    # from time import strftime

    try:
        get_request = requests.get(url,timeout=5)   # Increase timeout to 5 seconds
        if get_request.status_code == 200:
            get_status_code = get_request.status_code
        # if show_debug_info == 'DEBUG':
        #     print (' status code: ',get_status_code)
        get_request.raise_for_status()
    except requests.exceptions.Timeout:
        get_status_code = 'Timeout'
        if not suppress:
            if show_debug_info == 'DEBUG':
                print ('  status code: ',get_status_code)
        curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')
        print('ERROR:   Camera: {}  GET request has timed out'.format(session['camera_id']),'at',curr_time)
    except urllib3.exceptions.MaxRetryError:
        get_status_code = 'Max retries' 
        # print()
        if not suppress:
            if show_debug_info == 'DEBUG':
                print ('  status code: ',get_status_code)
        curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')
        print('ERROR:   GET request exceeded number of retries: ',url,'at',curr_time)
    except requests.exceptions.ConnectionError:
        get_status_code = 'ConnError'
        # print()
        if not suppress:
            if show_debug_info == 'DEBUG':
                print ('  status code: ',get_status_code)
        curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')
        if not suppress:
            print('ERROR:   GET request unable to connect to host: ',url,'at',curr_time)
    finally:
        # print('Command sent')            print('here')
        pass
    return get_status_code

def update_online_status(cam_id, suppress = False, show_debug_info = False):    # Note: order of suppression and debug info deliberately swapped
    # print('Cam_id in update_online_status=',cam_id)
    url_stripped = strip_url(cam_list[str(cam_id)])
    get_cam_status=send_url_command(url_stripped,show_debug_info,suppress)
    return get_cam_status

def set_ae_exposure(cam_id,ae_dir, ae_val = 'NaN',show_debug_info = False, suppress = False, action = ''): 
    is_reset = False
    is_multi = False
    is_initialize = False

    if action == 'init':
        is_initialize = True
    elif action == 'reset':     # Retain reset status
        is_reset = True
    elif action == 'Multi':
        is_multi = True

    if cam_id == 'stop':     # Retain stop status
        is_stopped = True
    else:
        is_stopped = False

    # print('Action=',action,'Cam_id=',cam_id)
    if not session['camera_id'] == '0':    # Never go to '0'

        # if show_debug_info == 'DEBUG': 
        #     print ("DEBUG:     IN AE: Camera ID: " ,session['camera_id'])

        # print('ao1')
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            # print('Cam_id=',cam_id,'Session camera ID=',session['camera_id'])
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            if not suppress:
                if show_debug_info == 'DEBUG':
                    print('DEBUG:     Curent ae_level: ',session['ae_level'],' direction: ', ae_dir, end='')
                elif not suppress:
                    print('INFO:      Curent ae_level: ',session['ae_level'],' direction: ', ae_dir, end='')

                if ae_dir == '0':   # For reset exposure
                    ae_val = '0'
                elif ae_dir == None:    # Force an overwrite of AE level instead of direction change
                    if type(ae_val) == int:    # ae_val is now assigned a value provided during function call
                        if show_debug_info == 'DEBUG':
                            print(f'\n',end='')
                            print('DEBUG:     Camera ID {} exposure value has changed: Force set AE value to: '.format(session['camera_id']), ae_val, end='')
                        elif not suppress:
                            # print(f'\n',end='')
                            print(f'\nINFO:      Camera exposure value has changed: Force set AE value to: ', ae_val, end='')
                    else:
                        print(f'\n',end='')
                        print('ERROR:   ae_val is NaN', ae_val, type(ae_val), end='')
                        ae_val = int(ae_val)
                else:
                    ae_val = int(session['ae_level']) + int(ae_dir)     # Change exposure in the direction requested
            # print('ao2')
            
            if str(ae_val) in ae_level_range:
                url = url_stripped + '/control?var=ae_level&val='+str(ae_val)
                session['ae_level'] = str(ae_val)
                # print('ao2b')
                status_code = send_url_command(url,show_debug_info,suppress)
                # print('ao2c')
                if status_code == 200:
                    # print('ao2c1')
                    if show_debug_info == 'DEBUG':
                        # print('ao2c2')
                        if not suppress:
                            print ('  New ae_level: ',ae_val)      # Part of previous INFO output
                            # print('ao2c3')
                        elif is_initialize or is_reset or is_multi:   # Don't force newline 
                            # print('ao2c4')
                            pass
                        else:
                            # print('ao2c5')
                            print(f'\n',end='')     # Force newline before displaying next debug
                        # print ('DEBUG:         New ae_level: ',ae_val)      # Part of previous DEBUG output
                        # print('ao2c6')
                    else:
                        # print('ao2c7')
                        if not suppress:
                            print ('  New ae_level: ',ae_val)      # Part of previous INFO output
                        # print('ao2c8')
                        # print(f'\n',end='')

                # print('ao2d')
            else:
                print(f'\n',end='')
                print ('ERROR:   Value out of range: ',ae_val, end='')
                url = 'No request made, AE value out of range ' # No url if you don't make a request
                status_code = 'No request made, AE value out of range ' # No status code if you don't make a request
                if ae_val > 2:      # Put ae_val back in range for DEBUG display purposes, wasn't changed in session['ae_level']
                    ae_val = 2
                elif ae_val < -2:
                    ae_val = -2
                if show_debug_info == 'DEBUG':
                    print(f'\nDEBUG:     AE level reset to: ',ae_val)
                else:
                    print('  AE level reset to: ',ae_val)

            # print('ao3')
            # if show_debug_info == 'DEBUG': 
            #     print('DEBUG:     IN AE, AFTER REQUEST SENT: Camera ID: ' ,session['camera_id'])

            if show_debug_info == 'DEBUG':
                if status_code == 200:
                    if not suppress:
                        print ('DEBUG:     AE set to: ',ae_val,' URL: ',url, ' level: ',session['ae_level'],' status code: ',status_code)
            # print('ao4')

            if status_code == 200:
                if not suppress:
                    write_session_data(cam_session[str(cam_id)]['camera_id'], ae_val, cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
                else:
                    write_session_data(cam_session[str(cam_id)]['camera_id'], ae_val, cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], not show_debug_info,suppress)
            else:
                print('ERROR:     AE level was not changed')

def set_black_point(cam_id, bpc_mode, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=bpc&val='+str(bpc_mode)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                # print ('DEBUG:     Black point correction set to: ',bpc_mode)     # Duplicate because of toggle logic
                # print (' status code: ',status_code)
                pass
            if status_code == 200:
                write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], bpc_mode, cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
            else:
                print('ERROR:     Black point correction was not changed for camera {}'.format(session['camera_id']))

def set_flip_image(cam_id, mirror_mode, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            hmirror_adjust_url = url_stripped + '/control?var=hmirror&val='+str(mirror_mode)
            if session['online_status']:
                h_status_code = send_url_command(hmirror_adjust_url,show_debug_info)
            else:
                h_status_code = False
            # get_request = requests.get(hmirror_adjust)
            if show_debug_info == 'DEBUG':
                print ('DEBUG:     Image flip: Horizontal mirror: ',h_status_code, end=' ')

            vfliup_adjust_url = url_stripped + '/control?var=vflip&val='+str(mirror_mode)
            if session['online_status']:
                v_status_code = send_url_command(vfliup_adjust_url,show_debug_info)
            else:
                v_status_code = False
            # get_request = requests.get(vfliup_adjust)
            if show_debug_info == 'DEBUG':
                print (' Vertical flip: ',v_status_code)
                print ('DEBUG:    Image flip for Cam ID: ',session['camera_id'],' Image mirror set to: ',mirror_mode)
                # print_session_data()
            if h_status_code == 200 and v_status_code == 200:
                write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'],mirror_mode, show_debug_info)
            else:
                print('ERROR:     Image flip for Cam ID: ',session['camera_id'],' was not changed')

def set_frame_size(cam_id, frame_size, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            url = url_stripped + '/control?var=framesize&val='+str(frame_size)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Frame size set to: ",frame_size, " Resolution: ", end=' ')
                if frame_size == '11':
                    print('1280 x 720', end=' ')
                else:
                    print('800 x 600', end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], frame_size, cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
            else:
                print('ERROR:     Frame size was not changed for camera {}'.format(session['camera_id']))
                # print(status_code)

def set_white_balance(cam_id, wb_mode, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url_stripped = strip_url(cam_list[str(session['camera_id'])])

            url = url_stripped + '/control?var=wb_mode&val='+str(wb_mode)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:    White Balance set to: ",wb_mode, end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], wb_mode, cam_session[str(cam_id)]['flip'], show_debug_info)
            else:
                print('ERROR:     White Balance was not changed for camera {}'.format(session['camera_id']))

def set_gain_ceiling(cam_id, gain_ceiling, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=gainceiling&val='+str(gain_ceiling)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Gain ceiling set to: ",gain_ceiling, end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                # write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
                pass
            else:
                print('ERROR:     Gain ceiling was not changed for camera {}'.format(session['camera_id']))

def set_aec(cam_id, ae_compensation, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=aec&val='+str(ae_compensation)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Auto exposure compensation set to: ",ae_compensation, end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                # write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
                pass
            else:
                print('ERROR:     Auto exposure compensation was not changed for camera {}'.format(session['camera_id']))

def set_aec_dsp(cam_id, ae_dsp, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=aec2&val='+str(ae_dsp)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Auto exposure compensation DSP set to: ",ae_dsp, end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                # write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
                pass
            else:
                print('ERROR:     Auto exposure compensation DSP was not changed for camera {}'.format(session['camera_id']))

def set_quality(cam_id, quality, show_debug_info = False): 
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=quality&val='+str(quality)
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Image quality is set to: ",quality, end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                # write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
                pass
            else:
                print('ERROR:     Image quality was not changed for camera {}'.format(session['camera_id']))

def set_DCW(cam_id, show_debug_info = False):    # Camera is set to down convert image, this disables that
    if not session['camera_id'] == '0':    # Never go to '0'
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        if not session['camera_id'] == 'stop' or not session['camera_id'] == 'reset':
            url = url_stripped + '/control?var=dcw&val='+dcw[0]
            if not session['camera_id'] == 'Multi':
                session['online_status']=update_online_status(cam_id)   # Check status beforehand
            if session['online_status']:
                status_code = send_url_command(url,show_debug_info)
            else:
                status_code = False
            if show_debug_info == 'DEBUG':
                print ("DEBUG:     Down conversion is set to: ",dcw, end=' ')
                print (' status code: ',status_code)
            if status_code == 200:
                # write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
                pass
            else:
                print('ERROR:     Down conversion was not changed for camera {}'.format(session['camera_id']))

def load_no_image():
    import cv2

    img_file = cv2.imread('static/images/source_unavailable.jpg')

    return img_file

def get_frames(cam_id,stop_capture=False): 
    import cv2

    curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')
    text="Cam "+cam_session[str(cam_id)]['camera_id']+" " 
    font = cv2.FONT_HERSHEY_COMPLEX

    # Update online status of camera
    session['online_status']=update_online_status(cam_id,True)

    print ("[ Cam:",cam_session[str(cam_id)]['camera_id']," ae:", cam_session[str(cam_id)]['ae_level']," wb:", cam_session[str(cam_id)]['white_balance']," bpc:", cam_session[str(cam_id)]['bpc']," flip mode:", cam_session[str(cam_id)]['flip']," status:", session['online_status'],"] ")

    try:
        video = cv2.VideoCapture(cam_list[str(cam_id)])
        video.setExceptionMode(True)
    # except cv2.error:
    except Exception as except_msg:
        print('ERROR:   An exception has occurred in opening the stream for Camera ID',cam_id)
        print(except_msg)

    while True:
        success, frame = video.read()
        if not success:
            print('ERROR:  Error getting video frame for Camera ID',cam_id)
            break
        elif stop_capture:
            video.ReleaseCapture()
            break
        else:

            cv2.putText(frame,  
                text,  
                (15, 25),  
                font, 1,  
                (255, 255, 255),  
                2,  
                cv2.LINE_AA) 
            
            ret_status, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_multi_frames(cam_id_1,cam_id_2,cam_id_3,cam_id_4,stop_capture=False,show_debug_info=False): 
    import cv2, numpy

    text1="Cam "+cam_session[str(cam_id_1)]['camera_id']+" " 
    text2="Cam "+cam_session[str(cam_id_2)]['camera_id']+" " 
    text3="Cam "+cam_session[str(cam_id_3)]['camera_id']+" " 
    text4="Cam "+cam_session[str(cam_id_4)]['camera_id']+" " 
    font = cv2.FONT_HERSHEY_COMPLEX


    frame_count = 0
    cam_online_status={}
    # y = 0      # for diagnoistics

    if show_debug_info == 'DEBUG': 
        print ("DEBUG:   Multi-cam: Force reset resolution of cameras")

    for cam_id in sess_defaults:     # Force all cameras to the same resolution
        # print(cam_id,sess_defaults)
        # print(cam_id, session)
        if not cam_id == '0':       # Don't overwrite default values
            session['camera_id']=cam_id     # Change camera ID or you'll overwrite the same one over and over
            session['online_status']=update_online_status(cam_id,True)
            cam_online_status[int(cam_id)]=session['online_status']
            if  cam_online_status[int(cam_id)] == 200:
                get_session_data(cam_id)
                if show_debug_info == 'DEBUG': 
                    print ('DEBUG:     Camera session data:    [{}]'.format(cam_id),sess_defaults[cam_id])
            # session['camera_id']=cam_id     # Change camera ID or you'll overwrite the same one over and over
            # session['online_status']=update_online_status(cam_id)
            # session.update(fs_size=sess_defaults[cam_id][2])        # Store original frame size setting
                set_frame_size(cam_id,'11')
                write_session_data(cam_session[str(cam_id)]['camera_id'], cam_session[str(cam_id)]['ae_level'], cam_session[str(cam_id)]['bpc'], cam_session[str(cam_id)]['fs_size'], cam_session[str(cam_id)]['white_balance'], cam_session[str(cam_id)]['flip'], show_debug_info)
            print ("[ Cam:",cam_session[str(cam_id)]['camera_id']," ae:", cam_session[str(cam_id)]['ae_level']," wb:", cam_session[str(cam_id)]['white_balance']," bpc:", cam_session[str(cam_id)]['bpc']," flip mode:", cam_session[str(cam_id)]['flip']," status:", cam_online_status[int(cam_id)], end=" ] ")
        if show_debug_info == 'DEBUG': 
            print ('\nDEBUG:   Frame size reset for Cam ID: ',cam_id)
    print ("")      # Send newline after all camera session info is printed
    # print (sess_defaults)
    if show_debug_info == 'DEBUG': 
        print (cam_online_status)

    if cam_online_status[int(cam_id_1)] == 200:
        video1 = cv2.VideoCapture(cam_list[str(cam_id_1)])
        # video1.setExceptionMode(True)
    else:
        success_1 = False
        frame_1 = load_no_image()
        video1 = (success_1,frame_1)

    if cam_online_status[int(cam_id_2)] == 200:
        video2 = cv2.VideoCapture(cam_list[str(cam_id_2)])
    #     video2.setExceptionMode(True)
    else:
        success_2 = False
        frame_2 = load_no_image()
        video2 = (success_2,frame_2)

    if cam_online_status[int(cam_id_3)] == 200:
        video3 = cv2.VideoCapture(cam_list[str(cam_id_3)])
    #     video3.setExceptionMode(True)
    else:
        success_3 = False
        frame_3 = load_no_image()
        video3 = (success_3,frame_3)

    if cam_online_status[int(cam_id_4)] == 200:
        video4 = cv2.VideoCapture(cam_list[str(cam_id_4)])
    #     video4.setExceptionMode(True)
    else:
        success_4 = False
        frame_4 = load_no_image()
        video4 = (success_4,frame_4)

    while True:
        if cam_online_status[int(cam_id_1)] == 200:
            success_1, frame_1 = video1.read()
        else:
            success_1 = False
            frame_1 = load_no_image()
        if cam_online_status[int(cam_id_2)] == 200:
            success_2, frame_2 = video2.read()
        else:
            success_2 = False
            frame_2 = load_no_image()
        if cam_online_status[int(cam_id_3)] == 200:
            success_3, frame_3 = video3.read()
        else:
            success_3 = False
            frame_3 = load_no_image()
        if cam_online_status[int(cam_id_4)] == 200:
            success_4, frame_4 = video4.read()
        else:
            success_4 = False
            frame_4 = load_no_image()

        if not success_1 or not cam_online_status[1]:
            if frame_count < 900:
                if frame_count == 1:
                    print('ERROR:  Error getting video frame for Camera ID',cam_id_1)
                frame_count = frame_count + 1
            else:       # Exceeded 900 frames or 30 secs with error, reset to 0
                frame_count = 0
                # print(x)

            # frame_1 = numpy.zeros((720,1280,3), dtype = int)
            frame_1 = load_no_image()
            # if y == 0:
            #     print(frame_1)     # for diagnoistics
            #     y = 1
            # break
        elif not success_2 or not cam_online_status[2]:
            if frame_count < 900:
                if frame_count == 1:
                    print('ERROR:  Error getting video frame for Camera ID',cam_id_2)
                frame_count = frame_count + 1
            else:       # Exceeded 900 frames or 30 secs with error, reset to 0
                frame_count = 0

            # frame_2 = numpy.zeros((720,1280,3), dtype = int)
            frame_2 = load_no_image()

        if frame_1 is None:
            frame_1 = load_no_image()
        if frame_2 is None:
            frame_2 = load_no_image()

        cv2.putText(frame_1, 
                text1, 
                (15, 25), 
                font, 1, 
                (255, 255, 255), 
                2, 
                cv2.LINE_AA) 
        cv2.putText(frame_2, 
                text2, 
                (15, 25), 
                font, 1, 
                (255, 255, 255), 
                2, 
                cv2.LINE_AA) 

        # try:
        h_concat_row_1 = numpy.concatenate((frame_1,frame_2), axis=1)
        # except ValueError:
        #     h_concat_row_1 = numpy.concatenate((frame_1,frame_2), axis=1)

        if not success_3 or not cam_online_status[3]:
            if frame_count < 900:
                if frame_count == 1:
                    print('ERROR:  Error getting video frame for Camera ID',cam_id_3)
                frame_count = frame_count + 1
            else:       # Exceeded 900 frames or 30 secs with error, reset to 0
                frame_count = 0

            # frame_3 = numpy.zeros((720,1280,3), dtype = int)
            frame_3 = load_no_image()
            # break
        elif not success_4 or not cam_online_status[4]:
            if frame_count < 900:
                if frame_count == 1:
                    print('ERROR:  Error getting video frame for Camera ID',cam_id_4)
                frame_count = frame_count + 1
            else:       # Exceeded 900 frames or 30 secs with error, reset to 0
                frame_count = 0

            frame_4 = load_no_image()
            # break

        if frame_3 is None:
            frame_3 = load_no_image()
        if frame_4 is None:
            frame_4 = load_no_image()

        cv2.putText(frame_3, 
                text3, 
                (15, 25), 
                font, 1, 
                (255, 255, 255), 
                2, 
                cv2.LINE_AA) 
        cv2.putText(frame_4, 
                text4, 
                (15, 25), 
                font, 1, 
                (255, 255, 255), 
                2, 
                cv2.LINE_AA) 

        # try:
        h_concat_row_2 = numpy.concatenate((frame_3,frame_4), axis=1)
        # except ValueError:
        #     h_concat_row_2 = numpy.concatenate((frame_3,frame_4), axis=1)

        v_concat = numpy.concatenate((h_concat_row_1,h_concat_row_2), axis=0)

        frame = v_concat

        if stop_capture:
            video1.ReleaseCapture()
            video2.ReleaseCapture()
            video3.ReleaseCapture()
            video4.ReleaseCapture()
            break
        else:
            ret_status, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    import sys
    from sessions import session, sess_defaults, cam_session
    # sys.path.append('config')   # allows for finding config folder
    from ..config.cameras import camera_list as cam_list
    from ..config.cameras import ae_level as ae_level_range
    from ..config.cameras import framesize, white_balance, dcw
    from ..config.network import host
    from ..config.network import debug_level
    # import network as network

    show_debug_info = check_debug_status()
    print (show_debug_info, session['enabled_debug'])

else:
    from lib.sessions import session, sess_defaults, cam_session
    from config.cameras import camera_list as cam_list
    from config.cameras import ae_level as ae_level_range
    from config.cameras import framesize, white_balance, dcw
    from config.network import host
    from config.network import debug_level
    import config.network as network

    # show_debug_info = check_debug_status()
    # print (show_debug_info, session['enabled_debug'])
    # print (show_debug_info)
