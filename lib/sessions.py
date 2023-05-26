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
    'enabled_debug' : False

}

sess_defaults = {
    # AE direction, BPC, FS_size, WB
    '0':['0','0','9','0'] ,     # No camera id
    '1':['0','0','9','0'] ,
    '2':['0','0','11','1'] ,
    '3':['0','0','11','1'] ,
    '4':['0','0','9','0'] 
}
