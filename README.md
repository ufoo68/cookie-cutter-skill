# cookie-cutter-skill

Codex agent skill for designing 3D-printable cookie-cutter STL files with Blender MCP.

This repository is laid out as a skill package: `SKILL.md` lives at the repository root, with reusable Blender code and printability guidance beside it.

## Contents

- `SKILL.md`: Trigger description, workflow, and modeling rules for cookie-cutter STL generation.
- `agents/openai.yaml`: Skill UI metadata and Blender MCP dependency metadata.
- `scripts/create_cookie_cutter_stl.py`: Blender Python template that creates a tapered cutter wall from a closed 2D centerline and exports STL.
- `references/design-checklist.md`: Printability and final validation checklist.

## Usage

Invoke the skill when asking Codex to create, preview, validate, or export a cookie cutter, clay cutter, fondant cutter, outline cutter, embossing cutter, or similar STL.

Example prompt:

```text
Use $cookie-cutter-stl to create a 70 mm heart-shaped cookie cutter STL with a 15 mm height.
```

The skill expects Blender MCP to be available so Codex can run Blender Python, inspect the generated object, and export the STL.
