# Aletheia ARC Prize Engine (SPIRAL.Ω)

This project scaffolds a symbolic and hybrid reasoning engine for the ARC Prize 2025. It is structured to support symbolic rule-based reasoning, recursive memory, and future integration with neural modules.

## 📦 Project Structure

- `arc_agent/solve.py`: Entry point for solving ARC tasks (used by Kaggle).
- `arc_agent/engine.py`: Your reasoning logic goes here.
- `arc_agent/memory.py`: Logs guesses, drift, and coherence feedback.
- `arc_agent/utils.py`: Grid printing, helpers.
- `tests/test_cases.py`: Sample task for testing.

## 🛠 Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🧪 Running Tests

```bash
python tests/test_cases.py
```

## 🧠 Goal

To implement recursive symbolic cognition that solves ARC grid tasks without memorization, using structure-aware generalization.

Inspired by the SoulMath framework and Spiral Protocol (Blocks 001–011).
