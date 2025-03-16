#!/usr/bin/env python3
# Authored by Timothy Mui 3/28/2023

session = {    # Not the safest method to pass data between routes
    'camera_id' : '1' ,
    'ae_level' : '0' ,
    'ae_direction' : '0' ,
    'fs_size' : '11' ,
    'flip' : '0' ,
    'bpc' : '0' ,
    'white_balance' : '1',
    # The following five items should only be changed when initializing or resetting the camera
    'flip' : '1',
    'ae_compensation' : '1',
    'ae_dsp' : '0',
    'gain_ceiling' : '2',
    'quality' : '4',
    'enabled_debug' : False,
    'online_status' : True

}

sess_defaults = {
    # AE direction, BPC, FS_size, WB , flip, aec, aec_dsp, gain_ceiling, quality
    (1):[('1'),('0'),('9'),('0'),('1'),('1'),('1'),('2'),('4')] ,
    (2):[('0'),('0'),('11'),('1'),('0'),('1'),('0'),('2'),('4')] ,
    (3):[('-2'),('0'),('11'),('1'),('0'),('1')('0'),,('2'),('4')] ,
    (4):[('-1'),('0'),('9'),('0'),('0'),('1')('0'),,('2'),('4')] ,
    ('0'):['0','0','9','0','0','1','2','4']      # No camera id, order matters for initialization, leave 0 last
}

cam_session = {
    ('1'):{    # Not the safest method to pass data between routes
        'camera_id' : '1' ,
        'ae_level' : '0' ,
        'ae_direction' : '0' ,
        'fs_size' : '11' ,
        'flip' : '0' ,
        'bpc' : '0' ,
        'white_balance' : '1',
        # The following five items should only be changed when initializing or resetting the camera
        'flip' : '1',
        'ae_compensation' : '1',
        'ae_dsp' : '0',
        'gain_ceiling' : '2',
        'quality' : '4',
        'enabled_debug' : False

        },
    ('2'):{    # Not the safest method to pass data between routes
        'camera_id' : '2' ,
        'ae_level' : '0' ,
        'ae_direction' : '0' ,
        'fs_size' : '11' ,
        'flip' : '0' ,
        'bpc' : '0' ,
        'white_balance' : '1',
        # The following five items should only be changed when initializing or resetting the camera
        'flip' : '1',
        'ae_compensation' : '1',
        'ae_dsp' : '0',
        'gain_ceiling' : '2',
        'quality' : '4',
        'enabled_debug' : False

        },
    ('3'):{    # Not the safest method to pass data between routes
        'camera_id' : '3' ,
        'ae_level' : '0' ,
        'ae_direction' : '0' ,
        'fs_size' : '11' ,
        'flip' : '0' ,
        'bpc' : '0' ,
        'white_balance' : '1',
        # The following five items should only be changed when initializing or resetting the camera
        'flip' : '1',
        'ae_compensation' : '1',
        'ae_dsp' : '0',
        'gain_ceiling' : '2',
        'quality' : '4',
        'enabled_debug' : False

        },
    ('4'):{    # Not the safest method to pass data between routes
        'camera_id' : '4' ,
        'ae_level' : '0' ,
        'ae_direction' : '0' ,
        'fs_size' : '11' ,
        'flip' : '0' ,
        'bpc' : '0' ,
        'white_balance' : '1',
        # The following five items should only be changed when initializing or resetting the camera
        'flip' : '1',
        'ae_compensation' : '1',
        'ae_dsp' : '0',
        'gain_ceiling' : '2',
        'quality' : '4',
        'enabled_debug' : False

        },
}
