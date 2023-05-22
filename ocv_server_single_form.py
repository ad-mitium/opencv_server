#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023

import os, argparse, requests
import netifaces
from time import strftime
from flask import Flask, render_template, Response, request
# from flask_session import Session     # This isn't production code, so not putting the effort to safely transfer variable data
from config.cameras import camera_list as cam_list
from config.cameras import ae_level as ae_level_range
from config.cameras import framesize, white_balance
from config.network import host
from config.network import debug_level
import config.network as network
from lib import version as ver
import cv2

app = Flask(__name__, template_folder='html')

version_number = (0,0,3)

session = {    # Not the safest method to pass data between routes
    'camera_id' : '1' ,
    'ae_level' : '0' ,
    'ae_direction' : '0' ,
    'fs_size' : '11' ,
    'flip' : '0' ,
    'bpc' : '0' ,
    'white_balance' : '1'

}

def strip_url(url): 
    from urllib.parse import urlparse

    parts = urlparse(url)
    domain_addr = parts.scheme + '://' + parts.netloc.split(':')[0] 
    if verbose == 'DEBUG':
        print (domain_addr)
    return domain_addr

def set_ae_exposure(ae_dir): 
    from time import sleep

    if not session['camera_id'] == 'stop':
        url_stripped = strip_url(cam_list[str(session['camera_id'])])

        print('Curent ae_level: ',session['ae_level'],' direction: ', ae_dir)
        
        if ae_dir == '0':
            ae_val = '0'
        else:
            ae_val = int(session['ae_level']) + int(ae_dir)
        
        # if verbose == 'DEBUG':
            # print ('AE val: ',ae_val) 
            # print(type(ae_val) , type(session['ae_level']))
        
        if str(ae_val) in ae_level_range:
            url = url_stripped + '/control?var=ae_level&val='+str(ae_val)
            session['ae_level'] = str(ae_val)
            # if verbose == 'DEBUG':
            #     print('URL: ',url,' level: ',session['ae_level'], end='')
            get_request = requests.get(url)
            get_status_code = get_request.status_code
            # if verbose == 'DEBUG':
            #     print (' status code: ',get_request.status_code)
        else:
            print ('Value out of range: ',ae_val, end=' ')
            url = 'No request made, AE value out of range ' # No url if you don't make a request
            get_status_code = 'No request made, AE value out of range ' # No status code if you don't make a request
            if ae_val > 2:      # Put ae_val back in range for DEBUG display purposes, wasn't changed in session['ae_level']
                ae_val = 2
            elif ae_val < -2:
                ae_val = -2
            if verbose == 'DEBUG':
                print('AE level reset to: ',ae_val)
            else:
                print('')


        if verbose == 'DEBUG':
            # print ("AE set to: ",ae_dir, url)
            print ("AE set to: ",ae_val,'URL: ',url, ' level: ',session['ae_level'],' status code: ',get_status_code) 
        # sleep(2)

def set_black_point(bpc_mode): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    url = url_stripped + '/control?var=bpc&val='+str(bpc_mode)
    get_request = requests.get(url)
    if verbose == 'DEBUG':
        print (get_request.status_code)
        print ("Black point correction set to: ",bpc_mode)

def set_flip_image(mirror_mode): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    hmirror_adjust = url_stripped + '/control?var=hmirror&val='+str(mirror_mode)
    get_request = requests.get(hmirror_adjust)
    if verbose == 'DEBUG':
        print (get_request.status_code)

    vfliup_adjust = url_stripped + '/control?var=vflip&val='+str(mirror_mode)
    get_request = requests.get(vfliup_adjust)
    if verbose == 'DEBUG':
        print (get_request.status_code)
        print ("Image mirror set to: ",mirror_mode)

def set_frame_size(frame_size): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    url = url_stripped + '/control?var=framesize&val='+str(frame_size)
    get_request = requests.get(url)
    if verbose == 'DEBUG':
        print (get_request.status_code)
        print ("Frame size set to: ",frame_size)

