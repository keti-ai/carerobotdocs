.. _manual:
=============
Manual
=============

This section list commands used to control robot

Refer to DEVICE_CLIENT_CONFIGS in :ref:`device_configs` for more details.

[CLIK  TO SOURCE]

How to use
--------------------

1. Make new skill

.. code-block:: python

       cd carerobotapp/skills
       touch new_skill.py

       # add new_skill to SKILL_LISTS  in carerobotapp.configs.tasks

.. code-block:: python
       # in skills/new_skill.py
       from carerobotapp.skills.recognition import find
       def new_skill(node, **kwargs):
           ret = find(node=node, **kwargs)
           if not ret['isdon']:
               return ret
           YOUR_CODE_HERE

2. Execute new skill

.. code-block:: python

       # Run in 3 different terminals
       python3 -m carerobotapp.node_prompt
       python3 -m carerobotapp.node_taskmanager
       python3 -m carerobotapp.node_skill_servers

.. code-block:: python

       # input in node_prompt running window
       new_skill::[INPUTS]


Init Arm
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Prompt Use 
     - Dev Use
   * - Clear  error 
     - clear_error:: 
     - node.agents['clean_error'].send({})
   * - Enable motion 
     - enable_motion::
     - node.agents['enable_motion'].send({'inputs':0})
   * - Set mode
     - set_mode::[INT]
     - node.agents['set_mode'].send({'inputs':[INT]})
   * - Set state
     - set_state::[INT]
     - node.agents['set_state'].send({'inputs':[INT]})
   * - Init Arm
     - init_arm::
     - .. code-block:: python

              from carerobotapp.skills.goto_ready import init_arm
              init_arm(node=node)

   
Arm Control 
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Usage 
     - Inputs

   * - Fuction 
     - Usage 
     - Inputs
   * - Arm movel
       
     - .. code-block:: python

              # PROMPT USE
              movel::[INPUTS]
              example: movel::x=200, y=700

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.arm import movel
              movel(node=node, x=200, y=700)
       
     - .. code-block:: python
              
              x, y, z 
                 [Default: Current x, y, z]
              dx, dy, dz 
                 [Default: 0]
              wait
                 [Default: True]
              
              Predefined locations:
                 afterpnp:
                     location afetr picking or placing

   * - Arm movej
       
     - .. code-block:: python

              # PROMPT USE
              movej::[INPUTS]
              example: movej::fold

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.arm import movej
              movej(node=node,  inputs='fold')
       
     - .. code-block:: python
              
              r0, r1, r2, r3, r4, r5, r6 
                 [Default: Current joints]
              dr0, dr1, dr2, dr3, dr4, dr5, dr6 
                 [Default: 0]
              wait
                 [Default: True]
              
              Predefined locations:
                 home: home pose
                 ready: ready pose
                 give: give me pose
                 fold: arm fold
                 unfold: arm unfod

   * - Move tool
       
     - .. code-block:: python

              # PROMPT USE
              movet::[INPUTS]
              example: movet::dz=100

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.arm import movel
              movet(node=node, dz=100)
       
     - .. code-block:: python
              
              dx, dy, dz
                 [Default: 0]
              wait
                 [Default: True]
   * - Movel + movet
       
     - .. code-block:: python

              # PROMPT USE
              movelf::[INPUTS]
              example: movelf::x=200, rx=-135

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.arm import movelf
              movelf(node=node, x=200, rx=-135)
       
     - .. code-block:: python
              
              x, y, z 
                 [Default: Current x, y, z]
              dx, dy, dz 
                 [Default: 0]
              rx, ry, rz: Roll, Pitch, Yaw
                 [Default: Current angles]
              drx, dry, drz:
                 [Default: 0]
              wait
                 [Default: True]
              

              
                     
Gripper / Litf/ Head / Mobile Control 
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Usage 
     - Inputs
   * - Grip
       
     - .. code-block:: python

              # PROMPT USE
              grip::[INT]
              example: grip::200

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.grip import grip
              grip(node=node, inputs=200)
       
     - .. code-block:: python
              
              inputs [0, 1000]
              
              Predefined locations:
                 open:
                     inputs=1000
                 close:
                     inputs=0
   * - Lift
       
     - .. code-block:: python

              # PROMPT USE
              lift::[INT]
              example: lift::200

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.grip import grip
              lift(node=node, inputs=200)
       
     - .. code-block:: python
              
              inputs [115, 650]
              
              Predefined locations:
                 lowest:
                     inputs=115
                 highest:
                     inputs=650
   * - Head
       
     - .. code-block:: python

              # PROMPT USE
              moveh::[INPUTS]
              example: moveh::left, straight

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.head import moveh
              moveh(node=node, inputs='left, straight')
       
     - .. code-block:: python
              
              inputs:
                 ry, rz [deg]
                     [Default: current angle]
              
              Predefined locations:
                 front: rz=0
                 lefet: rz=-90
                 right: rz=90
                 straight: ry=-25
                 up: ry=0
                 down: ry=-50
   * - Mobile move
       
     - .. code-block:: python

              # PROMPT USE
              move::[INPUTS]
              example: move::desk

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.mobile import move
              move(node=node, inputs='desk')
       
     - .. code-block:: python
              
              offset_x, offset_y [mm]
                 [Default: in ENV meta]
              offset_yaw [deg]
                 [Default: in ENV meta]
              
                    
