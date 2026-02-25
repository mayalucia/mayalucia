+++
title = "Data Foundations"
author = ["A Human-Machine Collaboration"]
lastmod = 2026-02-25T12:00:00+01:00
tags = ["bravli", "data", "lesson"]
draft = false
+++

Before building anything, we need a principled way to manage scientific data --- datasets that are large, heterogeneous, version-sensitive, and expensive to recompute. The data foundations layer establishes the abstractions that every subsequent lesson builds on.

## Lessons Covered

### Lesson 00 --- Foundations
Datasets, lazy evaluation, and the shape of scientific data management. Introduces the `@evaluate_datasets` decorator pattern: scientific functions declare what data they need, and the framework resolves, caches, and validates dependencies automatically.

### Lesson 01 --- Parcellation
The fly brain's geography: 78 neuropil regions organised in a spatial hierarchy. This lesson builds the anatomical coordinate system that all subsequent analyses reference.

### Lesson 02 --- Composition
Cell type counts and neurotransmitter profiles per brain region. Statistical description of circuit heterogeneity: how many neurons of each type, what neurotransmitter they release, where they project.

### Lesson 03 --- Factology
Structured scientific measurements: every number earns a name. The `@fact` and `@structural` decorators create reproducible, versioned factsheets for any circuit or brain region.

---

**Source files:**
- [`domains/bravli/codev/00-foundations.org`](https://github.com/mayalucia/bravli) (801 lines)
- [`domains/bravli/codev/01-parcellation.org`](https://github.com/mayalucia/bravli) (875 lines)
- [`domains/bravli/codev/02-composition.org`](https://github.com/mayalucia/bravli) (401 lines)
- [`domains/bravli/codev/03-factology.org`](https://github.com/mayalucia/bravli) (618 lines)
