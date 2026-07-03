Put self-hosted robot demo videos here (and their poster images).

Recommended files referenced by contents/architecture.rst:
  demo_full_task.mp4      poster_full_task.jpg     full pick-and-deliver run
  demo_grasp.mp4          poster_grasp.jpg         close-up of a fine_move grasp

Keep clips short (10-40 s) and < ~20 MB each so the docs site stays light.
Encode H.264 MP4 (yuv420p) for broad browser support, e.g.:
  ffmpeg -i raw.mov -vcodec libx264 -pix_fmt yuv420p -crf 24 -an demo_grasp.mp4
  ffmpeg -i demo_grasp.mp4 -vf "select=eq(n\,0)" -vframes 1 poster_grasp.jpg

For YouTube-hosted clips you do not need files here; see the iframe pattern
in contents/architecture.rst.
