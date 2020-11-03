#
# Building a Docker Image with
# the Latest Ubuntu Version and
# Basic Python Install
#
# Python for Finance, 2nd ed.
# (c) Dr. Yves J. Hilpisch
#

# latest Ubuntu version
FROM ubuntu:latest
RUN apt-get update  # updates the package index cache
RUN apt-get upgrade -y  # updates packages
# installs system tools
RUN apt-get install -y bzip2 gcc git htop screen vim wget
RUN apt-get upgrade -y bash  # upgrades bash if necessary
RUN apt update && apt upgrade -y

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh
RUN bash Miniconda.sh -b
ENV PATH="/root/miniconda3/bin:${PATH}"
# INSTALL PYTHON LIBRARIES
RUN conda update -y conda python # updates conda & Python (if required)
RUN conda install -y pandas  # installs pandas
RUN conda install -y ipython  # installs IPython shell
RUN conda install -y pyyaml  # installs IPython shell
# prepend the new path
ENV PATH /root/miniconda3/bin:$PATH

# execute IPython when container is run
CMD ['bash']