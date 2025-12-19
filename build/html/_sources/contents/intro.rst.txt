==========
Overview
==========

Introduction
-----------------

This work develops a Mobile Assistive Robotic System (MARS) designed to assist people with disabilities by performing daily tasks such as retrieving objects and helping with meals. MARS uses the ROS2 framework to connect a 7-DOF robotic arm, hybrid gripper, RGB-depth cameras, and a large language model-based planner, enabling integration of vision-based recognition, skill affordance, and natural language task planning. Through real-world experiments in cluttered environments, MARS provides a promising solution for autonomous assistive robots in dynamic home settings.

.. figure:: images/fig_testbed.png
   :alt: Alternative text
   :width: 600px
   :align: center

   Real-world use of a mobile assistive robot. (a) 7-DOF robotic arm on a two-wheeled base. (b) Sweeping water. (c) Picking and placing items.


System Overview
-----------------
.. figure:: images/fig_carerobot_overview.png
   :alt: Alternative text
   :width: 600px
   :align: center

To ensure modularity and seamless integration of various functionalities, the robot operates within a ROS2-based framework, 
as shown in the figure. The system includes:

    - **Frontend**: or user interaction, comprising 

      + **input** modalities (microphone for voice commands, text input, and pre-defined commands) and

      + **output** modalities (display for visual feedback and speaker for audio responses).
    - **main processor**: in the core backend, featuring 

      + a **WebRTC bridge server** for real-time communication and remote access, 
      
      + a **Task Manager** that decomposes high-level natural language prompts into sequences of requests, handles confirmations and feedback loops, and orchestrates task execution using LLM/VLM reasoning, 
      
      + and a **Skill Controller** that manages and executes primitive skills by sending requests to specialized hardware controllers

    - **external computing unit**: for offloading computationally intensive tasks, including 
    
      + a **voice recognition server** for speech-to-text processing and 
      
      + **LLM/VLM servers** for advanced multimodal planning and perception

    - **hardware controller**: layer that interfaces directly with the robot's actuators and sensors,encompassing arm control servers for 
    
      + manipulating the 7-DOF arm and gripper, 
      
      + mobile control servers for navigation, 
      
      + head control servers for orientation, 
      
      + elevator control servers (potentially for vertical reach adjustment), 
      
      + and sensor data publishers for real-time feedback from RGB-depth cameras and other sensors.

This modular architecture divides responsibilities between frontend user interface, backend task orchestration, external AI processing, and low-level hardware control. It enables robust, scalable integration of natural language understanding, vision-based affordance detection, and precise robotic execution in assistive scenarios.

System Details
-----------------

Frontend
********************
.. figure:: images/fig_frontend.png
   :alt: Alternative text
   :width: 600px
   :align: center

The frontend of the system features a user-friendly graphical user interface (GUI) implemented in HTML with integrated WebRTC technology, ensuring cross-platform compatibility and seamless operation on desktops, tablets, and mobile devices. This design prioritizes accessibility for both sighted and blind users by emphasizing voice-based interaction alongside visual elements. 
The interface includes: 

-  **buttons** for predefined commands to facilitate quick task selection, 

- a prominent **image display** area for verifying object recognition results and providing visual confirmation of the robot's perception, 

- a scrolling **message log** to show real-time feedback and status updates from the backend, 

- and **text areas** for entering free-form natural language prompts. 

- Additionally, a prominent **microphone icon** allows users to initiate voice recording with a single click or tap, stop recording with another click to automatically send the audio to the backend for processing, and receive spoken responses from the robot's speaker. 

This voice-centric approach is particularly beneficial for blind users, who may find precise screen touching challenging; they can simply speak directly to the robot or to their paired mobile device to issue commands, with the system providing auditory feedback and confirmations, thereby enabling intuitive and hands-free control in assistive scenarios.

WebRTC Bridge Server
********************
.. figure:: images/fig_webrtc_bridge.png
   :alt: Alternative text
   :width: 600px
   :align: center

