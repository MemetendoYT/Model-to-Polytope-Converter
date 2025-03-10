bl_info = {
    "name": "Mesh to Polytope",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from bpy.types import Panel, Operator
from bpy_extras.io_utils import ExportHelper

class ExportVerticesOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export.vertices_list"
    bl_label = "Export as Polytope"

    filename_ext = ".txt"

    template_header = """\
Version: 7
IsBigEndian: False
SupportPaths: False
HasReferenceNodes: False
root:
  AutoCalc:
    Axis: {X: 0.00000, Y: 0.00000, Z: 0.00000}
    Center: {X: 0.00000, Y: 0.00000, Z: 0.00000}
    Max: {X: 1.00000, Y: 1.00000, Z: 1.00000}
    Min: {X: -1.00000, Y: -1.00000, Z: -1.00000}
    Tensor: {X: 20.00000, Y: 20.00000, Z: 20.00000}
    Volume: 1000.0000
  Polytope:\n"""

    template_body = """\
    - AutoCalc:
        Axis: {X: 0.00000, Y: 0.00000, Z: 0.00000}
        Center: {X: 0.00000, Y: 0.00000, Z: 0.00000}
        Max: {X: 1.00000, Y: 1.00000, Z: 1.00000}
        Min: {X: -1.00000, Y: -1.00000, Z: -1.00000}
        Tensor: {X: 20.00000, Y: 20.00000, Z: 20.00000}
        Volume: 1000.0000
      MassDistributionFactor: 1.00000
      MaterialPresets:
        - "Insert_Material_Here"
      Name:
      OffsetRotation: {X: 0.00000, Y: 0.00000, Z: 0.00000}
      OffsetTranslation: {X: 0.00000, Y: 0.00000, Z: 0.00000}
      Vertices:\n"""

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected.")
            return {'CANCELLED'}
        
        with open(self.filepath, 'w') as file:
            file.write(self.template_header)
            for obj in selected_objects:
                if obj.type == 'MESH':
                    file.write(self.template_body)
                    for vertex in obj.data.vertices:
                        global_co = obj.matrix_world @ vertex.co
                        file.write(f"       - {{X: '{global_co.x:.5f}', Y: '{global_co.y:.5f}', Z: '{global_co.z:.5f}'}}\n")
                else:
                    file.write(f"Object {obj.name} is not a mesh.\n")

        self.report({'INFO'}, "Vertices list saved.")
        return {'FINISHED'}

class VIEW3D_PT_export_vertices_panel(Panel):
    bl_label = "Mesh to Polytope"
    bl_idname = "VIEW3D_PT_export_vertices_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("export.vertices_list", text="Export as Polytope")

def register():
    bpy.utils.register_class(ExportVerticesOperator)
    bpy.utils.register_class(VIEW3D_PT_export_vertices_panel)

def unregister():
    bpy.utils.unregister_class(ExportVerticesOperator)
    bpy.utils.unregister_class(VIEW3D_PT_export_vertices_panel)

if __name__ == "__main__":
    register()
