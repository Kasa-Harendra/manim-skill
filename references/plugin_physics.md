# manim-physics Plugin Reference Guide

`manim-physics` is a physics simulation extension for Manim Community. It provides 2D rigid-body mechanics powered by Pymunk, electrostatics (charges and electric field lines), magnetostatics (current-carrying wires and magnetic fields), geometric optics (refraction through lenses and ray tracing), and wave interference.

- **Repository**: [https://github.com/Matheart/manim-physics](https://github.com/Matheart/manim-physics)
- **Author**: Matheart, pdcxs, icedcoffeeee
- **Package**: `manim-physics`
- **Import Namespace**: `manim_physics`

---

## 1. Installation & Setup

```bash
pip install manim-physics pymunk
```

Import in your script:
```python
from manim import *
from manim_physics import *
```

---

## 2. Core Modules & APIs

### 1. Rigid Body Mechanics (`SpaceScene`)
Inherit from `SpaceScene` to activate the Pymunk physics engine:

```python
class PhysicsCollisionScene(SpaceScene):
    def construct(self):
        # Floor (static body)
        ground = Line(LEFT * 6, RIGHT * 6, color=GRAY).shift(DOWN * 3)
        self.add(ground)
        self.make_static_body(ground)

        # Dynamic falling bodies
        circle = Circle(radius=0.5, color=BLUE).shift(UP * 3 + LEFT * 0.5)
        square = Square(side_length=0.8, color=RED).shift(UP * 4 + RIGHT * 0.5)
        self.add(circle, square)

        self.make_rigid_body(circle, elasticity=0.8, density=1.0)
        self.make_rigid_body(square, elasticity=0.5, density=1.0)

        # Run live simulation
        self.wait(5)
```

---

### 2. Electromagnetism (`Charge`, `ElectricField`, `MagneticField`)

#### Electric Field Lines
```python
class ElectricDipoleScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        pos_charge = Charge(magnitude=1, point=LEFT * 2, color=RED)
        neg_charge = Charge(magnitude=-1, point=RIGHT * 2, color=BLUE)

        # Vector field formed by charges
        field = ElectricField(pos_charge, neg_charge)

        self.add(field, pos_charge, neg_charge)
        self.wait(1)
```

#### Magnetic Field Lines from Wires
```python
class MagneticFieldScene(ThreeDScene):
    def construct(self):
        wire = Wire(Circle(radius=2).rotate(PI / 2, UP), color=YELLOW)
        mag_field = MagneticField(wire)

        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.add(wire, mag_field)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
```

---

### 3. Geometric Optics (`Lens`, `Ray`)

Simulate ray refraction through convex and concave lenses:

```python
class LensRefractionScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Convex lens with focal distance
        lens = Lens(focal_distance=2.5, height=4, color=BLUE_C)
        self.add(lens)

        # Incident parallel rays
        rays = [
            Ray(start=LEFT * 5 + UP * y, direction=RIGHT, color=YELLOW_C)
            for y in np.linspace(-1.5, 1.5, 7)
        ]

        for ray in rays:
            self.add(ray)
            ray.propagate_through(lens)

        self.wait(2)
```

---

### 4. Wave Interference (`Wave`)

Simulates propagating wave crests and troughs:

```python
class WaveInterferenceScene(Scene):
    def construct(self):
        wave1 = Wave(source=LEFT * 2, wavelength=0.5, amplitude=0.3)
        wave2 = Wave(source=RIGHT * 2, wavelength=0.5, amplitude=0.3)
        self.add(wave1, wave2)
        self.wait(4)
```

---

## 3. Best Practices & 3b1b Aesthetic

1. **SpaceScene Updaters**: In `SpaceScene`, objects move automatically with delta-time during `self.wait(...)`. You do not need manual position updaters for falling/colliding bodies.
2. **Elasticity Calibration**: Set `elasticity` between `0.0` (completely inelastic collision) and `1.0` (perfectly elastic rebound) to create physically plausible demonstrations.
3. **Field Line Density**: Keep electric/magnetic field vector steps moderate (`step_size=0.5 - 0.8`) so arrow grids remain readable on 1080p video without visual moiré artifacts.
