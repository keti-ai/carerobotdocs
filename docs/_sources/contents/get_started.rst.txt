=============
Getting Started
=============

This guide provides step-by-step instructions to set up the necessary environment for your project, including CUDA, Docker, dependencies, and system execution.

---

Host PC Installation
===================

GPU Driver Installation
------------------------

**Prerequisites:**
- Ubuntu version **20.04 or later** (22.04 recommended)

Steps to Install CUDA Drivers:

1. Add the official graphics drivers repository:

   .. code-block:: bash

       sudo add-apt-repository ppa:graphics-drivers/ppa
       sudo apt update
       reboot

2. After rebooting, open **Software & Updates** → **Additional Drivers** and select the appropriate driver for your GPU.
3. Apply the changes and reboot the system:

   .. code-block:: bash

       reboot


Dependencies Installation
-------------------------

   .. code-block:: bash

       sudo update
       sudo apt install terminator htop  -y 
       sudo apt install python3-dev  python3-venv python-pip -y


Docker  and nvidia docker toolkit Installation
--------------------

https://docs.docker.com/engine/install/ubuntu/


https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html


Add some custom useful alias (Optional)
----------------------------------------

.. code-block:: bash

       # utils
       alias chown_keti='sudo chown -R keti .'
       alias sb='source ~/.bashrc'
       alias eb='sudo gedit ~/.bashrc'
       alias nb='nano ~/.bashrc'
       alias about_pc='lsb_release -a'
       alias create_py_simple_pkg='cookiecutter https://github.com/mtbui2010/python_pkg_simple_template.git'
       alias vscode='sudo code --no-sandbox --user-data-dir ~/.vscode_cache'
       alias run_pyvir='source ~/.pyvir/bin/activate'

       #docker
       alias docker_start='sudo docker start'
       alias docker_stop='sudo docker stop'
       alias docker_run='sudo docker run -it'
       alias docker_watch='sudo watch docker ps -a'
       alias image_watch='sudo watch docker image ls -a'
       alias image_rm='sudo docker image rm'


       #functions
       dockerexec() {
       xhost local: & sudo docker start "$@" & sudo docker exec -it "$@" /bin/bash
       }
       dockerrm() {
       sudo docker stop "$@" && sudo docker rm "$@"
       }
       gitpush() {
       git add . .gitignore && git commit -m "$@" && git push
       }
       runa() {
       container_name="$1"  # First argument is the container name
       shift 1              # Remove the first two arguments, leaving only additional script arguments
       
       xhost +
       sudo docker start "$container_name"
       sudo docker exec -it "$container_name" /bin/bash -c \
       "source ~/.bashrc && source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash && $@"
       }


Install and configure SSH and FTP server (Optional)
--------------------------------------------------

   .. code-block:: bash
       sudo apt install terminator htop openssh-server vsftpd  -y 
       sudo ufw allow ssh
       sudo systemctl start ssh

Configure FTP

   .. code-block:: bash

       #!/bin/bash
       set -e

       FTP_DIR="/media/keti/workdir"
       FTP_USER="keti"

       echo "🛠 Backing up original config..."
       sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.bak

       echo "📝 Writing new vsftpd config..."
       sudo tee /etc/vsftpd.conf > /dev/null <<EOL
       listen=YES
       listen_ipv6=NO
       anonymous_enable=NO
       local_enable=YES
       write_enable=YES
       local_umask=022
       chroot_local_user=YES
       allow_writeable_chroot=YES
       user_sub_token=\$USER
       local_root=${FTP_DIR}
       pasv_enable=YES
       pasv_min_port=10000
       pasv_max_port=10100
       EOL

       echo "📁 Setting permissions for $FTP_DIR..."
       sudo chown -R "$FTP_USER":"$FTP_USER" "$FTP_DIR"
       sudo chmod -R 755 "$FTP_DIR"

       echo "🔁 Restarting vsftpd..."
       sudo systemctl restart vsftpd
       sudo systemctl enable vsftpd

       echo "✅ FTP setup complete. You can now FTP into this machine with your user account."


