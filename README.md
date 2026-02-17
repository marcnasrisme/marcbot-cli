# Marcbot

Marcbot is a single-file command-line game written in Python. You play as a quick-witted service bot racing around a neon city block to keep critical systems running while dodging glitches. Each turn you can move, scan for threats, stabilize systems, or recharge. The goal: survive long enough to restore all failing systems before the grid collapses.

## Features
- Turn-based gameplay on a procedurally generated 5×5 grid
- Simple resource management (energy + system stability)
- Random events and escalating glitches
- Colorized terminal output (optional)

## Requirements
- Python 3.9+

(Optional) Install `colorama` for nicer terminal colors:

```bash
pip install colorama
```

## Running the game

```bash
python marcbot_game.py
```

Follow the on-screen prompts to move (W/A/S/D), scan, stabilize, repair, or recharge. Win by stabilizing every critical system node before stability or energy hits zero.
