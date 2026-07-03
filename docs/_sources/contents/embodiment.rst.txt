=====================================
Embodiment: skills, vision & hardware
=====================================

This page covers the robot-specific half of the stack: the ``kcare_robot``
skill set, the perception-and-grasp pipeline, the **VisionServe** GPU server,
and the ROS2 hardware — all reached through the ``pyconnect`` transport.

.. figure:: images/diag_embodiment.png
   :alt: Embodiment stack
   :width: 760px
   :align: center

   The embodiment stack (export ``diagram_body.drawio`` → ``images/diag_embodiment.png``).


The skill contract
=======================================

Every skill is a plain function ``skill(node, **params) -> dict`` that returns a
planner-readable result, at minimum ``{isdone: bool, msg: str}``. Skills are
stateless; all device access goes through ``node.agents[...]`` (never raw ROS).
``SkillRegistry.execute`` dispatches either an **internal** skill (a
``module:function`` pair) or an **external** one (an HTTP endpoint), returning
the same result shape so the verifier treats them identically.


Skill groups
=======================================

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Group
     - Skills
   * - Navigation
     - ``move`` · ``moveb`` (Nav2) · ``forward`` · ``turn`` · ``rotate`` · ``mobile_pose``
   * - Perception
     - ``find`` · ``detect`` · ``find_arm`` · ``get3d`` · ``grasp_succeed`` · ``inform``
   * - Manipulation
     - ``pick`` · ``place`` · ``placeat`` · ``open_drawer`` · ``close_drawer`` · ``wipe`` · ``stack`` (``fine_move`` self-correction)
   * - Low-level
     - ``arm`` (``movej`` / ``movel`` / ``movet``) · ``lift`` · ``head`` (``moveh``) · ``grip``

The full per-skill reference — prompt usage, dev usage and input syntax — is in
:doc:`manual`.


Perception & grasp pipeline
=======================================

The interesting work happens inside the Perception skills. A typical ``find`` /
grasp resolves through these stages:

#. **Fetch RGB-D** — ``fetch_camera_data`` reads the head (Femto Bolt) or wrist
   (RealSense D405) camera via ``node.agents[...]``.
#. **Detect** — ``VisionServe.predict(model, rgb, prompt=...)`` runs an
   open-vocabulary model (``grounding-dino`` for boxes, ``grounded-sam`` for
   masks, ``grasp-gd`` for grasp poses).
#. **Select** — ``select_target_object`` / ``select_target_grasp`` pick the best
   detection by quality / proximity.
#. **Lift to 3D** — ``get3d`` (the ``/create_object_marker`` ROS service) and the
   head-to-base calibration project the pixel target into the base frame.
#. **Result** — a dict ``ins{ loc_3d, pose_3d, grasppose:[x,y,z,rz,w], box,
   score, ... }`` that drives ``pick`` / ``fine_move``.

Two real runs, as seen by the robot's own cameras (all overlays are produced
live by the pipeline):

.. figure:: images/fig_pick_phone_strip.png
   :alt: pick the phone — robot camera frames
   :width: 100%
   :align: center

   ``pick the phone``: **(a)** head camera detects the phone on the table
   (``ph 0.88``, pose ``LYING``); **(b)** wrist camera segments it and scores a
   grasp candidate (``q0.97``); **(c)** ``fine_move`` aligns the gripper
   (width 72 mm, +2°); **(d)** the grasp check passes
   (``grasp OK, near=100%``).

.. figure:: images/fig_pick_coffee_strip.png
   :alt: pick the coffee can — robot camera frames
   :width: 100%
   :align: center

   ``pick the coffee can``: the same detect → segment → align → verify
   sequence on a standing can (``co 0.80``, ``q0.96``, width 68 mm,
   ``grasp OK, near=98%``).

The corresponding external-webcam videos of both runs are embedded on
:doc:`architecture`.


VisionServe — GPU inference server
=======================================

VisionServe is a **separate process** (typically on a GPU machine) that the
robot reaches over TCP/HTTP at ``:11435``:

- **Models**: GroundingDINO (boxes), GroundedSAM (masks), grasp-gd (grasp poses),
  plus a generic detector.
- **Request**: an RGB image + a text prompt; **response**: detections / masks /
  grasps with scores, plus inference ``device`` and timing.
- **Client**: ``_vs_client().predict(model, rgb, prompt=...)`` wraps the call;
  the connection is registered in ``connections.json`` (see :doc:`configuration`).

Because vision runs out-of-process, the robot PC stays light and the GPU box can
serve several robots.


Robot hardware (ROS2)
=======================================

.. figure:: images/photo_robot_modes.png
   :alt: The robot in its three arm-mount modes
   :width: 640px
   :align: center

   The real robot in its three arm-mount configurations — **left**, **front**
   and **right** mode. The KAAIR arm rides the vertical lift rail; the head
   camera sits on the pan-tilt mast.

``kcare_robot`` targets a mobile manipulator wired through ROS2 actions,
services and topics, each wrapped as a ``pyconnect`` agent:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Subsystem
     - ROS2 interface (examples)
   * - KAAIR 6-DOF arm
     - ``/kaair_worker/arm_moveJ`` · ``arm_moveL`` · ``arm_moveT`` (action)
   * - Lift / elevator
     - ``/kaair_worker/lift_move`` (action)
   * - Gripper (2-finger + suction)
     - ``/body/tool_controller/gripper_cmd`` (action)
   * - Pan-tilt head
     - ``/kaair_worker/head_move`` (action)
   * - Mobile base
     - ``/navigate_to_pose`` (Nav2 action) · ``/mobile/shift_pose`` · ``/mobile/rotate`` (services)
   * - Cameras
     - D405 wrist + Femto Bolt head RGB-D (compressed image topics) · camera-info
   * - 3D / poses
     - ``/create_object_marker`` (service) · ``/robot_pose/*`` (topics)

A **head-to-base calibration** (intrinsics + a transform chain with per-mode
error corrections) projects detections from the head camera into the base frame;
the wrist camera provides the close-range frames for ``fine_move`` grasping.

For how devices are declared and swapped per site, see :doc:`configuration`; for
the ``pyconnect`` node/agent framework itself, see :doc:`framework`.
