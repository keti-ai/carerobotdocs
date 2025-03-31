=============
Getting Started
=============

This guide provides step-by-step instructions to set up the necessary environment for your project, including CUDA, Docker, dependencies, and system execution.

---

Cuda Installation (Host PC)
===================

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


Docker Installation
===================

To set up a Docker containerized environment for your project, follow these steps:

1. Clone the Docker configuration repository:

   .. code-block:: bash

       git clone https://github.com/keti-ai/dockers.git
       cd dockers

2. Build the Docker image with the required specifications:

   .. code-block:: bash

       ./build_image.sh <UBUNTU_VERSION> <CUDA_VERSION> <ROS_DISTRO>

   Replace `<UBUNTU_VERSION>`, `<CUDA_VERSION>`, and `<ROS_DISTRO>` with your specific environment settings.

   Support versions:
   
   - Ubuntu20.04, 22.04 (recommeded)

   - CUDA 11.1.1, 11.7.1(recommeded), 12.1.0, 12.4.1, 12.6.3

   - ROS2: foxy, humble (recommeded)
   

3. Create and run a Docker container:

   .. code-block:: bash

       ./build_container.sh <UBUNTU_VERSION> <CUDA_VERSION> <ROS_DISTRO> <CONTAINER_NAME> <SHARE_DIR> <SSH_PORT> <PORT_MAP>

   - `<CONTAINER_NAME>`: Name of the container
   - `<SHARE_DIR>`: Shared directory path
   - `<SSH_PORT>`: SSH port number
   - `<PORT_MAP>`: Additional port mappings

---

Dependencies Installation
===================

Download Required Repositories
------------------------------

Clone the following repositories to set up the necessary dependencies:

.. code-block:: bash

       git clone https://github.com/CASIA-IVA-Lab/FastSAM.git
       git clone https://github.com/IDEA-Research/GroundingDINO.git
       git clone https://github.com/keti-ai/pyrecognition.git
       git clone https://github.com/keti-ai/pyconnect.git
       git clone https://github.com/keti-ai/pyinterfaces.git
       git clone https://github.com/keti-ai/rosinterfaces.git

Install Python Packages
-----------------------

Install the repositories as editable Python packages:

.. code-block:: bash

       pip install -e FastSAM
       pip install -e GroundingDINO
       pip install -e pyrecognition
       pip install -e pyconnect
       pip install -e pyinterfaces

Install ROS Interfaces
---------------------

1. Create a symbolic link to `rosinterfaces` inside the ROS2 workspace:

   .. code-block:: bash

       ln -s rosinterfaces ~/ros2_ws/src

2. Build the ROS package:

   .. code-block:: bash

       cd ~/ros2_ws
       colcon build --packages-select rosinterfaces


System Execution
===================

Robot and Device Server Execution in Edge PC
-------------------------------------------

Start the various components required for the robot and sensors:

.. code-block:: bash

       robot   # Initializes robot arm, elevator, head, etc.
       femto   # Runs the Femto camera
       hand    # Runs the wrist camera

Ollama Server Execution in Server PC
------------------------------------

To enter the running Ollama server’s container:

.. code-block:: bash

       sudo docker exec -it ollama /bin/bash

VLM Server Execution in Server PC
----------------------------------

Start the Vision-Language Model (VLM) server:

.. code-block:: bash

       python3 -m pyrecognition.run_server server_type=tcp port=8801 detector=groundedsam

ROS Node Execution in Control PC
--------------------------------

Navigate to the ROS application directory and run the necessary nodes:

.. code-block:: bash

       cd app_carerobot
       python3 node_prompt.py
       python3 node_taskmanager.py
       python3 node_skill_servers.py

Configuration Files
----------------------

For further configurations, refer to the `app_carerobot.configs` directory.
