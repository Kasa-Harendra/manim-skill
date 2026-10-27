# manim-meshes Plugin Reference Guide

`manim-meshes` is a 3D geometry and mesh visualization extension developed by the Interactive Graphics Systems Group (GRIS) at TU Darmstadt. It brings polygonal surface meshes, node-face topologies, `trimesh` integration, and Delaunay/Voronoi computational geometry into Manim Community.

- **Repository**: [https://github.com/bmmtstb/manim-meshes](https://github.com/bmmtstb/manim-meshes)
- **Authors**: Martin Steinborn, Vicky Hagemeister (TU Darmstadt)
- **Package**: `manim-meshes`
- **Import Namespace**: `manim_meshes`

---

## 1. Installation & Setup

```bash
pip install manim-meshes trimesh
```

### Renderer Requirement: OpenGL
Mesh rendering relies on OpenGL rasterization. Always render scenes containing `manim-meshes` with the `--renderer=opengl` flag:

```bash
manim --renderer=opengl -pql script.py MyMeshScene
```
Or set within the script:
```python
config.renderer = "opengl"
```

---

## 2. Core Mesh Classes & Architecture

### `Mesh` (Data Model)
Pure topological data container representing vertices and faces:
```python
from manim_meshes.models.data_models.mesh import Mesh

mesh_data = Mesh(
    vertices=[
        [1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0],
        [-1, 1, 0],
        [0, 0, 2]  # Apex
    ],
    faces=[
        [0, 4, 1],
        [1, 4, 2],
        [2, 4, 3],
        [3, 4, 0],
        [0, 1, 2],
        [2, 3, 0]
    ]
)
```

### `ManimMesh` & `Manim2DMesh` (Mobjects)
Manim visual wrappers around `Mesh` instances that support scaling, shifting, face color mapping, and wireframe opacity:

```python
from manim_meshes.models.manim_models.basic_mesh import ManimMesh

manim_mesh = ManimMesh(mesh=mesh_data)
self.add(manim_mesh)
```

### `TriangleManim2DMesh` & Delaunay Modules
Specialized 2D triangle mesh class for computational geometry, Voronoi duals, and Delaunay circumcircles:
```python
from manim_meshes.models.manim_models.triangle_mesh import TriangleManim2DMesh
from manim_meshes.delaunay.delaunay_criterion import get_circum_circle
from manim_meshes.delaunay.voronoi import VoronoiDelaunay
```

### Procedural Templates
Convenience functions in `manim_meshes.templates`:
- `create_triangle()`
- `create_pyramid()`
- `create_grid(x_nodes=5, y_nodes=5)`
- `create_model(name="suzanne" | "armadillo" | "tail_topper")`

---

## 3. Production Recipes

### Recipe 1: 3D Animated Wireframe Pyramid

```python
from manim import *
from manim_meshes.models.manim_models.basic_mesh import ManimMesh
from manim_meshes.templates import create_pyramid
import numpy as np

config.renderer = "opengl"

class PyramidMeshScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Setup camera orientation
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)

        # 2. Build topological mesh from template
        pyramid_data = create_pyramid()
        pyramid_data.scale_mesh(1.8)

        # 3. Create visual mobject
        mesh_mobject = ManimMesh(mesh=pyramid_data)
        self.add(mesh_mobject)

        title = Tex(r"\textbf{Topological Polyhedron Mesh}", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # 4. Smooth 3D camera pan & continuous rotation
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=80 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.wait(1)
```

---

### Recipe 2: Delaunay Triangulation & Circumcircle Criterion

```python
from manim import *
from manim_meshes.models.manim_models.triangle_mesh import TriangleManim2DMesh
from manim_meshes.templates import create_coplanar_triangles
from manim_meshes.delaunay.delaunay_criterion import get_circum_circle

config.renderer = "opengl"

class DelaunayCriterionScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Coplanar triangles
        triangles_mesh = create_coplanar_triangles()
        mesh_mobject = TriangleManim2DMesh(mesh=triangles_mesh)
        mesh_mobject.scale(2.0)

        self.play(Create(mesh_mobject), run_time=1.5)
        self.wait(0.5)

        # 2. Circumcircle of face 0
        circle_mobject = get_circum_circle(triangles_mesh, face_idx=0)
        circle_mobject.set_color(YELLOW_C)

        label = Tex(r"\textbf{Delaunay Empty Circumcircle Property}", font_size=28).to_edge(UP, buff=0.6)
        self.play(FadeIn(label), Create(circle_mobject), run_time=1.2)
        self.wait(1)

        # Highlight valid Delaunay condition
        self.play(Indicate(circle_mobject, color=GREEN_C))
        self.wait(1)
```

---

## 4. Best Practices

1. **OpenGL Requirement**: Always execute with `--renderer=opengl`. The Cairo renderer is not optimized for custom mesh shaders and vertex indices.
2. **Mesh Scale Limits**: For standard animated scenes, keep mesh resolutions below $\approx 1{,}000$ vertices for smooth interactive rendering with `ManimMesh`.
3. **Pure Black Contrast**: 3D wireframe edges stand out best against `BLACK`. Set edge stroke colors to `BLUE_D`, `TEAL_C`, or `YELLOW_C` for maximum readability.
