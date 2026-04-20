---
name: cookie-cutter-stl
description: Create 3D-printable cookie-cutter STL files with Blender MCP. Use when the user asks Codex to design, model, preview, validate, or export a cookie cutter, biscuit cutter, clay cutter, fondant cutter, outline cutter, embossing cutter, or cutter STL from a sketch, silhouette, text, icon, SVG-like path, or verbal shape description.
---

# Cookie Cutter STL

## Overview

Use Blender MCP to build a printable cutter from a 2D outline, verify the geometry in Blender, and export an STL. Prefer the bundled Blender Python template for repeatable wall, blade, lower lip, and export behavior.

## Workflow

1. Clarify the physical intent only when needed: body outer size in mm, cutter height, wall thickness, blade thickness, lower-lip size, whether an embossing stamp is needed, and the target output path.
2. Convert the requested design into one or more closed 2D centerline paths in millimeters. Keep outlines simple enough to clean and print; avoid narrow gaps below 2 mm unless the user explicitly wants fine detail.
3. Use `scripts/create_cookie_cutter_stl.py` as the starting Blender Python code. Edit the parameters and `points` generator, then run it through `mcp__blender__execute_blender_code`.
4. Inspect the created object with `mcp__blender__get_object_info`. Check dimensions, object count, and that the STL was exported to the requested path. The total footprint should include the lower-lip overhang.
5. If the model has unsupported tiny features, self-crossing paths, or a wrong scale, revise the point path and rerun the Blender code.

## Modeling Rules

- Work in millimeters. Set Blender scene units to metric with `scale_length = 0.001`.
- Make the path closed, planar, and ordered consistently. Use 64-160 points for smooth organic shapes; use fewer points for crisp geometric shapes.
- Default dimensions: `height_mm=15`, `wall_width_mm=1.6`, `cut_width_mm=0.6`, `blade_height_mm=2.0`, `bottom_lip_outset_mm=2.0`, `bottom_lip_height_mm=1.2`.
- Treat the user's requested width as the upper/body outer width unless they explicitly ask for total footprint. With the default lower lip, total width is `requested_width + 4 mm` because the bottom edge protrudes 2 mm on each side.
- Keep the cutter body one watertight mesh. The bottom edge should form an outward lip/flange, then transition up into the tapered blade and the normal wall.
- Add separate embossing geometry only when requested. Name objects clearly, for example `cookie_cutter` and `emboss_lines`.
- Export binary STL after selecting only the intended printable objects.

## Blender MCP Pattern

Use small, explicit Blender MCP calls:

1. Run the edited Python template with `mcp__blender__execute_blender_code`.
2. Query `cookie_cutter` with `mcp__blender__get_object_info`.
3. If needed, run a short corrective code block rather than resending unrelated scene setup.

When the user provides an image or vague idea, first derive a simple silhouette. State assumptions in the final response: body size, total lip footprint, height, wall thickness, bottom-lip overhang, and output path.

## Resources

- `scripts/create_cookie_cutter_stl.py`: Blender Python template for a tapered cookie-cutter wall from a closed 2D centerline.
- `references/design-checklist.md`: printability and validation checklist to read before final export or when a model fails.
