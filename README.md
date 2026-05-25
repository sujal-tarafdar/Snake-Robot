# 🐍 Snake Robot — Rolling Locomotion (Webots R2025a)

A complete Webots simulation of a **12-joint rolling snake robot** using
alternating Horizontal / Vertical hinge joints and sinusoidal wave gait.

---

## 📁 Project Structure

```
snake_robot/
├── worlds/
│   └── snake.wbt                          ← Open this in Webots
└── controllers/
    └── snake_controller/
        └── snake_controller.py            ← Python controller (auto-loaded)
```

---

## 🚀 Quick Start

1. **Open Webots R2025a**
2. `File → Open World…` → select `worlds/snake.wbt`
3. Click **▶ Play**
4. The snake will begin rolling forward immediately.

> ⚠️ Webots auto-discovers the controller because its folder name matches the
> `controller` field in the `.wbt` file (`"snake_controller"`).  
> Make sure both files are in the paths shown above.

---

## 🤖 Robot Architecture

```
Robot (segment_0 / HEAD)
 └─ HingeJoint [H0]  axis=(0 1 0)  motor_H_0
     └─ segment_1
         └─ HingeJoint [V1]  axis=(1 0 0)  motor_V_1
             └─ segment_2
                 └─ HingeJoint [H2]  axis=(0 1 0)  motor_H_2
                     └─ segment_3
                         └─ HingeJoint [V3]  axis=(1 0 0)  motor_V_3
                             └─ segment_4
                                 └─ HingeJoint [H4]  ...
                                     ...
                                         └─ segment_12 (TAIL)
```

| Parameter         | Value         |
|-------------------|---------------|
| Total joints      | 12            |
| Pattern           | H-V H-V × 6  |
| Segment radius    | 0.03 m        |
| Segment height    | 0.12 m        |
| Segment mass      | 0.08 kg (head 0.10 kg) |
| Joint range       | ±90° (±π/2)   |

---

## 🌊 Rolling Gait Equations

```
θ_H(i, t) = A_H × sin(ω·t + φ·i)
θ_V(i, t) = A_V × cos(ω·t + φ·i + π/2)
```

| Symbol | Value    | Meaning                          |
|--------|----------|----------------------------------|
| A_H    | 0.6 rad  | Horizontal amplitude (~34°)      |
| A_V    | 0.4 rad  | Vertical amplitude   (~23°)      |
| ω      | 1.8 rad/s| Angular (temporal) frequency     |
| φ      | π/3 rad  | Spatial phase shift per pair     |
| i      | 0–5      | Joint-pair index                 |

The **π/2 phase offset** between the H and V planes produces a
helical travelling wave — the hallmark of sidewinder / rolling locomotion.

---

## 🎛️ Tuning the Gait

Edit the top of `snake_controller.py`:

```python
A_H   = 0.6        # increase for wider horizontal sweeps
A_V   = 0.4        # increase for taller vertical undulations
OMEGA = 1.8        # increase for faster rolling
PHI   = math.pi/3  # decrease for longer body wavelength
```

### Preset table

| Mode          | A_H  | A_V  | OMEGA | PHI    |
|---------------|------|------|-------|--------|
| Slow roll     | 0.4  | 0.3  | 1.0   | π/4    |
| Default roll  | 0.6  | 0.4  | 1.8   | π/3    |
| Fast spiral   | 0.8  | 0.5  | 2.5   | π/2.5  |
| Sidewinder    | 0.7  | 0.2  | 2.0   | π/3    |

---

## ⚙️ Physics Notes

* Every segment has a `Physics` node (mass 0.08 kg) and a `boundingObject`
  Cylinder — no floating or disconnected bodies.
* `ContactProperties` set `coulombFriction 0.8` on material `"snake_body"`.
* `dampingConstant 0.1` on every joint prevents chaotic oscillation.

---

## 🛠️ Troubleshooting

| Symptom | Fix |
|---------|-----|
| Controller not found | Ensure folder is `controllers/snake_controller/` |
| Robot falls through floor | Rebuild the world (Ctrl+Shift+R) |
| Joints all at zero | Check motor names match exactly (case-sensitive) |
| Slow simulation | Reduce `basicTimeStep` from 16 → 32 ms |

---

## 📜 Compatibility

- **Webots R2025a** (VRML_SIM R2025a header)
- Python 3.8+
- No external dependencies beyond the Webots `controller` library
