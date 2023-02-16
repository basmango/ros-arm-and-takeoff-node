FROM ros:noetic-ros-core

LABEL maintainer Bassam Pervez

# Trick to get apt-get to not prompt for timezone in tzdata
ENV DEBIAN_FRONTEND=noninteractive

ARG STARTDELAY=5
ENV STARTDELAY=$STARTDELAY

# Install gstreamer dependencies 
RUN sudo apt-get update && sudo apt-get install -y  git python3-catkin-tools 

RUN sudo apt-get install -y python3 python3-pip  ros-noetic-mavros ros-noetic-mavros-msgs


COPY requirements.txt /
COPY controller.py  /



COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh 


