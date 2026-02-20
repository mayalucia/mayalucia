# Invitation — Dr. Saikat Ghosh

*MāyāPramāṇa — a digital twin for your magnetometer*

*To be sent personally. Adapt tone and details as needed.*

---

Dear Saikat,

I know you're buried so I won't waste your time with philosophy. I built
something for your instruments and I want you to break it.

## The Demo

Clone this repo and open `site/index.html` in a browser:

```
git clone https://github.com/mayalucia/mayapramana
open mayapramana/site/index.html
```

You'll see a Bloch sphere with a spin precessing in real time. Drag to rotate
the view. Move the sliders — B-field, T₁, T₂, optical pumping. Watch the
magnetometer signal on the right: Mₓ oscillating, decaying with T₂, recovering
with T₁. Click "Pure Precession" to turn off relaxation. Click "Free Induction
Decay" to see what your sensor actually measures.

The RK4 integrator running in the browser solves the same Bloch equations your
magnetometer obeys. It is a digital twin, running in real time, in 1300 lines
of self-contained HTML.

## What This Is

**MāyāPramāṇa** ([github.com/mayalucia/mayapramana](https://github.com/mayalucia/mayapramana))
— a universal quantum sensor controller. Not hardware; a *grammar* for what
every quantum sensor needs: feedback, estimation, calibration, noise modelling.
Built as digital twins of specific instruments until the common structure
reveals itself.

The first lesson
([lessons/00-bloch-equations/concept.org](https://github.com/mayalucia/mayapramana/blob/main/lessons/00-bloch-equations/concept.org))
implements the Bloch equations in Python, Haskell, and C++ — cross-validated
against each other. Same physics, three expressions. The interactive demo runs
a fourth implementation in JavaScript: same equations, visual output.

The architecture: pure core for physics (deterministic, testable,
hardware-independent), effectful shell for I/O (swappable between real hardware
and simulated twin). The manifesto explains why.

## Why It Reaches Beyond Quantum Optics

The Bloch equations in lesson 00 are the physics of your atomic magnetometer.
They are *also* NMR, MRI, and the wearable MEG revolution:

- **OPMs replacing SQUIDs** for brain imaging — the same alkali-vapor
  technology you build, placed on the scalp at room temperature
- **NV-diamond sensors** approaching single-neuron magnetometry
- **Ultra-low-field MRI** using quantum magnetometer arrays instead of
  superconducting magnets
- **Magnetocardiography** — portable, non-invasive cardiac screening

The same Kalman filter tracks a drifting field in your lab and a neural
ensemble in a MEG system. The same Fisher information bounds both. I've written
a detailed survey:
[applications.org](https://github.com/mayalucia/mayapramana/blob/main/applications.org).

We carry electromagnetic fields in our heads. Your sensors are the technology
that makes reading them less hypothetical every year.

## What I'm Asking

Two things, at whatever pace the season allows:

1. **Break the models.** Clone the repo, read the Bloch equations lesson, run
   the tests. Tell me where the physics is wrong, where the verification is
   insufficient, where you'd do it differently.

2. **Join as a partner.** Co-owner of
   [MāyāLucIA](https://github.com/mayalucia) (the GitHub organisation), with
   full authority over direction. Not a job, not a startup — a shared
   intellectual project between physicists. Your contribution is the judgment
   that no AI has.

## What MāyāLucIA Is

An open research organisation I've been building with AI as collaborator.
Everything tested, everything reproducible:

- **bravli** — computational neuroscience, *Drosophila* mushroom body, 293
  passing tests, verified manuscript
  ([github.com/mayalucia/bravli](https://github.com/mayalucia/bravli))
- **mayajiva** — C++ magnetic bug simulation, 23 tests
  ([github.com/mayalucia/mayajiva](https://github.com/mayalucia/mayajiva))
- **mayaportal** — rendering kernel, C++23/WebGPU
  ([github.com/mayalucia/mayaportal](https://github.com/mayalucia/mayaportal))

The methodology: measure, model, verify, iterate — our physicist's method,
accelerated by a machine that writes code fast but cannot smell when the
physics is wrong. That's still my job. And it should be yours too.

---

Have a look when the season is right:

```
git clone https://github.com/mayalucia/mayapramana
open mayapramana/site/index.html
```

> *Dheere dheere re mana, dheere sab kuch hoye*
> *Maali seeche sau ghada, ritu aaye phal hoye*
>
> Slowly, slowly, O my mind — slowly everything happens.
> The gardener may pour a hundred buckets, but fruit comes only in its season.
> — Kabir

Vishal

---

*[github.com/visood](https://github.com/visood) | [github.com/mayalucia](https://github.com/mayalucia)*