The WebRTC Bridge Server serves as a critical communication hub that enables seamless, real-time bidirectional interaction between the client-side frontend (running on mobile devices, tablets, or desktops) and the ROS2-based backend task manager on the robot. 
As illustrated in the figure, it consists of two primary interfaces: 

- a **WebRTC Interface** for client connectivity and 

- a **ROS2 Interface** for integration with the robotic system. 

On the client side, the bridge handles incoming prompts (voice or text commands) via 

- a **Callback mechanism**, 

- **broadcasts** messages (such as status updates, feedback, or spoken responses) to the client, 

- and manages **confirmation loops** by sending Confirm Requests to the client and receiving Confirm Responses. 

On the ROS2 side, it exposes 

- a **Prompt Publisher** to forward user prompts to the Task Manager, 

- an **Observe Subscriber** to receive ongoing messages and feedback, 

- and a **Confirm Service Server** to handle synchronous confirmation requests and responses during task execution. 

This design allows low-latency, secure WebRTC-based remote access over the internet while translating web-friendly protocols into native ROS2 topics and services, ensuring that users—particularly those with disabilities—can reliably control and monitor the assistive robot from any device without direct physical access to the robot's local network.

Task Manager
********************
.. figure:: images/fig_task_manager.png
   :alt: Alternative text
   :width: 600px
   :align: center

The Task Manager is the central orchestration component of the robotic system, 
responsible for translating high-level natural language user prompts into executable sequences of low-level robotic skills. 

- As depicted in the figure, it begins by subscribing to incoming **prompts** from the WebRTC Bridge Server **via a Prompt Subscriber**. 

- Upon receiving a prompt, the **Task Manager invokes the external LLM/VLM-based Task Planning** module, which decomposes the user intent into a structured task plan and generates a sequence of skill requests. 

- To ensure safe and transparent operation—particularly important in assistive scenarios—the Task Manager incorporates an interactive confirmation loop: it sends Confirm Requests to the user through a **Confirm Service Client**, awaits Confirm Responses, and, if the user selects "Terminate" or "Skip," aborts or bypasses the current step accordingly. 

- When the user chooses to continue or when no confirmation is required, the Task Manager proceeds by dispatching a sequence of skill requests to the Skill Servers via dedicated **Skill Clients**. 

- It concurrently collects sequences of responses and feedback from executed skills, which can be fed back into the LLM/VLM for replanning or error recovery if necessary.

This closed-loop design enables robust, user-supervised task execution while leveraging advanced multimodal reasoning for complex, 
long-horizon assistive tasks in unstructured home environments.

LLM-based Task Planning
+++++++++++++++++++
.. figure:: images/fig_llm_task_plan.png
   :alt: Alternative text
   :width: 600px
   :align: center

