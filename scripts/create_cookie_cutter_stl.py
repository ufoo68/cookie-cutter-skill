"""Blender Python template for creating a cookie-cutter STL.

Paste this file into Blender MCP's execute_blender_code after editing the
parameters and point generator. Coordinates are in millimeters. By default,
the requested BODY_OUTER_WIDTH_MM is the normal upper/body width; the lower
edge protrudes outward by BOTTOM_LIP_OUTSET_MM on each side. No taper is used.
"""

import math
import os

import bpy
from mathutils import Vector


OUTPUT_PATH = os.path.join(os.path.expanduser("~"), "cookie_cutter.stl")
OBJECT_NAME = "cookie_cutter"

BODY_OUTER_WIDTH_MM = 70.0
HEIGHT_MM = 15.0
WALL_WIDTH_MM = 1.6
BOTTOM_LIP_OUTSET_MM = 2.0
BOTTOM_LIP_HEIGHT_MM = 1.2


def make_star_points(centerline_width_mm=70.0, outer_points=5):
    """Return a closed 5-point star centerline."""
    outer_radius = centerline_width_mm / (2.0 * math.cos(math.radians(18.0)))
    inner_radius = outer_radius * 0.45
    pts = []
    for i in range(outer_points * 2):
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle = math.radians(90.0 + i * 180.0 / outer_points)
        pts.append((radius * math.cos(angle), radius * math.sin(angle)))

    scale = centerline_width_mm / (max(x for x, _ in pts) - min(x for x, _ in pts))
    scaled = [(x * scale, y * scale) for x, y in pts]
    cx = (min(x for x, _ in scaled) + max(x for x, _ in scaled)) / 2.0
    cy = (min(y for _, y in scaled) + max(y for _, y in scaled)) / 2.0
    return [(x - cx, y - cy) for x, y in scaled]


def polygon_area(points):
    area = 0.0
    for i, (x1, y1) in enumerate(points):
        x2, y2 = points[(i + 1) % len(points)]
        area += x1 * y2 - x2 * y1
    return area * 0.5


def offset_loop(points, half_width):
    """Offset a closed centerline loop using mitered joins.

    The loop is normalized to counterclockwise order. For a CCW loop, the
    left normal points inward, so positive half_width offsets inward and
    negative half_width offsets outward.
    """
    pts = [Vector((x, y)) for x, y in points]
    if polygon_area(points) < 0:
        pts.reverse()

    out = []
    count = len(pts)
    for i, current in enumerate(pts):
        prev = pts[(i - 1) % count]
        nxt = pts[(i + 1) % count]
        d1 = (current - prev).normalized()
        d2 = (nxt - current).normalized()
        n1 = Vector((-d1.y, d1.x))
        n2 = Vector((-d2.y, d2.x))
        miter = n1 + n2
        if miter.length < 1e-6:
            miter = n2
        else:
            miter.normalize()
        denom = max(0.2, abs(miter.dot(n2)))
        out.append(current + miter * (half_width / denom))
    return [(p.x, p.y) for p in out]


def scale_loop_to_width(loop, target_width):
    current_width = max(x for x, _ in loop) - min(x for x, _ in loop)
    factor = target_width / current_width
    return [(x * factor, y * factor) for x, y in loop]


def max_body_width_for_centerline(centerline_width_mm):
    pts = make_star_points(centerline_width_mm)
    outer = offset_loop(pts, -WALL_WIDTH_MM / 2.0)
    return max(x for x, _ in outer) - min(x for x, _ in outer)


def solve_centerline_width(body_outer_width_mm):
    low = body_outer_width_mm * 0.50
    high = body_outer_width_mm
    for _ in range(50):
        mid = (low + high) / 2.0
        if max_body_width_for_centerline(mid) > body_outer_width_mm:
            high = mid
        else:
            low = mid
    return (low + high) / 2.0


def add_loop(verts, outer, inner, z):
    outer_idx = []
    inner_idx = []
    for x, y in outer:
        outer_idx.append(len(verts))
        verts.append((x, y, z))
    for x, y in inner:
        inner_idx.append(len(verts))
        verts.append((x, y, z))
    return outer_idx, inner_idx


def build_cutter_mesh(points):
    wall_outer = offset_loop(points, -WALL_WIDTH_MM / 2.0)
    wall_inner = offset_loop(points, WALL_WIDTH_MM / 2.0)

    lip_outer_width = BODY_OUTER_WIDTH_MM + 2.0 * BOTTOM_LIP_OUTSET_MM
    lip_outer = scale_loop_to_width(wall_outer, lip_outer_width)
    lip_inner = wall_inner

    verts = []
    loops = [
        add_loop(verts, lip_outer, lip_inner, 0.0),
        add_loop(verts, lip_outer, lip_inner, BOTTOM_LIP_HEIGHT_MM),
        add_loop(verts, wall_outer, wall_inner, BOTTOM_LIP_HEIGHT_MM),
        add_loop(verts, wall_outer, wall_inner, HEIGHT_MM),
    ]

    faces = []
    count = len(points)
    for level in range(len(loops) - 1):
        outer_a, inner_a = loops[level]
        outer_b, inner_b = loops[level + 1]
        for i in range(count):
            j = (i + 1) % count
            faces.append((outer_a[i], outer_a[j], outer_b[j], outer_b[i]))
            faces.append((inner_a[j], inner_a[i], inner_b[i], inner_b[j]))

    top_outer, top_inner = loops[-1]
    bottom_outer, bottom_inner = loops[0]
    for i in range(count):
        j = (i + 1) % count
        faces.append((top_outer[i], top_outer[j], top_inner[j], top_inner[i]))
        faces.append((bottom_outer[j], bottom_outer[i], bottom_inner[i], bottom_inner[j]))

    mesh = bpy.data.meshes.new(OBJECT_NAME + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    return mesh


def count_non_manifold_edges(mesh):
    uses = {}
    for poly in mesh.polygons:
        vertices = list(poly.vertices)
        for i, a in enumerate(vertices):
            b = vertices[(i + 1) % len(vertices)]
            key = tuple(sorted((a, b)))
            uses[key] = uses.get(key, 0) + 1
    return sum(1 for use_count in uses.values() if use_count != 2)


def export_selected_stl(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    if hasattr(bpy.ops.wm, "stl_export"):
        bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True)
    else:
        bpy.ops.export_mesh.stl(filepath=path, use_selection=True, ascii=False)


def main():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    centerline_width = solve_centerline_width(BODY_OUTER_WIDTH_MM)
    points = make_star_points(centerline_width)
    mesh = build_cutter_mesh(points)
    print(f"Non-manifold edges before export: {count_non_manifold_edges(mesh)}")
    obj = bpy.data.objects.new(OBJECT_NAME, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    export_selected_stl(OUTPUT_PATH)
    print(f"Exported {OBJECT_NAME} to {OUTPUT_PATH}")


main()
