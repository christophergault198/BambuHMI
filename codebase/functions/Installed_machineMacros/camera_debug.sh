#!/bin/sh

source /usr/bin/mqtt_access.sh

# Removed the module_choice function to avoid user interaction

function check_camera_online () {
    ret=`cat /sys/devices/platform/ff510000.i2c/i2c-1/1-0036/sensor_online`
    if [ $ret -eq 1 ];then
        echo "isp camera is online"
    else
        echo "isp camera is offline"
    fi

    ls /dev/v4l/by-id >& /dev/null
    if [ $? -eq 0 ]; then
        echo "usb camera is online"
    else
        echo "usb camera is offline"
    fi
}

function stop_xcam() {
    killall service_check.sh
    kill -9 `pidof xcam`
}

function start_camera() {
    json="{ \
        \"print\":{\"command\":\"gcode_line\", \"sequence_id\":\"2001\", \"param\":\"M973 S3\"} \
    }"
    mqtt_pub "$json"
}

function stop_camera() {
    json="{ \
        \"print\":{\"command\":\"gcode_line\", \"sequence_id\":\"2001\", \"param\":\"M973 S4\"} \
    }"
    mqtt_pub "$json"
}

function isp_camera_1920_1080_to_lcd() {
    stop_xcam
    sleep 1
    rkisp_demo -r -w 1920 -h 1080 -f NV12 -d /dev/video13 -v
}

function isp_camera_640_480_to_lcd() {
    stop_xcam
    sleep 1
    rkisp_demo -r -w 640 -h 480 -f NV12 -d /dev/video13 -v
}

function isp_camera_640_480_yuv_dump() {
    stop_xcam
    sleep 1
    rkisp_demo -r -w 640 -h 480 -f NV12 -d /dev/video13 -o /userdata/dump.yuv -n 100
}

function clean_camera_log() {
    killall camera_monitor.sh
    sleep 1
    rm -f /userdata/log/camera_log
    rm -f /userdata/log/camera_raw_log
    sync
    camera_monitor.sh &

}

function show_total_mipi_log() {
    cat /userdata/log/camera_log
}

function show_raw_mipi_log() {
    cat /userdata/log/camera_raw_log
}

function show_current_mipi_cnt() {
    clk_isp=`cat /proc/rkisp0  | grep -w clk_isp | awk '{print $2}'`
    if [ "$clk_isp"x == "20000000"x ]; then
        echo "camera stream off now"
    else
        cat /proc/rkisp0 | grep Cnt
    fi
}

function show_interrupts() {
   cat /proc/interrupts | grep vsync
   cat /proc/interrupts | grep time_sync
   cat /proc/interrupts | grep rkisp
}

function enable_ipcam_recorder() {
    echo -n 2 > /tmp/device/print_state_mc
}

function disable_ipcam_recorder() {
    echo -n 1 > /tmp/device/print_state_mc
}

# Directly set MODULE_CHOICE to 10
MODULE_CHOICE=10

module_test()
{
    case ${MODULE_CHOICE} in
        1)
            check_camera_online
            ;;
        2)
            start_camera
            ;;
        3)
            stop_camera
            ;;
        4)
            show_total_mipi_log
            ;;
        5)
            show_raw_mipi_log
            ;;
        6)
            show_current_mipi_cnt
            ;;
        7)
            clean_camera_log
            ;;
        8)
            isp_camera_1920_1080_to_lcd
            ;;
        9)
            show_interrupts
            ;;
        10)
            isp_camera_640_480_to_lcd
            ;;
        11)
            isp_camera_640_480_yuv_dump
            ;;
        12)
            enable_ipcam_recorder
            ;;
        13)
            disable_ipcam_recorder
            ;;
    esac
}

# Removed the call to module_choice to avoid waiting for user input
module_test