The LLM/VLM-based Task Planning module serves as the intelligent reasoning core that bridges high-level natural language user commands with executable robotic actions. As shown in the figure, it receives structured prompts from the Task Manager containing the user's intent (e.g., "Give me remote control on the bed") along with a description of the robot's available primitive skills—pick, place, move, find, and inform—which define the system's capabilities for grasping, positioning, navigation, object detection, and environmental reporting. Leveraging multimodal large language (and optionally vision-language) models hosted on an external computing unit, the module decomposes the command into a feasible sequence of skill invocations, outputting a structured program that specifies action_types (e.g., place), target_objects (e.g., remote control), target_locations (e.g., bed), and destination_locations (e.g., the user's position, denoted as "me"). This structured output enables the Task Manager to generate a precise sequence of skill requests while incorporating contextual understanding, such as resolving ambiguous references (e.g., "me" as the user's current location) and handling multi-object or multi-step tasks (as illustrated in the example of delivering both a phone and door key). By grounding planning in the robot's defined skill affordances, the LLM ensures safe, interpretable, and adaptable task execution tailored to dynamic assistive scenarios in home environments.



Skill controller
********************
.. figure:: images/fig_skill_controller.png
   :alt: Alternative text
   :width: 600px
   :align: center
 

The Skill Controller acts as the bridge between high-level task planning and low-level hardware execution, 
managing a set of parameterized primitive skills that encapsulate the robot's core capabilities. 
As illustrated in the figure, incoming skill requests from the Task Manager's Skill Clients are 
received and handled by dedicated Skill Servers for each primitive action: 

- **Move** (for mobile base navigation), 

- **Find** (for object detection and localization using onboard cameras), 

- **Pick** (for grasping objects with the arm and hybrid gripper, optionally using suction), and 

- **Place** (for positioning and releasing objects at specified locations). 

Each Skill Server processes its requests by invoking the appropriate Device Control Clients, 
which include specialized clients for arm control, mobile base control, head orientation control,
elevator vertical adjustment, and sensor data subscription to obtain real-time RGB-D images and 
other environmental feedback. 

Critically, the Find and Pick skills leverage an external VLM Server for advanced vision-based reasoning—such 
as object recognition, affordance detection, and grasp planning in cluttered scenes—ensuring robust perception 
before physical interaction. 

The arrows indicate the primary serving direction: requests flow from Skill Clients to Skill Servers, 
then to Device Control Clients that directly interface with the Hardware Controller, 
while perceptual data (especially from sensors and VLM) flows back upward to inform ongoing skill execution and
provide feedback to the Task Manager. 

This hierarchical, modular design enables reliable, vision-guided performance of atomic actions 
while maintaining clear separation between planning, skill abstraction, and hardware-specific control.


Skill Workflow
+++++++++++++++++++
.. figure:: images/fig_skills.png
   :alt: Alternative text
   :width: 600px
   :align: center



The skill workflow in the Skill Controller is designed to achieve robust autonomous execution through 
hierarchical precondition checks and built-in retry mechanisms, 
ensuring reliable performance in real-world cluttered environments. 
As depicted in the flowchart, when a high-level skill is invoked, 
the system first evaluates necessary preconditions and, if unmet,
 recursively triggers lower-level skills with a fixed number of retries (experimentally set to n=2) 
 to increase success rates without excessive delay. 

 - For the **Place skill**, it initially checks if the object is grasped; if not, it calls Pick. It then verifies arrival at the destination; if not, it triggers Move (with up to 2 navigation attempts). Only upon satisfying both conditions does it execute the final place action. 
 
 - The **Pick skill** checks if the object is already found; if not, it invokes Find (allowing up to 2 detection attempts using the VLM Server), followed by the grasp execution if successful. 
 
 - Similarly, the **Find skill** first confirms whether the robot is at an optimal target viewpoint; if not, it calls Move (with up to 2 trials) before performing object detection and localization. 
 
 - The base Move skill directly executes navigation with its own internal robustness. 
 
 
At each execution step (move_exec, find_exec, pick_exec, place_exec), 
failure after the allotted retries propagates upward, causing the calling skill to return failure. 
This retry-augmented cascaded structure minimizes planning complexity at the Task Manager level 
while providing fault tolerance through limited reattempts,
making the system particularly effective for assistive tasks where occasional perception or 
motion errors are common.





SDK Overview 
-----------------

1. Installation: see the :ref:`install` section for more details.


2. Task-based packages

To reduce the complexity and time consumming while repeatdly coding  callback function or handle different kinds of connections, 
we developed task-based pakages that aids the easy implementation of the system. The packages inludes:

 -  pyconnect: Enables repeated communication between nodes and functionality PCs with easy ROS node setup and message logging. 

 - pyrecognition: Implements popular recognition functions (e.g., grasp detection, object detection, instance segmentation, VLM)

 - carerobotapp: ROS2 Nodes Implementation

 - pyinterfaces: Represents frequently used terms and utilities (e.g., instances, masks, boxes, grasp pose, place pose)

 - rosinterfaces: ROS2 Data Interfaces

3. Manual: see the :ref:`manual` section for more details.

4. Examples: see the :ref:`examples` section for more details.