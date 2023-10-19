#raspivid -t 0 -h 480 -w 640 -fps 25 -hf -b 1000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! udpsink host=10.25.46.36 port=5000
#raspivid -t 0 -h 480 -w 640 -fps 25 -hf -b 1000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! tcpserversink host=10.25.46.36 port=5000
#raspivid -t 0 -h 480 -w 640 -fps 10 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=10.25.46.36 port=5000


gst-launch-1.0 -v rpicamsrc preview=false ! video/x-raw, width=640, height=480, framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=2000000 ! "video/x-h264, profile=high" ! h264parse ! rtph264pay config-interval=1 mtu=1400 ! udpsink host=10.0.2.15 port=5000
