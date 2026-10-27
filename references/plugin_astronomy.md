# manim-Astronomy Plugin Reference Guide

`manim-Astronomy` is an extension for Manim Community designed for astronomical, astrophysical, and gravitational visualizations. It provides procedural celestial bodies, particle stars, planetary ring systems, and dynamic 3D spacetime fabric grids for illustrating General Relativity.

- **Repository**: [https://github.com/hassamrajpoot/manim-Astronomy](https://github.com/hassamrajpoot/manim-Astronomy)
- **Author**: Hassam ul Haq
- **Package**: `manim-Astronomy`
- **Import Namespace**: `manim_Astronomy`

---

## 1. Installation & Requirements

Ensure your environment satisfies Python $\ge 3.11$:

```bash
pip install manim-Astronomy vedo
```

### Renderer Configuration
Many components inherit from `metaclass=ConvertToOpenGL`. While basic scenes work in default Cairo, OpenGL mode provides accelerated particle and 3D wireframe performance:

```python
from manim import *
from manim_Astronomy import Star, Planet, SpaceTimeFabric

# Optional but recommended for heavy particle swarms:
config.renderer = "opengl"
```

---

## 2. Core Components & Class APIs

### `Star`
Creates a luminous celestial star generated as a 3D spherical particle cloud (`Dot3D` particles) with randomized angular distribution.

```python
Star(
    center=ORIGIN,               # Point3D: Center position [x, y, z]
    radius=0.5,                  # float: Outer radius of particle sphere
    num_of_particles=1000,       # int: Total particle density
    size_of_particle=0.005,      # float: Radius of each Dot3D particle (see note below)
    colors=[YELLOW],             # list[str]: Palette sampled for particle colors
    luminosity=1.0,              # float: Particle fill_opacity (0.0 to 1.0)
    mass=1.0,                    # float: Metadata mass parameter
    temperature=6000,            # float: Blackbody temp in Kelvin (metadata)
    **kwargs
)
```

> [!TIP]
> **Particle Size Gotcha**: The default package parameter `size_of_particle=0.000001` is microscopic and can be invisible at 1080p. Always pass an explicit `size_of_particle` between `0.001` and `0.01` (e.g. `size_of_particle=0.005`) for crisp, glowing stars.

---

### `Planet`
Creates a spherical celestial body (`Dot3D`) with an optional planar ring system (debris disc) populated by orbital particles.

```python
Planet(
    center=ORIGIN,               # Point3D: Center location
    radius=0.05,                 # float: Central sphere radius
    include_planetary_disc=False,# bool: Whether to render orbital rings
    ring_inner_radius=0.1,       # float: Disc inner boundary
    ring_outer_radius=0.15,      # float: Disc outer boundary
    num_particles=100,           # int: Disc particle count
    size_of_particle=0.01,       # float: Size of ring particles
    color=BLUE,                  # Passed via **kwargs to central sphere
    **kwargs
)
```

---

### `SpaceTimeFabric`
Generates a parametric 3D wireframe mesh deformed by a gravitational potential or wave equation $z = s \cdot f(u, v, \dots)$.

```python
SpaceTimeFabric(
    func=None,                   # Callable: f(u, v, *func_args) returning z-height/potential
    func_args=(),                # tuple: Additional args forwarded to func
    u_range=(-1, 1),             # tuple: (u_min, u_max)
    v_range=(-1, 1),             # tuple: (v_min, v_max)
    resolution=(50, 50),         # tuple: (grid_lines_u, grid_lines_v)
    scaling_factor=0.1,          # float: Multiplier for func z-displacement
    t_range=(-1, 1),             # tuple: Parametric curve range
    stroke_color=BLUE_D,         # Wireframe color
    stroke_opacity=1.5,          # Wireframe stroke width
    **kwargs
)
```

Dynamic deformation is achieved by attaching an updater with `mob.become(SpaceTimeFabric(...))`.

---

### `HubbleSpaceTelescope` & `JamesWebbSpaceTelescope`
Loads 3D polygonal wavefront meshes via `vedo` and projects them into Manim `Polygon` mobjects.

```python
from manim_Astronomy import HubbleSpaceTelescope, JamesWebbSpaceTelescope

# Note: The built-in class attempts to load mesh from relative path "./Assets/hubble.obj"
# Ensure the Assets/ directory containing the .obj file exists in your project working directory.
telescope = HubbleSpaceTelescope(center=ORIGIN, size=0.5)
```

---

## 3. Production Animation Recipes

### Recipe 1: Kepler's Second Law (Elliptical Orbit & Swept Area)

Demonstrates equal area swept out in equal time intervals by an orbiting planet:

```python
from manim import *
from manim_Astronomy import Star, Planet
import numpy as np

class KeplersSecondLawScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Central Star with visible particle glow
        star = Star(
            center=ORIGIN,
            radius=0.8,
            num_of_particles=1200,
            size_of_particle=0.004,
            colors=[YELLOW_D, YELLOW_C, ORANGE]
        )
        self.add(star)

        # 2. Elliptical trajectory: x = a*cos(t), y = b*sin(t)
        a, b = 4.0, 2.5
        orbit = ParametricFunction(
            lambda t: np.array([a * np.cos(t), b * np.sin(t), 0]),
            t_range=[0, TAU],
            color=BLUE_E,
            stroke_width=2.0
        )
        self.add(orbit)

        # 3. Planet with ring system
        planet = Planet(
            center=orbit.point_from_proportion(0),
            radius=0.12,
            include_planetary_disc=True,
            ring_inner_radius=0.18,
            ring_outer_radius=0.28,
            num_particles=60,
            size_of_particle=0.008,
            color=TEAL
        )
        self.add(planet)

        # 4. Orbit animation via ValueTracker
        time_tracker = ValueTracker(0)
        planet.add_updater(lambda mob: mob.move_to(orbit.point_from_proportion(time_tracker.get_value() % 1.0)))

        # 5. Swept sector generator
        def get_swept_sector(start, end, num_points=40):
            start = np.clip(start, 0.0, 1.0)
            end = np.clip(end, 0.0, 1.0)
            alphas = np.linspace(start, end, num_points)
            pts = [ORIGIN] + [orbit.point_from_proportion(alpha) for alpha in alphas]
            return Polygon(*pts, stroke_width=0, fill_color=YELLOW_C, fill_opacity=0.35)

        # 6. Swept intervals
        intervals = [(0.05, 0.15), (0.45, 0.55)]
        swept_areas = VGroup()

        def update_swept():
            curr = time_tracker.get_value()
            for start, end in intervals:
                if start <= curr <= end:
                    swept_areas.add(get_swept_sector(start, curr))
            return swept_areas

        sweep_group = always_redraw(update_swept)
        self.add(sweep_group)

        # Camera orientation for 3D depth
        self.set_camera_orientation(phi=65 * DEGREES, theta=-75 * DEGREES)
        self.play(time_tracker.animate.set_value(1.0), run_time=10, rate_func=linear)
        self.wait(1)
```

---

### Recipe 2: Spacetime Distortion by Moving Gravitational Masses

Deforms a 2D spacetime fabric dynamically as a mass orbits around a central body:

```python
from manim import *
from manim_Astronomy import SpaceTimeFabric
import numpy as np

def multi_body_potential(u, v, mass_positions, masses, softening=0.15):
    potential = 0.0
    for pos, m in zip(mass_positions, masses):
        r_sq = (u - pos[0])**2 + (v - pos[1])**2 + (pos[2])**2
        r = np.sqrt(r_sq) + softening
        potential += -m / r
    return potential

class SpacetimeCurvatureDemo(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK

        # Massive bodies
        central_star = Dot3D(point=ORIGIN, radius=0.25, color=YELLOW_C)
        orbiting_planet = Dot3D(point=[1.5, 0, 0], radius=0.08, color=BLUE_C)
        self.add(central_star, orbiting_planet)

        # Dynamic Fabric
        fabric = SpaceTimeFabric(
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(40, 40),
            t_range=(-3, 3),
            scaling_factor=0.03,
            stroke_color=BLUE_E,
            stroke_opacity=1.5,
            func=multi_body_potential,
            func_args=([central_star.get_center(), orbiting_planet.get_center()], [35.0, 8.0])
        )
        self.add(fabric)

        # Camera tilt
        self.set_camera_orientation(phi=65 * DEGREES, theta=-80 * DEGREES)

        # Orbit motion
        angle_tracker = ValueTracker(0)

        def update_planet_pos(mob):
            ang = angle_tracker.get_value()
            mob.move_to(np.array([1.5 * np.cos(ang), 1.5 * np.sin(ang), 0]))

        orbiting_planet.add_updater(update_planet_pos)

        # Fabric updater
        def update_fabric(mob):
            mob.become(SpaceTimeFabric(
                u_range=(-3, 3),
                v_range=(-3, 3),
                resolution=(40, 40),
                t_range=(-3, 3),
                scaling_factor=0.03,
                stroke_color=BLUE_E,
                stroke_opacity=1.5,
                func=multi_body_potential,
                func_args=([central_star.get_center(), orbiting_planet.get_center()], [35.0, 8.0])
            ))

        fabric.add_updater(update_fabric)

        self.play(angle_tracker.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait(1)
```

---

### Recipe 3: Gravitational Waves Post-Black Hole Merger

Simulates circular ripple wave propagation across the spacetime grid following a coalescence event:

```python
from manim import *
from manim_Astronomy import SpaceTimeFabric
import numpy as np

def ripple_wave(u, v, t, amplitude=0.3, wavelength=0.6, speed=1.8):
    dist = np.sqrt(u**2 + v**2)
    # Damped outgoing sinusoidal wave
    phase = 2 * PI * (dist - speed * t) / wavelength
    decay = np.exp(-0.35 * dist)
    return amplitude * np.sin(phase) * decay

class GravitationalWaveScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK

        # Merged singularity
        merger_singularity = Dot3D(point=ORIGIN, radius=0.15, color=DARK_GREY)
        self.add(merger_singularity)

        t_tracker = ValueTracker(0.0)

        fabric = SpaceTimeFabric(
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(45, 45),
            t_range=(-3, 3),
            scaling_factor=0.15,
            stroke_color=TEAL_E,
            stroke_opacity=1.2,
            func=ripple_wave,
            func_args=(0.0,)
        )
        self.add(fabric)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-70 * DEGREES)

        fabric.add_updater(lambda mob: mob.become(
            SpaceTimeFabric(
                u_range=(-3, 3),
                v_range=(-3, 3),
                resolution=(45, 45),
                t_range=(-3, 3),
                scaling_factor=0.15,
                stroke_color=TEAL_E,
                stroke_opacity=1.2,
                func=ripple_wave,
                func_args=(t_tracker.get_value(),)
            )
        ))

        self.play(t_tracker.animate.increment_value(4.0), run_time=8, rate_func=linear)
        self.wait(1)
```

---

## 4. Best Practices & 3Blue1Brown Integration

1. **Pure Black Cosmos**: Always ensure `self.camera.background_color = BLACK`. Stars and spacetime fabrics look crispest against absolute `#000000`.
2. **Resolution vs. Performance in `SpaceTimeFabric`**: A grid resolution of `(35, 35)` to `(50, 50)` provides the ideal trade-off between smooth curves and responsive updater rendering. Going above `(80, 80)` during live updaters can dramatically slow down frame generation.
3. **Softening Factor $\epsilon$**: When calculating point mass potentials $V = -G M / r$, always include a small softening parameter (e.g. $r = \sqrt{\Delta x^2 + \Delta y^2 + z^2} + \epsilon$) to prevent division by zero or infinite wireframe spikes at object centers.
4. **Camera Choreography**: Astronomical visualizations require continuous 3D perspective shifts. Combine orbital motion with gentle camera panning (`self.begin_ambient_camera_rotation(rate=0.05)` or `self.move_camera(phi=..., theta=..., run_time=...)`).
