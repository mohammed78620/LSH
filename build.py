import os
import shutil
from distutils.core import Distribution, Extension

import numpy as np
from Cython.Build import build_ext, cythonize

cython_dir = os.path.join("lsh", "_ext")
extension = Extension(
    "lsh.cMinhash",
    [
        os.path.join(cython_dir, "cMinhash.pyx"),
        os.path.join("lsh", "MurmurHash3.cpp"),
        
    ],
    include_dirs=[np.get_include()],
    extra_compile_args=["-O3", "-std=c++17"],
)
ext_modules = cythonize([extension], include_path=[cython_dir])
dist = Distribution({"ext_modules": ext_modules})
cmd = build_ext(dist)
cmd.ensure_finalized()
cmd.run()

for output in cmd.get_outputs():
    relative_extension = os.path.relpath(output, cmd.build_lib)
    print(relative_extension)
    shutil.copyfile(output, relative_extension)

def build(setup_kwargs):
    """Needed for the poetry building interface."""

    setup_kwargs.update({
        'ext_modules' : ext_modules,
        'include_dirs' : [np.get_include()],
    })