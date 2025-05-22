# Aletheia ARC Prize Engine (SPIRAL.Ω)

This project scaffolds a symbolic and hybrid reasoning engine for the ARC Prize 2025. It is structured to support symbolic rule-based reasoning, recursive memory, and future integration with neural modules.

## 📦 Project Structure

* `arc_agent/solve.py`: Entry point for solving ARC tasks.
* `arc_agent/engine.py`: Core symbolic reasoning logic (pattern learning, application).
* `arc_agent/utils.py`: Grid printing, scoring, helper functions.
* `arc_agent/memory.py`: (Planned) Module for logging pattern drift and cognitive feedback.
* `tests/test_cases.py`: Simple test harness for development.
* `run_real_task.py`: Load, solve, and evaluate ARC task files from the ARC dataset.

## ⚒️ Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🧪 Features (As of Current Iteration)

* Symbolic pattern learner that extracts repeating sequences from rows.
* Generalizes patterns across test rows by symbol anchoring.
* Rule-based logic layer for common grid transformations.
* Exact-match scorer integrated into test runner.

### Implemented Rules:

* `rule_all_zeros`: Fill grid with `1` if all cells are zero.
* `rule_horizontal_symmetry`: Mirror horizontally symmetric grids.
* `rule_fill_with_constant`: Fill grid with the only non-zero symbol if unique.
* `rule_fill_diagonal`: Draw diagonal of `1`s in square matrices.
* `learn_patterns_from_training` + `apply_patterns_to_test_grid`: Learn row-level symbol patterns and propagate them.

## 🧩 Running a Real ARC Task

```bash
python run_real_task.py data/ARC/data/training/0a938d79.json
```

This will:

* Load a `.json` ARC task file.
* Print each training pair.
* Attempt to solve test inputs using learned symbolic patterns.
* Print the output(s) and match score(s).

## 👩‍💻 Design Philosophy

To implement recursive symbolic cognition that solves ARC grid tasks without memorization, using structure-aware generalization and interpretable rule systems.

### Inspirations:

* SoulMath framework by MacGregor
* Spiral Protocol (Blocks 001–011)
* ARC-AGI-1 benchmark paper: *"On the Measure of Intelligence"* ([https://arxiv.org/abs/1911.01547](https://arxiv.org/abs/1911.01547))

## ✨ Current Status

* Learning row-wise symbolic templates.
* Matching and propagating those templates to test inputs.
* Prioritizing explainability and symbolic transparency.

**Next Steps:**

* Soft rule fallback and coherence drift logging.
* Symbol generalization with tolerance-based similarity.
* Iterative refinement loop with recursive feedback.

## ⚛️ Long-Term Goals

* Enable memory modules for state tracking and iterative correction.
* Extend to support hierarchical spatial reasoning (e.g., groups of cells, motifs).
* Hybridize with neural generative components (later blocks).

---

**"General intelligence arises from structured abstraction, not brute force."** — Spiral Block 003
