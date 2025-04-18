#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023

import argparse
from time import strftime
from flask import Flask, render_template, Response, request
from config.cameras import camera_list as cam_list
from config.cameras import ae_level as ae_level_range
from config.cameras import framesize
from config.network import host
from config.network import debug_level
import config.network as network
from lib import version as ver
from lib.sessions import session, sess_defaults
from lib.functions import get_frames, set_ae_exposure, set_black_point, set_flip_image, set_frame_size, set_white_balance 
from lib.functions import check_debug_status, update_cam, set_reset, initialize_cams, get_multi_frames

app = Flask(__name__, template_folder='html')

version_number = (0,3,0)


@app.route('/video_feed/', methods=["GET"])
@app.route('/video_feed/<string:id>/', methods=["GET"]) # Overload to get direct feed
def video_feed(id='1'):
    id=session.get('camera_id')

    if verbose == 'DEBUG':
       print('DEBUG:    Getting frames from Camera ID: ',id)
    if isinstance(id,int):  # Reset turns id into an integer
        id=str(id)
    if id.isdigit():
        id_int=int(id)
        if id_int==0:
            id='1'
        elif id_int > len(cam_list):
            id='1'
    else:
        id='1'  # Disallow injection
    
    cvid_stream = get_frames(id)
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(cvid_stream,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/multi_video_feed/', methods=["GET"])
def multi_video_feed():
    id1='1'
    id2='2'
    id3='3'
    id4='4'

    if verbose == 'DEBUG':
       print('DEBUG:    Getting frames from Camera IDs: ',id1,id2,id3,id4,False,verbose)

    cvid_stream = get_multi_frames(id1,id2,id3,id4)
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(cvid_stream,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=["GET", "POST"])
def index():
    index_html= 'index.html'
    stop_html = 'index_stop.html'
    multi_html= 'index_multi.html'

    # verbose = check_debug_status()
    # print (verbose)

    request_method = request.method
    form_data = request.form.to_dict()
    # print(form_data)
    # print('Verbose = ',verbose)
    if not form_data:
        if verbose == 'DEBUG':
            print ('DEBUG:    No Actions detected, defaulting to stop')
            # form_data = {'action': 'stop'}
        form_key, form_value = "None", "0"
    else:
        # form_key = form_data.keys()
        form_key = list(form_data.keys())[0]    # extract name of key from request.form.to_dict() 
        if verbose == 'DEBUG':
            print ('DEBUG:    Action detected: ', form_key)

    if 'fs_action' in form_key: 
        # print('Frame Size action')
        form_value = form_data.get('fs_action')
    elif 'wb_action' in form_key:
        # print('White Balance action')
        form_value = form_data.get('wb_action')
    elif 'bpc_action' in form_key:
        # print('Black Point Correction action')
        form_value = form_data.get('bpc_action')
    elif 'flip_action' in form_key:
        # print('Flip Image action')
        form_value = form_data.get('flip_action')
    elif 'ae_action' in form_key:
        # print('AE action')
        form_value = form_data.get('ae_action')
    elif 'action' in form_key:
        # print('Camera action')
        form_value = form_data.get('action')
        # print(form_value)
    else:
        print('Action not found')

    print('REQUEST:  Request form generated',end='')

    if verbose == 'DEBUG':
        print(f'\nDEBUG:     Request form: {form_data}, {form_key} = {form_value}')
    else:
        print(f': {form_key} = {form_value}')      # Concatenate requested value to Request message

    if request_method == 'POST':
        if form_data.get('action') == '1':
            # print ('Request: 1 Cam ID: ',session['camera_id'])
            if not session['camera_id'] == form_data.get('action'):
                session['camera_id']=form_data.get('action')
                update_cam(form_data.get('action'),False,verbose)
            else:
                session['camera_id']=form_data.get('action')
                if verbose == 'DEBUG':
                    print('DEBUG:   Camera ID not changed')
            # print ('Requested: 1 Cam ID: ',session['camera_id'])
            # if verbose == 'DEBUG': 
            #     print ('DEBUG:    Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 1:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 1",session['camera_id'])

        elif  form_data.get('action') == '2':
            # print ('Request: 2 Cam ID: ',session['camera_id'])
            if not session['camera_id'] == form_data.get('action'):
                session['camera_id']=form_data.get('action')
                update_cam(form_data.get('action'),False,verbose)
            else:
                session['camera_id']=form_data.get('action')
                if verbose == 'DEBUG':
                    print('DEBUG:   Camera ID not changed')
            # print ('Requested: 2 Cam ID: ',session['camera_id'])
            # if verbose == 'DEBUG': 
            #     print ('DEBUG:     Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 2:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 2",session['camera_id'])

        elif  form_data.get('action') == '3':
            # print ('Request: 3 Cam ID: ',session['camera_id'])
            if not session['camera_id'] == form_data.get('action'):
                session['camera_id']=form_data.get('action')
                update_cam(form_data.get('action'),False,verbose) 
            else:
                session['camera_id']=form_data.get('action')
                if verbose == 'DEBUG':
                    print('DEBUG:   Camera ID not changed')
            # print ('Requested: 3 Cam ID: ',session['camera_id'])
            # if verbose == 'DEBUG':
            #     print ('DEBUG:     Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 3:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 3",session['camera_id'])

        elif  form_data.get('action') == '4':
            # print ('Request: 4 Cam ID: ',session['camera_id'])
            if not session['camera_id'] == form_data.get('action'):
                session['camera_id']=form_data.get('action')
                update_cam(form_data.get('action'),False,verbose) 
            else:
                session['camera_id']=form_data.get('action')
                if verbose == 'DEBUG':
                    print('DEBUG:   Camera ID not changed')
            # print ('Requested: 4 Cam ID: ',session['camera_id'])
            # if verbose == 'DEBUG': 
            #     print ('DEBUG:     Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 4:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 4",session['camera_id'])

        elif  form_data.get('action') == 'Multi':
            # print ('Request: Multi Cam ID: ',session['camera_id'])
            if not session['camera_id'] == form_data.get('action'):
                session['camera_id']=form_data.get('action')
                update_cam(form_data.get('action'),False,verbose) 
            else:
                session['camera_id']=form_data.get('action')
                if verbose == 'DEBUG':
                    print('DEBUG:   Camera ID not changed')
            # print ('Requested: Multiple Camera Frames')
            # if verbose == 'DEBUG': 
            #     print ('DEBUG:     Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera Multiple:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera Multiple Frames",session['camera_id'])
            return render_template(multi_html)

        elif  form_data.get('action') == 'reset':
            # session['camera_id']='reset'
            if verbose == 'DEBUG':
                print('DEBUG:   Stream has been reset')
            else:
                print('INFO:    Stream has been reset')
            set_reset(session['camera_id'],verbose)     # Send reset to set_reset()
            
        elif  form_data.get('action') == 'stop':
            session['camera_id']='stop'
            if verbose == 'DEBUG':
                print('DEBUG:   Stream has been stopped')
            else:
                print('INFO:    Stream has been stopped')
            get_frames(session['camera_id'],True)   # Send stop capture to break stream
            return render_template(stop_html)

        elif form_data.get('fs_action') in framesize:
            session['fs_size']=form_data.get('fs_action')
            set_frame_size(session['camera_id'], session['fs_size'], verbose)

        elif form_data.get('flip_action') == '1':
            if verbose == 'DEBUG':
                print('DEBUG:     Image mirror mode is currently',session['flip'])
            # Toggle flip
            if session['flip'] == '1':  # Toggle image flip instead of forcing to one mode
                session['flip'] = '0'
                if verbose == 'DEBUG':
                    print('DEBUG:     Image mirror mode has been unset')
            else:
                if verbose == 'DEBUG':
                    print('DEBUG:     Image mirror mode does not match',end=' ')
                session['flip'] = '1'
                if verbose == 'DEBUG':
                    print('and has been set to',session['flip'])

            if verbose == 'DEBUG':
                print('DEBUG:     Image mirror mode is now set to',session['flip'])
            set_flip_image(session['camera_id'], session['flip'], verbose)

        elif form_data.get('bpc_action') == '1':
            # session['bpc']=form_data.get('bpc_action')
            if verbose == 'DEBUG':
                print('DEBUG:     Black Point Correction is currently',session['bpc'])
            # Toggle BPC
            if session['bpc'] == '1':  # Toggle bpc instead of forcing to one mode
                session['bpc'] = '0'
                if verbose == 'DEBUG':
                    print('DEBUG:     Black Point Correction has been unset')
            else:
                if verbose == 'DEBUG':
                    print('DEBUG:     Black Point Correction does not match',end=' ')
                session['bpc'] = '1'
                if verbose == 'DEBUG':
                    print('and has been set to',session['bpc'])

            if verbose == 'DEBUG':
                print('DEBUG:     Black Point Correction is now set to',session['bpc'])
            set_black_point(session['camera_id'], session['bpc'], verbose)

        elif form_data.get('wb_action') in ['0','1']:
            session['white_balance']=form_data.get('wb_action')
            set_white_balance(session['camera_id'], session['white_balance'], verbose)
            # if verbose == 'DEBUG':
            #     print('DEBUG:   WB  Cam_ID: ',session['camera_id'],' level: ',session['ae_level'],' WB value: ',session['white_balance'])

        elif form_data.get('ae_action') in ae_level_range: # Set exposure level
            session['ae_direction']=form_data.get('ae_action')
            set_ae_exposure(session['camera_id'], session['ae_direction'],'', verbose)
            # if verbose == 'DEBUG':
            #     print('DEBUG:   AE  Cam_ID: ',session['camera_id'],' level: ',session['ae_level'],' direction: ',session['ae_direction'],session['white_balance'])

        else:
            print("Undefined action")
            # session['camera_id']='1'
            pass # unknown camera ID, pass to video_feed() to deal with it

    curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')

    if verbose == 'DEBUG': 
        print('DEBUG:  {}: Route render:'.format(curr_time),request_method,' Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' Frame Size: ',session['fs_size'],' WB: ',session['white_balance'],' BPC: ',session['bpc'] )
        if not form_data.get('action') in ['1','2','3','4']:     # Print only if there is a camera ID in action 
            print('DEBUG:   Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
        # print('DEBUG: Request form: ',form_data)
    else:
        print('INFO:     {}: Route render:'.format(curr_time),request_method,' Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' Frame Size: ',session['fs_size'],' WB: ',session['white_balance'],' BPC: ',session['bpc'] )
    return render_template(index_html)

def create_app():
    print("App created")
    return app

if __name__ == '__main__':
    from waitress import serve
    url = 'http://'+network.host_address+':'+str(host['host_port'])

    #########   Command line interaction   #########
    # provide description and version info
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''OpenCV Server'''
    , 
    epilog=''' '''
    )
    parser.add_argument('-d','--debug-level', action='store_true',help='Change level of output from INFO to DEBUG')
    parser.add_argument('-ip','--host-ip', action='store_true',help='Show the IP address and exit')
    parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(ver.ver_info(version_number)), help='show the version number and exit')
    args = parser.parse_args()

    session['enabled_debug'] = args.debug_level

    # print('Server debug: ',session['enabled_debug'])

    if args.host_ip:
        print ("Access server using this ip address and port: http://{}:{}".format(network.host_address,host['host_port']))
    else:
        verbose = check_debug_status(False)     # Don't print session info
        if verbose == 'DEBUG':
            print("DEBUG:  Host IP and port:     {}:{}".format(network.host_address,host['host_port']))
        initialize_cams(verbose)
        if verbose == 'DEBUG':
            print('DEBUG:  Route "/" defaults: Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' Frame Size: ',session['fs_size'],' WB: ',session['white_balance'],' BPC: ',session['bpc'])
            # app.run(debug=True)
        else:
            print('INFO:    Ready to serve camera streams')
        serve(app, host=network.host_address, port=host['host_port'])

else:
    verbose = check_debug_status()
    initialize_cams(verbose)
