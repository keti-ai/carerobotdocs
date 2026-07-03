=========================
Troubleshooting & FAQ
=========================

Common issues when bringing up or operating the closed-loop stack.


The backend won't boot
=======================================

Check ``GET /diagnostics/boot`` — it surfaces boot-time errors (a missing
config, an unreachable device, a bad ``connections.json`` entry). Confirm the
backend is the ``kcare_robot`` FastAPI app on ``:8001`` and that the active
location's ``connections.json`` is valid.


No devices / ROS not connected
=======================================

- Make sure the ROS2 stack (Humble) and the robot's drivers are up on the
  control machine, and ``ROS_DOMAIN_ID`` matches.
- In the dashboard's DevicePanel, scan ROS interfaces and verify each agent in
  ``connections.json`` resolves to a live topic/service/action.
- Switching the **location** triggers a reconnect — use it to re-establish
  devices after the robot drivers restart.


VisionServe / detection fails
=======================================

- Verify the VisionServe server is running and reachable at ``:11435`` (the
  client checks ``health`` on connect).
- ``find`` returns nothing → check the text prompt and that the requested model
  (``grounding-dino`` / ``grounded-sam`` / ``grasp-gd``) is served.
- Detections look mislocated → suspect the head-to-base **calibration**, not the
  detector.


Planning / LLM problems
=======================================

- "planner unavailable" → ``pyplanner`` must be installed (``pip install -e
  pyplanner``) for the ``grace`` backend.
- The model is slow or unreachable → confirm the LLM backend
  (``POST /agent/llm-config``) and that Ollama (``:11434``) or the API key is set.
- Plans keep failing verification → inspect the per-run JSONL in ``task_runs/``;
  the failing layer (``isdone`` / ``symbolic`` / ``VLM``) is recorded per step.


Grasping issues
=======================================

- ``holding`` shows the wrong object — there is **no gripper sensor**; it is a
  belief. Correct it from the dashboard's Robot State (``PUT /agent/world``).
- A grasp uses an old pose — if ``found_pose`` is flagged **stale** (base moved
  > 0.25 m since detection), re-run ``find`` before picking.


Replanning never finishes
=======================================

Replans are **bounded** (default 3). If a task exhausts the budget it ends with
``status = failed`` — read the run log to see which sub-goal could not be
repaired, and check that the precondition the verifier complains about is
actually satisfiable on this robot.


Voice / TTS
=======================================

The Announcer speaks milestones in vi / ko / en. If Vietnamese audio falls back
to English on the backend, that is the known TTS clamp; the dashboard's
browser-side speech can still speak ``vi-VN``.


Two operators conflict
=======================================

If the robot behaves erratically, make sure only **one** client is commanding
it. The dashboard and the CLI both resolve to ``POST /skill/<name>``; running
them against the same robot at once is unsafe.
