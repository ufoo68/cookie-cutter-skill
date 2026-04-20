# Cookie Cutter Design Checklist

Use this checklist before final STL export.

## Printability

- Overall size matches the user's requested millimeters.
- Treat requested width as upper/body outer width unless the user asks for total footprint.
- Default lower lip protrudes 2 mm per side, so total footprint width is body width plus 4 mm.
- Wall width is usually 1.2-2.0 mm for FDM printing.
- Wall thickness is constant by default; do not add a cutting-edge taper unless requested.
- Minimum distance between unrelated walls is at least 2 mm unless the user accepts delicate details.
- Interior corners are not too tight for dough release; round small decorative details.
- Height is usually 12-18 mm. Very tall cutters may need a handle rim.
- Organic curves use enough points to look smooth, but not so many that STL becomes noisy.

## Geometry

- The centerline path is closed and does not self-intersect.
- The generated object is a single manifold-looking mesh with no obvious flipped sections.
- The lower edge has a short outward lip/flange and meets the constant wall with a flat shoulder.
- Scene units are metric and the mesh dimensions are in millimeters.
- Only intended printable objects are selected for STL export.

## User-Facing Final Response

Report the exported STL path and the main physical dimensions. Mention any assumptions, such as default wall thickness or size, briefly.