Recognition Skills
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Usage 
     - Inputs

   * - Find
       
     - .. code-block:: python

              # PROMPT USE
              find::[INPUTS]
              example: find::banana@desk

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.recognition import find
              find(node=node, inputs='banana@desk')
       
     - .. code-block:: python
              
              inputs [caption@location]
                 e.g: yellow cup@desk
                     . if no location:
                        find at current loc
                     . else:
                        move to loc first
              detector:
                 [Default: groudingdino]
                 [groudingdino, fastsam, 
                 Groundedsam, groundedsam_grasp]
              camera:
                 [Default: head]
                 [head, rs_raw]
              once: 
                 [Default: True]
                 True:
                   Find at loc only
                 False:
                   Search all loc in ENV

   * - Find_arm
       
     - .. code-block:: python

              # PROMPT USE
              find_arm::[INPUTS]
              example: find_arm::banana

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.recognition import find_arm
              find_arm(node=node, inputs='banana')
       
     - .. code-block:: python
              
              inputs [caption]

              detector:
                 [Default: groundedsam_grasp]
                 [groudingdino, fastsam, 
                 groundedsam, groundedsam_grasp]
              camera:
                 [Default: rs_raw]
                 [head, rs_raw]

Approach Skills
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Usage 
     - Inputs

   * - + Approach_close
       + Approach
       
     - .. code-block:: python

              # PROMPT USE
              approach_close::[INPUTS]

              example 1: 
                 approach_close::banana@desk
              
              example 2: 
                 find::banana@desk
                 approach_close::banana
              
              example 3: 
                 approach_close::[x,y,z,wrist_angle]

              example 4: 
                 approach_close::desk@living_room

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.approach import approach_close
              approach_close(node=node, inputs='banana@desk')
       
     - .. code-block:: python
              
              inputs 
                 [caption, location,
                 caption@location, pose_3d]
                     . if no location:
                        find at current loc
                     . else:
                        move to loc first
                     
                     . if caption:
                         find [caption] first
                       else:
                         move to location
                         approach to placepose
                     
                     . if pose_3d:
                        approach to pose_3d
                     

              init_pose_fixed
                 [Defalt: False]
              
              All find input params


Pick Skills
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Usage 
     - Inputs

   * - Pick
       
     - .. code-block:: python

              # PROMPT USE
              pick::[INPUTS]

              example 1: 
                 pick::banana@desk
              
              example 2: 
                 find::banana@desk
                 pick::banana
              
              example 3: 
                 pick::[x,y,z,wrist_angle]


       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.pick import pick
              pick(node=node, inputs='banana@desk')
       
     - .. code-block:: python
              
              inputs 
                 [caption, location,
                 caption@location, pose_3d]
                     . if no location:
                        find at current loc
                     . else:
                        approach to loc first

              init_pose_fixed
                 [Defalt: True]
              
              All find input params

Place Skills
--------------------

.. list-table:: 
   :header-rows: 1

   * - Fuction 
     - Usage 
     - Inputs

   * - Place
       
     - .. code-block:: python

              # PROMPT USE
              place::[INPUTS]

              example 1: 
                 place::banana@shelf>>desk@living_room
              
              example 2: 
                 pick::banana@shelf@kitchen
                 place::wooden_dish@desk@living_room
              
              example 3: 
                 place::[x,y,z,wrist_angle]

              example 4: 
                 place::desk@living_room

       .. code-block:: python
              
              # DEV USE
              from carerobotapp.skills.place import place
              place(node=node, inputs='banana@desk')
       
     - .. code-block:: python
              
              inputs 
                 [caption, location,
                 caption@location, pose_3d]
                     . if no location:
                        find at current loc
                     . else:
                        move to loc first
                     
                     . if caption:
                         find [caption] first
                       else:
                         move to location
                         approach to placepose
                     
                     . if pose_3d:
                        approach to pose_3d
              
              All approach input params
              
