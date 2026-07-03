=============
Configuration
=============

Most of what you customize for a deployment lives in ``kcare_robot``'s config
folder and in a few backend endpoints. Nothing here requires touching the
robot-agnostic ``robot_agent`` engine.


Location (site) profiles
=======================================

A robot backend keeps **one config folder per deployment site**, each holding
its own ``connections.json`` plus global configs. The active site is switched at
runtime; switching triggers a backend device reconnect.

Managed over HTTP and from the dashboard's Location picker:

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Endpoint
     - Action
   * - ``GET /config/locations``
     - list sites
   * - ``POST /config/locations``
     - create a site (optionally copy from another)
   * - ``PUT /config/locations/...``
     - rename / activate a site
   * - ``DELETE /config/locations/...``
     - delete a site

Sites are a **per-robot backend** concept, distinct from the multi-robot URL
registry the dashboard keeps in ``localStorage``.


Device connections
=======================================

``connections.json`` declares every device the robot talks to. Each entry names
a connection ``type`` (ROS ``topic`` / ``service`` / ``action``, ``visionserve``,
``llm``, HTTP, …), an agent name used as ``node.agents[name]``, and a config
block (topic/service/action name, codecs, URL/port). For example the vision
server is a ``visionserve`` entry pointing at ``http://<gpu-host>:11435``.

See :doc:`embodiment` for the hardware interfaces these entries wrap.


The name map
=======================================

``grace_namemap`` is the robot-specific adapter the ``ActionMapper`` reads. It
declares:

- **Location table** — planner location name → ENV/move key.
- **Object table** — planner object name → detector string.
- ``SKILL_MAP`` — planner action → kcare skill.
- ``SUPPORTED_ACTIONS`` / ``NOOP_ACTIONS`` / ``VLM_ACTIONS`` — what this robot can
  do, skips, and vision-checks.
- ``observe`` / ``vlm_hook`` — grounding and the optional layer-3 vision check.

Editing the name map is how you teach a new robot which planner actions it
supports without changing the engine.


World state
=======================================

The persistent belief (``WorldState``) is stored in ``world_state.json`` and
read/written via ``GET`` / ``PUT /agent/world``. It survives restarts; ``arrived``
is reconciled from localization on each run, the rest are beliefs. See
:doc:`cognition` for the field semantics.


LLM provider & keys
=======================================

- ``POST /agent/llm-config`` — set provider (Ollama / OpenAI / Gemini) and model.
- ``POST /agent/api-key`` / ``GET /agent/api-keys`` — store / list provider keys
  server-side.

Running Ollama locally keeps the planner fully on-premise. SAGE-specific options
(memory paths, ``top_k``, ``max_refines``, Chroma on/off) are passed through to
``pyplanner`` when the ``grace`` backend is constructed.
