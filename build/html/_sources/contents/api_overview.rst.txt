=============
APIs Overview
=============


ROS2 Nodes Implementation
===================

**Git Repository: app_carerobot**

Nodes:

- node_prompt: Captures user input (keyboard or voice, TBD) and RGB sensor image (optional). Creates and sends task plan to node_taskmanager.

- node_taskmanager: Manages skill client agents, assigns tasks to appropriate agents, and forwards jobs to corresponding servers.

 - node_skill_servers: Receives requests from node_taskmanager and executes sequences on device servers.

 - skills package: Contains all robot skills.


General Data and Node Communication Implementation
==========================

**Purpose**: Enables repeated communication between nodes and functionality PCs with easy ROS node setup and message logging.

**Git Repository: pyconnect**

**Components**

- tcp/ip: TCP/IP server and client implementation.

- ros: ROS2 topic pub/sub, service server/client, and action server/client.

- llm: LLM client for OLLAMA and ChatGPT.


ROS2 Data Interfaces
==========================

**Git Repository: rosinterfaces**

**Components**

Python Data Interfaces
==========================

**Purpose**: Represents frequently used terms and utilities (e.g., instances, masks, boxes, grasp pose, place pose).

**Git Repository: pyinterfaces**



Python Recognition Function Implementation
==========================

**Purpose**: Implements popular recognition functions (e.g., grasp detection, object detection, instance segmentation, VLM).

**Git Repository: pyrecognition**




