.. _manual:
=============
Manual
=============

This section list commands used to control robot

Refer to DEVICE_CLIENT_CONFIGS in :ref:`device_configs` for more details.

[CLIK  TO SOURCE]

Device Control
-------------------

- Example code for one time sending device control request

.. code-block:: python

       from pyconnect.ros.custom_node import CustomNode
       from rosinterfaces.srv import SendStringData
       from pyconnect.ros.utils import node_add_agents_from_configs
       from carerobotapp.configs.device_clients import DEVICE_CLIENT_CONFIGS
       

       node = CustomNode(name='device_control')
       node = node_add_agents_from_configs(node=node, configs=DEVICE_CLIENT_CONFIGS)
       node.spin(run_thread=True)

       node.agents[agent_name].send(request)





Enable robot motion
*******************

- Agent name: /xarm/motion_enable

- Request format

.. code-block:: bash

       enable_motion::

Set mode
*******************

- Agent name: /xarm/set_mode

- Request format

.. code-block:: bash

       set_mode::0

Set state
*******************

- Agent name: /xarm/set_state

- Request format

.. code-block:: bash

       set_state::0

Clean error
*******************

- Agent name: /xarm/clean_error

- Request format

.. code-block:: bash

       clean_error::

Move joint
*******************

- Agent name: /xarm/set_servo_angle

- Request format

.. code-block:: bash

       move_angles::joint_angle0,joint_angle1,joint_angle2,joint_angle3,joint_angle4,joint_angle5,joint_angle6

Notes:
       - joint angles in [radians]
       - move_angles::home: move to predefined HOME_JOINT
       - move_angles::ready: move to predefined READY_JOINT


Move relative
*******************

- Agent name: /xarm/set_position,

- Request format

.. code-block:: bash

       dmove::dx=dx,dy=dy,dz=dz,drx=drx,dry=dry,dz=drz

Notes:
       - dx, dy, dz in [mm], drx, dry, drz in [degrees]
       - dmove::dx=dx: move for x-axis only


Lift arm
*******************

- Agent name: /elevation/set_position

- Request format

.. code-block:: bash

       lift::position

Notes:
       - position in [mm]

Grip control
*******************

- Agent name: /gripper/command

- Request format

.. code-block:: bash

       grip::position

Notes:
       - position in range [0,1000]
       - grip::open = grip::1000
       - grip::close = grip::0

Move head
*******************

- Agent name: /head/pose_command

- Request format

.. code-block:: bash

       move_head::ry=ry,rz=rz

Notes:
       - ry, rz in [degrees]
       - ry < 0: look down




Device State
-------------------

- Example code for getting device state

.. code-block:: python

       from pyconnect.ros.custom_node import CustomNode
       from rosinterfaces.srv import SendStringData
       from pyconnect.ros.utils import node_add_agents_from_configs
       from carerobotapp.configs.device_clients import DEVICE_CLIENT_CONFIGS
       

       node = CustomNode(name='device_control')
       node = node_add_agents_from_configs(node=node, configs=DEVICE_CLIENT_CONFIGS)
       node.spin(run_thread=True)

       while True:
              rev_data = node.agents[agent_name].rev_data
              if rev_data is None:
                     time.sleep(1)
                     continue
              print(rev_data)
              break



Skill Control
-----------------------

- To run skill control, system need to be executed as descired in :ref:`system_exec`

Init robot
****************

- Request format

.. code-block:: bash

       init_robot::


Init pick
****************

- Request format

.. code-block:: bash

       init_pick::

Detect Object
****************

- Request format

.. code-block:: bash

       detect::caption

Notes:
       - caption: in format 'object_name1, object_name2, ....'


Find Object
****************

- Request format

.. code-block:: bash

       find::caption

Pick Object
****************

- Request format

.. code-block:: bash

       pick::object_name

Notes:
       - Pick request should be appear after a detect or find function
       - example: find::cup\npick::cup

Place object
****************

- Request format

.. code-block:: bash

       place::object_name

Approach object
****************

- Request format

.. code-block:: bash

       approach::object_name


Arm back

- Request format

.. code-block:: bash

       arm_back::




