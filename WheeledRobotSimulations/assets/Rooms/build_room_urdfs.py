import os
import sys
from object2urdf import ObjectUrdfBuilder

# Build Library of URDFs
object_folder = "todo"
builder = ObjectUrdfBuilder(object_folder)
builder.build_library(force_overwrite=True, decompose_concave=True, force_decompose=False, center='mass')

