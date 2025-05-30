# OpenCV Server with Flask and ESP32 Camera

## Overview (or why I am doing this)

Playing around with some [ESP32 WiFi boards](https://arduino-esp8266.readthedocs.io/en/latest/index.html) with onboard [cameras](https://www.arducam.com/ov2640/) and realized that the [built-in web server](https://github.com/espressif/arduino-esp32) is rather bad. Besides that, the HTML is in a binary formatted file that you have to convert just to make modifications to the HTML.  Then, after modifications are completed, conversion back to binary before uploading the code to the ESP32 board.

I also noted that the video stream was being pushed out on port 81. It occurred to me that I could bypass the demo code and display it on another computer with a bit of Python and Flask.

It should be obvious, but it has to be put in writing, that you use this at your own risk.

## Usage

There are two ways to use this script.  The first method is to run the script in a command line.  The second method involves using a WSGI capable application.

### Using command line

    python3 ocv_server_single_form.py [-d,-ip,-h,-v]

When using this script in command line mode, several flags are accessible.

    -d, --debug-level           Enable DEBUG mode, defaults to INFO
    -ip, --host-ip              Shows the host IP address detected (or assigned by 
                                    user) and designated PORT

    -h, --help                  Shows the help dialogue
    -v, --version               Shows the current version number

### Using Waitress WSGI

[Waitress](https://pypi.org/project/waitress/) is not the only WGSI application out there, it is just the one I've tested my script on at this time. It can be started by designating the ```HOST IP``` and ```PORT``` directly:

    waitress-serve --host <HOST IP> --port <HOST PORT> --call ocv_server_singelform:create_app

### Configuring the script

The script is configured by the files in the config folder.  Change the ```host['host_ip']``` field and uncomment the appropriate ```host_address``` variable in ```network.py``` if you want to hard code the IP address.

## Known Issues

### Dropped WiFi connections and invalid data

The ESP32 seems to drop connection or send invalid data quite often.  That may be an issue with my wireless environment or it could be the ESP32 wasn't intended to be on 24/7. These devices appear to be rather fragile with respect to connectivity.

There are two things I have implemented to address the dropped connections and invalid data.  I made changes to the demo code and I added some javascript in ```index.html``` to reload the page every few minutes.

#### Changes made to demo code

For the sake of documenting all of the changes I made in one place, I made some modifications to the widely available demo [ESP32 code](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer). The modifications involved ensuring that the device would check every 5 minutes to see if it lost WiFi connection, and if it did, it would then attempt to reconnect.

Below are the modifications made:

    unsigned long previousMillis = 0;
    unsigned long interval = 300000;

    void loop() {
        unsigned long currentMillis = millis();
        if (currentMillis - previousMillis >=interval){
            switch (WiFi.status()){
            case WL_NO_SSID_AVAIL:
                Serial.println("Configured SSID cannot be reached");
                break;
            case WL_CONNECTED:
                Serial.println("Connection successfully established");
                break;
            case WL_CONNECT_FAILED:
                Serial.println("Connection failed");
                break;
            case WL_CONNECTION_LOST:
                Serial.println("Reconnecting");
                WiFi.begin(ssid, password);
                break;
            }
            Serial.printf("Connection status: %d\n", WiFi.status());
            Serial.println("");
            previousMillis = currentMillis;
        }
    }

### Session handling

Furthermore, this is not production level code, so I've decided to sidestep implementing session handling with a Dict. You are free to implement it if you wish.

### ```swscaler``` invalid slice messages

Changing the image resolution to a larger resolution causes OpenCV to complain about invalid slices. This will not be fixed because the fix requires changing how OpenCV handles image size changes. Either that or suppressing OpenCV error output outright.  I have not been successful in catching OpenCV errors.

It occurs at all times, but is most frequently observed when forcing all video streams to the same size in multiple camera view for image concatenation.

### Issues specific to Multiple Camera view

#### Heavy CPU usage when stream is lost

Added handling for lost image stream when in multiple camera view. When the ```frame_count``` variable is < 100 frames, CPU usage jumps to 100%. For now, the ```frame_count``` is set to 30 seconds worth of frames to reduce CPU usage to managable levels. I haven't decided if it is worth the compute cost to add this check to the single camera view.

#### Setting buttons default to camera 4 in multiple camera view

A "feature" when changing settings in multiple camera view is that it defaults to camera 4. However, there is a long delay before the server shows an image. Long enough for a user to think the application is not working. It is due to some legacy session handling when there wasn't a multiple camera view. It's caused a lot of headaches as well as workarounds to maintain compatibility and may very well require a re-write.

#### After a while all feeds become "unavailable"

Over time, all feeds eventually show unavailable despite only one feed reporting errors. The forced refresh helps address this. Ultimately, there is a logic error that needs to be addressed with respect to exception handling when concatenating each of the rows of video.

## Required python libraries

* flask
* opencv-python-headless
* numpy (required by opencv-python-headless)
* waitress
* netifaces (Optional if you hardcode your host ip address)

## ToDo

* ~~Implement per Camera ID session handling~~ Completed
* ~~Implement ```flip_image``` button toggling for flipping the image~~ Completed
* ~~Add Camera ID overlay to multiple camera stream view~~ Completed
* ~~Fix lazy session handling of camera ID when changing settings in multiple camera view~~ Completed
* Rewrite route logic and perform actions by action type
* TBD
