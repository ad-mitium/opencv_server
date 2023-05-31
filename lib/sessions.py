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
    # The following four items should only be changed when initializing or resetting the camera
    'flip' : '1',
    'ae_compensation' : '1',
    'gain_ceiling' : '2',
    'quality' : '4',
    'enabled_debug' : False

}

sess_defaults = {
    # AE direction, BPC, FS_size, WB , flip, aec, gain_ceiling, quality
    '1':['0','0','9','0','1','1','2','4'] ,
    '2':['0','0','11','1','0','1','2','4'] ,
    '3':['0','0','11','1','0','1','2','4'] ,
    '4':['0','0','9','0','0','1','2','4'] ,
    '0':['0','0','9','0','0','1','2','4']      # No camera id, order matters for initialization, leave 0 last
}
