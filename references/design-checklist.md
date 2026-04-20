# Cookie Cutter Design Checklist

Use this checklist before final STL export.

## Printability

- Overall size matches the user's requested millimeters.
- Wall width is usually 1.2-2.0 mm for FDM printing.
- Cutting edge is usually 0.4-0.8 mm wide, not a mathematically sharp zero-width edge.
- Minimum distance between unrelated walls is at least 2 mm unless the user accepts delicate details.
- Interior corners are not too tight for dough release; round small decorative details.
- Height is usually 12-18 mm. Very tall cutters may need a handle rim.
- Organic curves use enough points to look smooth, but not so many that STL becomes noisy.

## Geometry

- The centerline path is closed and does not self-intersect.
- The generated object is a single manifold-looking mesh with no obvious flipped sections.
- The blade taper is at the bottom, with the broader wall above it.
- Scene units are metric and the mesh dimensions are in millimeters.
- Only intended printable objects are selected for STL export.

## User-Facing Final Response

Report the exported STL path and the main physical dimensions. Mention any assumptions, such as default wall thickness or size, briefly.
