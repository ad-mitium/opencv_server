# OpenCV Server with Flask and ESP32 Camera

## Overview (or why I am doing this)

Playing around with some [ESP32 WiFi boards](https://arduino-esp8266.readthedocs.io/en/latest/index.html) with onboard [cameras](https://www.arducam.com/ov2640/) and realized that the [built-in web server](https://github.com/espressif/arduino-esp32) is rather bad. Besides that, the HTML is in a binary formatted file that you have to convert just to make modifications to the HTML.  Then, after modifications are completed, conversion back to binary before uploading the code to the ESP32 board.

I also noted that the video stream was being pushed out on port 81. It occurred to me that I could bypass the demo code and display it on another computer with a bit of Python and Flask.

It should be obvious, but it has to be put in writing, that you use this at your own risk.

## Usage

There are two ways to use this script.  The first method is to run the script in a command line.  The second method involves using a WSGI capable application.

    python3 ocv_server_single_form.py

For example, using [Waitress](https://pypi.org/project/waitress/):

    waitress-serve --host <HOST IP> --port <HOST PORT> --call ocv_server_singelform:create_app

This is not the only WGSI application out there, just the one I've tested at this time.

### Configuring the script

The script is configured by the files in the config folder.  Change the ```host['host_ip']``` field and uncomment the appropriate ```host_address``` variable in ```network.py``` if you want to hard code the IP address.

## Issues

### Dropped WiFi connections and invalid data

The ESP32 seems to drop connection or send invalid data quite often.  That may be an issue with my wireless environment or it could be the ESP32 wasn't intended to be on 24/7.

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

### ```GET``` Requests fail

While the code works, there are some issues sending ```GET``` requests to CameraWebServer on the ESP32. Until I can determine where the issue lies with the ```GET``` requests, I'm putting the code up as is.

### Session handling

Furthermore, this is not production level code, so I've decided to sidestep implementing session handling with a Dict. You are free to implement it if you wish.

## ToDo

* Until the issue with ```GET``` requests is resolved, ```WB``` code isn't going to be implemented
* Implement ```frame_size``` for resolution changes, also waiting on the ```GET``` request issue
* TBD
