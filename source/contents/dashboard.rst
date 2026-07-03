==================
Operator dashboard
==================

The ``robotapp`` dashboard is an **optional** Next.js web app that lets one or
more operators drive and monitor a robot over HTTP / WebSocket. The robot is
fully operable without it (CLI / Python API); the dashboard adds a multi-user
interactive layer.

.. note::

   📷 **Screenshot slot** — add ``images/shot_dashboard.png`` (the full
   dashboard) and the per-panel shots named below into
   ``source/contents/images/``.

.. figure:: images/shot_dashboard.png
   :alt: The robotapp dashboard
   :width: 700px
   :align: center

   The dashboard: device/location pickers, task input, live plan & world state,
   shortcut buttons, and camera feed.


Choosing a robot and a site
=======================================

The **DevicePanel** has two pickers:

- **Robot** — a client-side registry (kept in ``localStorage``) of robot backend
  URLs. Switching robots re-targets every API call and the WebSocket; an
  unreachable robot rolls back to the previous one.
- **Location** — per-robot, **server-side** config profiles (each a
  ``connections.json`` + global configs for one deployment site). Activating a
  location hot-reloads the backend's device connections, so the connection list
  refreshes right after. Sites are distinct from the multi-robot URL registry.

The panel also exposes device connections (ROS topics/services/actions, LLM
clients, API keys) for the active site.


Sending a task
=======================================

The **AgentPanel** is the command box:

- **Structured vs. unstructured** input (predefined tasks vs. free natural
  language), with optional **voice** input/output (vi / ko / en).
- **Planner** selection — ``grace`` (SAGE closed loop) or ``direct``.
- **Plan-only** — generate the plan without executing it.

Submitting opens the ``/ws/agent`` WebSocket and streams the run back live.


Watching the run
=======================================

The **PlanPanel** shows, top to bottom:

- **Robot State** (``WorldStateBlock``) — editable inputs for ``arrived`` /
  ``holding`` / ``found`` / ``opened`` / ``on``, a "held N m ago" age hint, and a
  read-only *found pose* with a fresh / ⚠ stale badge. Each save is a
  ``PUT /agent/world`` — safe even mid-run.
- **Plan** — the generated steps.
- **Execution timeline** — per-step status (⟳ running, ✓ done, ✗ failed) with
  nested logs, result objects, and step images.

The value shown comes from the latest ``world`` event on the agent WebSocket,
falling back to ``GET /agent/world`` on mount.

Other panels: **ButtonPanel** (server-synced shortcut buttons, drag to
reorder), **CameraFeed** (WebRTC / MJPEG streams), **SkillPanel**,
**EnvPanel**, and **GuidePanel**.


Safety
=======================================

``POST /skill/<name>`` is the same path the CLI mode resolves through. **Two
clients driving the same robot simultaneously is unsafe** — coordinate so only
one operator (or the dashboard *or* the CLI) commands a given robot at a time.


Build & deploy
=======================================

.. code-block:: bash

    cd robotapp
    make run-frontend        # next dev on :3007
    make build-frontend      # static export to frontend/out/
    CLOUDFLARE_API_TOKEN=… make deploy

The production build is a static export deployed to Cloudflare Pages.
