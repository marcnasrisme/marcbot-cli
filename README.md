# Marcbot

A single-file terminal survival puzzler in Python. You play a service bot trying to stabilize critical systems on a procedurally generated 5×5 grid before glitches consume the network.

Each turn you can move, scan for threats, stabilize a node, or recharge. Energy drains, glitches escalate, integrity decays. Restore every node before the grid collapses.

```bash
python marcbot_game.py
```

## Gameplay

| Action | Effect |
|---|---|
| **Move** (W/A/S/D) | Step one tile; reveals adjacent nodes |
| **Scan** | Reveal threats and degraded nodes |
| **Stabilize** | Restore the node under you (consumes energy) |
| **Recharge** | Refill energy at the cost of a turn |
| **Repair** | Heal a damaged node |

Win condition: every critical node restored. Lose condition: energy or system stability hits zero.

## Why it's interesting (briefly)

It's a small project, but it leans on a few things worth showing:

- **Pure stdlib** for the simulation — `dataclass`-driven node and bot state, deterministic seeds for reproducibility
- **Procedural grid generation** with controlled difficulty curves (glitch spawn rate scales with turn count)
- **Stateful turn loop** with separate tick phases for environment decay, agent action, and event spawn — clean separation makes it easy to add new actions
- **Graceful color fallback** — works whether or not `colorama` is installed

## Requirements

Python 3.9+

Optional (nicer terminal colors):

```bash
pip install colorama
```

## Files

- `marcbot_game.py` — entire game in 252 lines
- `requirements.txt` — single optional dependency
