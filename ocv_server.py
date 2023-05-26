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
from lib.functions import check_debug_status, get_frames, set_ae_exposure, set_black_point, set_flip_image, set_frame_size, set_white_balance, set_defaults

app = Flask(__name__, template_folder='html')

version_number = (0,1,1)


@app.route('/video_feed/', methods=["GET"])
@app.route('/video_feed/<string:id>/', methods=["GET"]) # Overload to get direct feed
def video_feed(id='1'):
    id=session.get('camera_id')

    if verbose == 'DEBUG':
       print('DEBUG:  Getting frames from Camera ID: ',id)
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

@app.route('/', methods=["GET", "POST"])
def index():
    index_html= 'index.html'
    stop_html = 'index_stop.html'

    # verbose = check_debug_status()
    # print (verbose)

    if request.method == 'POST':
        if request.form.get('action') == '1':
            # print("Request get: ",request.form.get('action'), type(request.form.get('action')), ' Camera ID: ', session['camera_id'] )
            # print ('Request: 1 Cam ID: ',session['camera_id'])
            if not session['camera_id'] == request.form.get('action'):
                session['camera_id']=request.form.get('action')
                set_defaults(request.form.get('action'))
            else:
                session['camera_id']=request.form.get('action')
            # print ('Requested: 1 Cam ID: ',session['camera_id'])
            if verbose == 'DEBUG': 
                print ('DEBUG:   Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 1:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 1",session['camera_id'])
        elif  request.form.get('action') == '2':
            if not session['camera_id'] == request.form.get('action'):
                session['camera_id']=request.form.get('action')
                set_defaults(request.form.get('action'))
            else:
                session['camera_id']=request.form.get('action')
            if verbose == 'DEBUG': 
                print ('DEBUG:   Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 2:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 2",session['camera_id'])
        elif  request.form.get('action') == '3':
            print ('Request: 3 Cam ID: ',session['camera_id'])
            if not session['camera_id'] == request.form.get('action'):
                session['camera_id']=request.form.get('action')
                set_defaults(request.form.get('action')) 
            else:
                session['camera_id']=request.form.get('action')
            print ('Requested: 3 Cam ID: ',session['camera_id'])
            if verbose == 'DEBUG':
                print ('DEBUG:   Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 3:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])

            # print("Camera 3",session['camera_id'])
        elif  request.form.get('action') == '4':
            if not session['camera_id'] == request.form.get('action'):
                session['camera_id']=request.form.get('action')
                set_defaults(request.form.get('action')) 
            session['camera_id']=request.form.get('action')
            if verbose == 'DEBUG': 
                print ('DEBUG:   Camera session data:    [{}]'.format(session['camera_id']),sess_defaults[session['camera_id']])
                # print(f"Camera 4:\n         ",session,'\n',sess_defaults,'\n',sess_defaults[session['camera_id']])
            # print("Camera 4",session['camera_id'])
        elif  request.form.get('action') == 'reset':
            # session['camera_id']='reset'
            set_defaults(session['camera_id'],True)     # Send reset to set_defaults()
        elif  request.form.get('action') == 'stop':
            session['camera_id']='stop'
            print('INFO: Stream has been stopped')
            get_frames(session['camera_id'],True)   # Send stop capture to break stream
            return render_template(stop_html)
        elif request.form.get('fs_action') in framesize:
            session['fs_size']=request.form.get('fs_action')
            set_frame_size(session['fs_size'], verbose)
        elif request.form.get('flip_action') in ['0','1']:
            session['flip']=request.form.get('flip_action')
            set_flip_image(session['flip'], verbose)
        elif request.form.get('bpc_action') == '1':
            session['bpc']=request.form.get('bpc_action')
            set_black_point(session['bpc'], verbose)
        elif request.form.get('wb_action') in ['0','1']:
            session['white_balance']=request.form.get('wb_action')
            set_white_balance(session['white_balance'], verbose)
            if verbose == 'DEBUG':
                print('DEBUG: WB  Cam_ID: ',session['camera_id'],' level: ',session['ae_level'],' WB value: ',session['white_balance'])
        elif request.form.get('ae_action') in ae_level_range: # Set exposure level
            session['ae_direction']=request.form.get('ae_action')
            set_ae_exposure(session['ae_direction'], verbose)
            if verbose == 'DEBUG':
                print('DEBUG: AE  Cam_ID: ',session['camera_id'],' level: ',session['ae_level'],' direction: ',session['ae_direction'],session['white_balance'])
        else:
            print("Undefined action")
            # session['camera_id']='1'
            pass # unknown camera ID, pass to video_feed()
    curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')
    if verbose == 'DEBUG': 
        print('DEBUG: {}: Route render:'.format(curr_time),request.method,' Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' Frame Size: ',session['fs_size'],' WB: ',session['white_balance'],' BPC: ',session['bpc'] )
        print('DEBUG: Request form: ',request.form)
    else:
        print('INFO: {}: Route render:'.format(curr_time),request.method,' Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' Frame Size: ',session['fs_size'],' WB: ',session['white_balance'],' BPC: ',session['bpc'] )
    return render_template(index_html)

def create_app():
    print("App created")
    set_defaults('0')
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

    # verbose = check_debug_status()
    # if not session['enabled_debug']:
    #     verbose = debug_level['0']
    #     print ('Debug level set to ',verbose,' and session is: ',session['enabled_debug'])
    # else:
    #     verbose = debug_level['1']
    #     print ('Debug level set to ',verbose,' and session is: ',session['enabled_debug'])
    #     print (f'Session data:\n    ',session)
        
    if args.host_ip:
        print ("Access server using this ip address and port: http://{}:{}".format(network.host_address,host['host_port']))
    else:
        verbose = set_defaults('0')
        if verbose == 'DEBUG':
            print('DEBUG:  Route "/" defaults: Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' Frame Size: ',session['fs_size'],' WB: ',session['white_balance'],' BPC: ',session['bpc'])
            # print (strip_url(url))
            # print ('INFO:   Debug level set to ',verbose,' and session is: ',session['enabled_debug'])
            # print (check_debug_status())
        else:
            print('INFO: Ready to serve camera streams')
        # app.run(debug=True)
        serve(app, host=network.host_address, port=host['host_port'])

else:
    verbose = check_debug_status()
