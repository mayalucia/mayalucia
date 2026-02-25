+++
title = "Magnetic Landscapes"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["mayajiva", "landscape", "geophysics"]
draft = false
+++

The landscape is the world the bug navigates --- a 2D magnetic field environment that models the Earth's geomagnetic field plus geological anomalies. The uniform geomagnetic field provides the compass signal; the anomalies test the compass's robustness.

## Geomagnetic Background

The background field is characterised by:
- **Declination** --- the angle between geographic and magnetic north
- **Inclination** --- the dip angle (how steeply field lines plunge into the Earth)
- **Total intensity** --- ~50 μT at mid-latitudes

An inclination compass (like the radical-pair mechanism) measures the angle between the field and the local vertical, not the field direction. This means it cannot distinguish north from south --- it detects the axis, not the polarity.

## Anomaly Types

| Type | Model | Physical Origin |
|------|-------|----------------|
| Gaussian | Localised intensity perturbation | Ore body, volcanic intrusion |
| Dipole | 1/r³ decay, full vector field | Magnetised rock, buried object |
| Fault | Step function in inclination | Geological contact, fault line |
| Gradient | Linear variation across domain | Regional tectonic structure |

Anomalies can reach hundreds of nanotesla --- significant compared to the few-percent anisotropy that the compass relies on. The model reveals that same-frame bias cancellation (subtracting a reference channel) provides robust anomaly rejection up to ~500 nT.

---

**Source:** [`modules/mayajiva/experiment/landscape.py`](https://github.com/mayalucia/mayajiva) (248 lines), [`src/core/landscape.hpp`](https://github.com/mayalucia/mayajiva) (164 lines)