Test SSH and FTP servers

   .. code-block:: bash

       ssh keti@0.0.0.0
       ftp 0.0.0.0



Edge and Control PCs Container Installation
===================

0. Git credential:

   .. code-block:: bash

       git config --global credential.helper store
       

To set up a Docker containerized environment for your project, follow these steps:

1. Build containers

- Clone the Docker configuration repository:

   .. code-block:: bash

       git clone https://github.com/keti-ai/dockers.git
       cd dockers


- Build the Docker image with the required specifications:

   .. code-block:: bash

       ./build_image.sh <UBUNTU_VERSION> <CUDA_VERSION> <ROS_DISTRO>

   Replace `<UBUNTU_VERSION>`, `<CUDA_VERSION>`, and `<ROS_DISTRO>` with your specific environment settings.

   Support versions:
   
   - Ubuntu20.04, 22.04 (default)

   - CUDA 11.1.1, 11.7.1(default), 12.1.0, 12.4.1, 12.6.3

   - ROS2: foxy, humble (default)
   

- Create and run a Docker container:

   .. code-block:: bash

       ./build_container.sh <UBUNTU_VERSION> <CUDA_VERSION> <ROS_DISTRO> <CONTAINER_NAME> <SHARE_DIR> <SSH_PORT> <PORT_MAP>

   - `<CONTAINER_NAME>`: Name of the container [default: kcare]
   - `<SHARE_DIR>`: Shared directory path [default: /media/keti/workdir/projects]
   - `<SSH_PORT>`: SSH port number        [default: 2222]
   - `<PORT_MAP>`: Additional port mappings [default: 8000-8099:8000-8099]


Servere PC Installation
===================

   .. code-block:: bash
       
       cd dockers
       ./build_recognition_container.sh <SSH_PORT> <PORT_MAP> <SHARE_DIR> <IMAGE_NAME> <CONTAINER_NAME>
   
   - `<IMAGE_NAME_NAME>`: Name of the image [default: mtbui2010/ubuntu22:cuda11.7-recognition]
   - `<CONTAINER_NAME>`: Name of the container [default: reg_u22cu11]
   - `<SHARE_DIR>`: Shared directory path [default: /media/keti/workdir/projects]
   - `<SSH_PORT>`: SSH port number        [default: 2202]
   - `<PORT_MAP>`: Additional port mappings [default: 8000-8099:8000-8099]

       


Clone the following repositories to set up the necessary dependencies:

.. code-block:: bash

       git clone https://github.com/keti-ai/pyrecognition.git
       git clone https://github.com/keti-ai/pyconnect.git
       git clone https://github.com/keti-ai/pyinterfaces.git
       git clone https://github.com/keti-ai/rosinterfaces.git



Install the repositories as editable Python packages:

.. code-block:: bash

       pip install -e pyrecognition
       pip install -e pyconnect
       pip install -e pyinterfaces

Install ROS Interfaces

- Create a symbolic link to `rosinterfaces` inside the ROS2 workspace:

   .. code-block:: bash

       ln -s rosinterfaces ~/ros2_ws/src

- Build the ROS package:

   .. code-block:: bash

       cd ~/ros2_ws
       colcon build --packages-select rosinterfaces


System Execution
===================

Edge PC
-------------------------------------------

Robot and Device Server Execution:

.. code-block:: bash

       robot   # Initializes robot arm, elevator, head, etc.
       femto   # Runs the Femto camera
       hand    # Runs the wrist camera

Server PC
------------------------------------

Ollama Server Execution:

.. code-block:: bash

       sudo docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
       sudo docker exec -it ollama /bin/bash


VLM Server Execution:

.. code-block:: bash

       python3 -m pyrecognition.run_server server_type=tcp port=8801 detector=groundedsam

Control PC
--------------------------------

ROS Node Execution

.. code-block:: bash

       cd app_carerobot
       python3 node_prompt.py
       python3 node_taskmanager.py
       python3 node_skill_servers.py
       

Configuration Files
----------------------

For further configurations, refer to the `app_carerobot.configs` directory.