def set_white_balance(wb_mode): 
    url_stripped = strip_url(cam_list[str(session['camera_id'])])

    url = url_stripped + '/control?var=wb_mode&val='+str(wb_mode)
    get_request = requests.get(url)
    if verbose == 'DEBUG':
        print (get_request.status_code)
        print ("WB set to: ",wb_mode)

def get_frames(cam_id,stop_capture=False): 
    # strip_url(cam_list[str(cam_id)])

    video = cv2.VideoCapture(cam_list[str(cam_id)])
    # print('{}'.format('ID= {cam_id}, {stream}'.format(cam_id=cam_id,stream=cam[str(cam_id)]) if enabled_debug else '',end='\r'))

    while True:
        success, frame = video.read()
        if not success:
            print('Error getting video frame')
            break
        elif stop_capture:
            video.ReleaseCapture()
            break
        else:
            ret_status, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/', methods=["GET"])
@app.route('/video_feed/<string:id>/', methods=["GET"]) # Overload to get direct feed
def video_feed(id='1'):
    id=session.get('camera_id')

    if verbose == 'DEBUG':
       print('Camera ID: ',id)
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

    # print (verbose)

    if request.method == 'POST':
        if request.form.get('action') == '1':
            session['camera_id']=request.form.get('action')
            # print("Camera 1",session['camera_id'])
        elif  request.form.get('action') == '2':
            session['camera_id']=request.form.get('action')
            # print("Camera 2",session['camera_id'])
        elif  request.form.get('action') == '3':
            session['camera_id']=request.form.get('action')
            # print("Camera 3",session['camera_id'])
        elif  request.form.get('action') == 'stop':
            session['camera_id']='stop'
            get_frames(session['camera_id'],True)
            return render_template(stop_html)
        elif request.form.get('fs_action') in ['9','11']:
            session['fs_size']=request.form.get('fs_action')
            set_frame_size(session['fs_size'])
        elif request.form.get('flip_action') in ['0','1']:
            session['flip']=request.form.get('flip_action')
            set_flip_image(session['flip'])
        elif request.form.get('bpc_action') == '1':
            session['bpc']=request.form.get('bpc_action')
            set_black_point(session['bpc'])
        elif request.form.get('wb_action') in ['0','1']:
            session['white_balance']=request.form.get('wb_action')
            set_white_balance(session['white_balance'])
            if verbose == 'DEBUG':
                print('WB  Cam_ID: ',session['camera_id'],' level: ',session['ae_level'],' WB value: ',session['white_balance'])
        elif request.form.get('ae_action') in ae_level_range: # Set exposure level
            session['ae_direction']=request.form.get('ae_action')
            set_ae_exposure(session['ae_direction'])
            if verbose == 'DEBUG':
                print('AE  Cam_ID: ',session['camera_id'],' level: ',session['ae_level'],' direction: ',session['ae_direction'],session['white_balance'])
        else:
            print("Undefined action")
            # session['camera_id']='1'
            pass # unknown camera ID, pass to video_feed()
    curr_time = strftime('%m-%d-%Y ') + strftime('%H:%M:%S')
    if verbose == 'DEBUG' or verbose == 'INFO': 
        print('{}: Route render:'.format(curr_time),request.method,' Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' WB: ',session['white_balance'] )
    return render_template(index_html)

def create_app():
    return app

if __name__ == '__main__':
    from waitress import serve
    verbose = debug_level['0']
    # enabled_debug=False
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

    enabled_debug = args.debug_level

    if enabled_debug:
        verbose = debug_level['1']
    # else:
        
    if args.host_ip:
        print ("Access server using this ip address and port: http://{}:{}".format(network.host_address,host['host_port']))
    else:
        if verbose == 1:
            print('Route "/" defaults: Cam_ID: ',session['camera_id'],' AE level: ',session['ae_level'],' WB: ',session['white_balance'])
            print (strip_url(url))
        # app.run(debug=True)
        serve(app, host=network.host_address, port=host['host_port'])

