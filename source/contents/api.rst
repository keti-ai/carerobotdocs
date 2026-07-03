================
API & code map
================

A quick reference to the backend HTTP/WebSocket surface and where the key code
lives. (Full autodoc can be wired back in once the packages import cleanly in
the docs environment; see :ref:`autodoc_note`.)


HTTP / WebSocket endpoints
=======================================

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Endpoint
     - Purpose
   * - ``GET /skills``
     - list registered skills
   * - ``POST /skill/<name>``
     - run a skill (body = params)
   * - ``POST /skills/reload``
     - refresh the registry after edits
   * - ``GET /devices`` · ``POST /devices``
     - list / add configured devices
   * - ``GET /diagnostics/boot``
     - boot-error inspection
   * - ``GET /camera/<id>``
     - MJPEG / WebRTC stream
   * - ``GET`` / ``PUT /agent/world``
     - read / partially update the world belief
   * - ``POST /agent/llm-config``
     - set LLM provider & model
   * - ``POST /agent/api-key`` · ``GET /agent/api-keys``
     - manage provider API keys
   * - ``…/config/locations[...]``
     - per-site config profiles (CRUD + activate)
   * - ``WS /ws/agent``
     - run a task; stream plan / step / world / done events


Where the code lives
=======================================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Module
     - Responsibility
   * - ``robot_agent`` core / planning
     - ``ClosedLoop``, ``ActionMapper``, ``StepVerifier``, ``WorldState``, ``Announcer``, ``RunLogger``
   * - ``robot_agent`` planning/registry
     - ``get_planner`` + backends (``grace`` → SAGE, ``llm_direct``)
   * - ``robot_agent`` core
     - ``UnifiedAgent``, ``SkillRegistry``, ``DeviceManager``, ``AgentState``
   * - ``robot_agent`` api
     - FastAPI routers incl. ``/ws/agent`` and ``/agent/world``
   * - ``pyplanner``
     - LLM planners incl. **SAGE** (decompose · memory · symbolic gate · suffix repair)
   * - ``kcare_robot`` skills
     - the 23 skills (navigation / perception / manipulation / low-level)
   * - ``kcare_robot`` configs
     - ``grace_namemap`` + per-site ``connections.json``
   * - ``pyconnect``
     - ROS2 ``CustomNode`` + agents, codecs, VisionServe client
   * - ``robotapp/frontend``
     - Next.js dashboard (``lib/api.ts``, ``lib/types.ts``, panels)


.. _autodoc_note:

Enabling autodoc
=======================================

``conf.py`` already adds the package roots to ``sys.path`` (overridable with the
``CAREROBOT_REPO`` environment variable). To generate API pages from docstrings,
add an ``autodoc``/``automodule`` toctree once the target packages (and their
heavy dependencies — ROS2, torch, the vision SDK) import in the build
environment; otherwise stub those imports with ``autodoc_mock_imports``.
