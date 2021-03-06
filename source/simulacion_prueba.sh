#!/usr/bin/env bash
##copiar achivos
cp -r ~/catkin_ws/src/offbnode/models/iris_gimbal ~/Firmware/Tools/sitl_gazebo/models
cp -r ~/catkin_ws/src/offbnode/worlds ~/Firmware/Tools/sitl_gazebo
cp -r ~/catkin_ws/src/offbnode/init.d/* ~/Firmware/ROMFS/px4fmu_common/init.d-posix
cd
cd .ros/
cd eeprom/
rm parameters
#rm *.log
#rm dataman
#rosclean purge


cd ~/Firmware
DONT_RUN=1 make px4_sitl_default gazebo_iris
#////////
#para solo lanzar sim
source ~/catkin_ws/devel/setup.bash    # (optional)
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
#roslaunch px4 posix_sitl.launch 
#roslaunch offbnode mavros_posix_sitl.launch
#roslaunch offbnode mavros_posix_sitl.launch vehicle:=typhoon_h480
roslaunch offbnode mundo_y_dron.launch vehicle:=iris_gimbal world:="$(find mavlink_sitl_gazebo)/worlds/p3.world"
reset
