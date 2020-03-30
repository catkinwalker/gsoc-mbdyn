import bpy


def poly(x):
    return   0.1 * x * x - x + 3

vase = bpy.data.curves.new("poly", 'CURVE')
vase.dimensions  = '3D'
bez = vase.splines.new('BEZIER')
pts = [(poly(z), 0, z) for z in range(10)]
flat = [p for pt in pts for p in pt]
s = vase.splines.new('BEZIER')
s.bezier_points.add(len(pts) - 1)
s.bezier_points.foreach_set("co", flat)
for bp in s.bezier_points:
    bp.handle_left_type = bp.handle_right_type = 'AUTO'

bpy.ops.curve.primitive_bezier_curve_add()
ob = bpy.context.object
ob.data = vase

screw = ob.modifiers.new("Screw", 'SCREW')

bpy.ops.transform.resize(value=(0.509353, 0.509353, 0.509353), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

sourceName = bpy.context.object.name
source = bpy.data.objects[sourceName]
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
bpy.context.object.name = sourceName + "_Voxelized"
bpy.ops.object.convert(target='MESH')

source.hide_render = True
source.hide_viewport = True

targetName = bpy.context.object.name
target = bpy.data.objects[targetName]


bpy.ops.object.modifier_add(type='REMESH')
bpy.context.object.modifiers["Remesh"].mode = 'BLOCKS'
bpy.context.object.modifiers["Remesh"].octree_depth = 6
bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")
