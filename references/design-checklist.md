# Cookie Cutter Design Checklist

Use this checklist before final STL export.

## Printability

- Overall size matches the user's requested millimeters.
- Treat requested width as upper/body outer width unless the user asks for total footprint.
- Default lower lip protrudes 2 mm per side, so total footprint width is body width plus 4 mm.
- Wall width is usually 1.2-2.0 mm for FDM printing.
- If constant wall thickness is requested, sample or print-check the inner/outer wall distance; do not rely on separately scaled loops.
- Wall thickness is constant by default; do not add a cutting-edge taper unless requested.
- Outside lips should protrude outward from the body. For a counterclockwise loop, remember the left normal points inward; verify the lip footprint is wider than the body.
- If the lip and cutter edge should share the same contact plane, confirm inner bottom, wall outer bottom, and lip outer bottom are all at the same Z value.
- Minimum distance between unrelated walls is at least 2 mm unless the user accepts delicate details.
- Interior corners are not too tight for dough release; round small decorative details.
- Height is usually 12-18 mm. Very tall cutters may need a handle rim.
- Organic curves use enough points to look smooth, but not so many that STL becomes noisy.
- Image-derived silhouettes are simplified into clean arcs/segments instead of pixel-traced bumps.
- Segment joins are checked for local backtracking, especially where shoulders meet roofs, wheel arches, ears, handles, or other large curves.
- For hearts and cusped shapes, avoid miter spikes in outer support geometry. Preserve a sharp inner point only when requested.
- Internal marking or emboss lines are added only when requested, and open-line endpoints are either intentionally joined into the cutter wall or understood to print as separate pieces.

## Geometry

- The centerline path is closed and does not self-intersect.
- Offset joins do not create visible miter spikes or protrusions. If a screenshot reveals a bump, inspect the nearby point order before adjusting global scale or wall width.
- The generated object is a single manifold-looking mesh with no obvious flipped sections.
- The lower edge has a short outward lip/flange and meets the constant wall with a flat shoulder.
- The inner cutting wall has no unintended ledges, shelves, or internal shoulders.
- Mesh edge-use validation reports zero non-manifold edges; each edge belongs to exactly two faces.
- Outside-only lip meshes use one closed swept cross-section rather than overlapping coplanar strips.
- Scene units are metric and the mesh dimensions are in millimeters.
- Only intended printable objects are selected for STL export.
- Scene object count matches the requested variant: outline-only exports should usually contain one cutter object; marked cutters should contain the cutter plus only the requested marking objects.

## User-Facing Final Response

Report the exported STL path and the main physical dimensions. Mention any assumptions, such as default wall thickness or size, briefly.
