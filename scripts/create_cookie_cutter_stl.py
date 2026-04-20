"""Blender Python template for creating a tapered cookie-cutter STL.

Paste this file into Blender MCP's execute_blender_code after editing the
parameters and points. It uses millimeter dimensions and exports a binary STL.
"""

import math
import os

import bpy
from mathutils import Vector


OUTPUT_PATH = os.path.abspath("cookie_cutter.stl")
OBJECT_NAME = "cookie_cutter"

HEIGHT_MM = 15.0
WALL_WIDTH_MM = 1.6
CUT_WIDTH_MM = 0.6
BLADE_HEIGHT_MM = 2.0


def make_heart_points(width_mm=70.0, samples=120):
    """Return a closed heart-shaped centerline in millimeters."""
    pts = []
    for i in range(samples):
        t = 2.0 * math.pi * i / samples
        x = 16.0 * math.sin(t) ** 3
        y = (
            13.0 * math.cos(t)
            - 5.0 * math.cos(2.0 * t)
            - 2.0 * math.cos(3.0 * t)
            - math.cos(4.0 * t)
        )
        pts.append((x, y))

    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    scale = width_mm / (max_x - min_x)
    scaled = [(x * scale, y * scale) for x, y in pts]
    cx = sum(x for x, _ in scaled) / len(scaled)
    cy = sum(y for _, y in scaled) / len(scaled)
    return [(x - cx, y - cy) for x, y in scaled]


def polygon_area(points):
    area = 0.0
    for i, (x1, y1) in enumerate(points):
        x2, y2 = points[(i + 1) % len(points)]
        area += x1 * y2 - x2 * y1
    return area * 0.5


def offset_loop(points, half_width):
    """Offset a closed centerline loop by half_width using mitered joins."""
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


def build_cutter_mesh(points, height_mm, wall_width_mm, cut_width_mm, blade_height_mm):
    z_levels = [
        (0.0, cut_width_mm),
        (blade_height_mm, wall_width_mm),
        (height_mm, wall_width_mm),
    ]
    verts = []
    loops = []

    for z, width in z_levels:
        outer = offset_loop(points, width / 2.0)
        inner = offset_loop(points, -width / 2.0)
        outer_idx = []
        inner_idx = []
        for x, y in outer:
            outer_idx.append(len(verts))
            verts.append((x, y, z))
        for x, y in inner:
            inner_idx.append(len(verts))
            verts.append((x, y, z))
        loops.append((outer_idx, inner_idx))

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

    points = make_heart_points(width_mm=70.0)
    mesh = build_cutter_mesh(points, HEIGHT_MM, WALL_WIDTH_MM, CUT_WIDTH_MM, BLADE_HEIGHT_MM)
    obj = bpy.data.objects.new(OBJECT_NAME, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    export_selected_stl(OUTPUT_PATH)
    print(f"Exported {OBJECT_NAME} to {OUTPUT_PATH}")


main()
