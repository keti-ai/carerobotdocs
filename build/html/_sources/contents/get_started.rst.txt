.. _install:

===========
Get started
===========

This guide installs and runs the **closed-loop stack**: the ``robot_agent``
runtime, the ``kcare_robot`` robot package, the optional ``robotapp`` dashboard,
the ``pyplanner`` / SAGE planner, and the ``VisionServe`` GPU vision server.

For host preparation (NVIDIA driver, CUDA, Docker) see :ref:`host_setup` at the
bottom of this page.


Repositories
===========================

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Repository
     - Role
   * - ``robot_agent``
     - robot-agnostic FastAPI runtime (closed loop, world state, verifier)
   * - ``kcare_robot``
     - reference robot package (skills + name map + per-site configs)
   * - ``pyplanner``
     - pluggable LLM planners incl. **SAGE** (used by ``robot_agent``)
   * - ``pyconnect``
     - ROS2 transport + VisionServe client
   * - ``robotapp``
     - optional Next.js operator dashboard
   * - ``visionserve``
     - GPU inference server (object + grasp detection)


Prerequisites
===========================

- Ubuntu 22.04, Python 3.10+, and an NVIDIA GPU for VisionServe.
- ROS2 (Humble) on the robot/control machine for the hardware interfaces.
- Node.js 18+ if you want to run the dashboard.
- An LLM backend: a local Ollama server (recommended, on-premise) or an
  OpenAI / Gemini API key.


Install the Python packages
===========================

Clone the repositories side by side and install them editable:

.. code-block:: bash

    pip install -e pyplanner
    pip install -e robot_agent
    pip install -e kcare_robot
    pip install -e pyconnect

Install the dashboard dependencies:

.. code-block:: bash

    cd robotapp/frontend && npm install        # or: cd robotapp && make install


Run the stack
===========================

The stack is three long-running processes (plus an LLM server). Start them in
this order:

**1. LLM server (Ollama, local).**

.. code-block:: bash

    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    docker exec -it ollama ollama pull qwen2.5:7b

**2. VisionServe GPU server** — listens on ``:11435`` (object + grasp detection).
Start it on the GPU machine per the ``visionserve`` README; the robot reaches it
via the ``visionserve`` connection in ``connections.json``.

**3. Robot backend** — the ``kcare_robot`` FastAPI app (boots on ``:8001``).

.. code-block:: bash

    uvicorn kcare_robot.main:app --host 0.0.0.0 --port 8001

**4. Dashboard (optional)** — Next.js dev server on ``:3007``.

.. code-block:: bash

    cd robotapp && make run-frontend

.. note::

   Exact backend / VisionServe launch commands can vary by deployment — confirm
   against each package's README. The ports above (``8001`` backend, ``11435``
   VisionServe, ``11434`` Ollama, ``3007`` dashboard) are the project defaults.


Your first command
===========================

**From the dashboard** — open ``http://<robot-ip>:3007``, pick the robot and a
location, type or speak a task ("bring me the cup from the table"), choose the
``grace`` planner, and watch the plan, world state, and step timeline update
live.

**From the CLI / Python API** — drive the same skills in-process without the
dashboard (see :doc:`manual` for the skill syntax and :doc:`examples` for code).

Two clients driving the *same* robot at once is unsafe — operate from one at a
time.


Deployment scenarios
===========================

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Scenario
     - What runs where
   * - Single-PC dev
     - everything on one machine with a GPU; Ollama + VisionServe + backend local
   * - Robot + GPU box
     - backend on the robot PC; VisionServe + Ollama on a GPU server reached over the LAN
   * - Remote operator
     - add the dashboard; operators drive the robot over HTTP / WebSocket from any device


.. _host_setup:

Appendix: host setup
===========================

GPU driver, Docker and the NVIDIA Container Toolkit are needed for the GPU
machine (Ollama + VisionServe):

- NVIDIA drivers: ``sudo add-apt-repository ppa:graphics-drivers/ppa`` then pick
  the driver in *Software & Updates ▸ Additional Drivers* and reboot.
- Docker Engine: https://docs.docker.com/engine/install/ubuntu/
- NVIDIA Container Toolkit:
  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

Base packages:

.. code-block:: bash

    sudo apt update
    sudo apt install -y python3-dev python3-venv python3-pip terminator htop
