#raspivid -t 0 -h 480 -w 640 -fps 25 -hf -b 1000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! udpsink host=10.25.46.36 port=5000
raspivid -t 0 -h 480 -w 640 -fps 25 -hf -b 1000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! tcpserversink host=10.25.46.36 port=5000