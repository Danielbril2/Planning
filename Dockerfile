FROM docker.io/osrf/ros:humble-desktop-full

# Update all packages
RUN apt-get update && apt-get upgrade -y

# Install extra packages
RUN apt-get install gdb -y

# Rosdep update
RUN rosdep update

# Source the ROS humble setup file
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
