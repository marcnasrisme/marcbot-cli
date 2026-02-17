#!/usr/bin/env python3
"""Marcbot – a terminal survival puzzler."""
from __future__ import annotations

import os
import random
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:  # pragma: no cover
    class Dummy:
        RESET_ALL = ""

        def __getattr__(self, _):
            return ""

    Fore = Style = Dummy()

    def colorama_init(*_, **__):
        return None

# Initialize colorama if available
colorama_init(autoreset=True)

Coord = Tuple[int, int]


@dataclass
class Node:
    position: Coord
    integrity: int = 3
    discovered: bool = False

    def is_stable(self) -> bool:
        return self.integrity <= 0

    def tick(self) -> bool:
        """Randomly deteriorate this node. Returns True if damaged."""
        if self.is_stable():
            return False
        if random.random() < 0.4:
            self.integrity = max(0, self.integrity - 1)
            return True
        return False


@dataclass
class Player:
    energy: int = 12
    system_stability: int = 12
    position: Coord = (2, 2)
    scan_charges: int = 2
    history: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        if len(self.history) > 6:
            self.history.pop(0)
        self.history.append(message)


class MarcbotGame:
    GRID = 5

    def __init__(self) -> None:
        self.player = Player()
        self.turn = 1
        self.nodes: Dict[Coord, Node] = {}
        self._seed_nodes()

    def _seed_nodes(self) -> None:
        all_coords = [(x, y) for x in range(self.GRID) for y in range(self.GRID)]
        random.shuffle(all_coords)
        for coord in all_coords[:5]:
            self.nodes[coord] = Node(position=coord, integrity=random.randint(2, 4))

    # ----------------------- Game helpers -----------------------
    def draw_grid(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{Fore.CYAN}=== MARCBOT : CITY NODE WATCH ==={Style.RESET_ALL}")
        print(f"Turn {self.turn} | Energy {self.player.energy} | Grid stability {self.player.system_stability}")
        print("Nodes stabilized: " + f"{self.stable_nodes}/{len(self.nodes)}")
        print("Scan charges: " + str(self.player.scan_charges))
        print("".rjust(2))
        for y in range(self.GRID):
            row = []
            for x in range(self.GRID):
                coord = (x, y)
                if coord == self.player.position:
                    icon = Fore.YELLOW + "M" + Style.RESET_ALL
                elif coord in self.nodes:
                    node = self.nodes[coord]
                    if node.discovered or node.is_stable():
                        icon = Fore.GREEN + "S" + Style.RESET_ALL if node.is_stable() else Fore.RED + "N" + Style.RESET_ALL
                    else:
                        icon = Fore.MAGENTA + "?" + Style.RESET_ALL
                else:
                    icon = "."
                row.append(icon)
            print(" ".join(row))
        print("".rjust(2))
        if self.player.history:
            print("Recent events:")
            for item in self.player.history[-4:]:
                print("  •", item)
        print()
        print("Commands: W/A/S/D move | scan | stabilize | recharge | wait | log")

    @property
    def stable_nodes(self) -> int:
        return sum(1 for node in self.nodes.values() if node.is_stable())

    def _neighbors(self, coord: Coord) -> List[Coord]:
        x, y = coord
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        results = []
        for dx, dy in deltas:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.GRID and 0 <= ny < self.GRID:
                results.append((nx, ny))
        return results

    def in_bounds(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.GRID and 0 <= y < self.GRID

    def move_player(self, direction: str) -> None:
        moves = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        if direction not in moves:
            self.player.log("Movement failed: invalid direction")
            return
        dx, dy = moves[direction]
        x, y = self.player.position
        new_coord = (x + dx, y + dy)
        if not self.in_bounds(new_coord):
            self.player.log("Marcbot bumps into a barrier.")
            self.player.energy -= 1
            return
        self.player.position = new_coord
        self.player.energy -= 1
        self.player.log(f"Moved to {new_coord}.")
        node = self.nodes.get(new_coord)
        if node:
            node.discovered = True

    def scan(self) -> None:
        if self.player.scan_charges <= 0:
            self.player.log("Scanner is depleted.")
            return
        self.player.scan_charges -= 1
        self.player.energy -= 1
        discovered = 0
        for coord in self._neighbors(self.player.position):
            node = self.nodes.get(coord)
            if node and not node.discovered:
                node.discovered = True
                discovered += 1
        self.player.log(f"Scanner pulse reveals {discovered} nearby node(s).")

    def stabilize(self) -> None:
        node = self.nodes.get(self.player.position)
        if not node:
            self.player.log("Nothing to stabilize here.")
            return
        if node.is_stable():
            self.player.log("Node already stable.")
            return
        node.integrity = max(0, node.integrity - 2)
        self.player.energy -= 1
        self.player.log("Stabilizer deployed!")

    def recharge(self) -> None:
        self.player.energy = min(15, self.player.energy + 3)
        self.player.system_stability = max(0, self.player.system_stability - 1)
        self.player.log("Rerouted spare power to energy reserves.")

    def wait(self) -> None:
        self.player.energy -= 1
        self.player.log("Holding position.")

    def random_events(self) -> None:
        # global stability tick
        if random.random() < 0.5:
            self.player.system_stability -= 1
            self.player.log("City grid flickers – stability dropping!")
        # node deterioration
        troubled = [node for node in self.nodes.values() if not node.is_stable()]
        if troubled:
            node = random.choice(troubled)
            if node.tick():
                self.player.log(f"Node at {node.position} destabilizes further!")

    def check_endgame(self) -> bool:
        if self.player.energy <= 0:
            print(Fore.RED + "Marcbot drained all energy. Shutdown imminent." + Style.RESET_ALL)
            return True
        if self.player.system_stability <= 0:
            print(Fore.RED + "City grid failed. Mission lost." + Style.RESET_ALL)
            return True
        if self.stable_nodes == len(self.nodes):
            print(Fore.GREEN + "All nodes stabilized. Marcbot saves the block!" + Style.RESET_ALL)
            score = self.player.system_stability + self.player.energy
            print(f"Final score: {score}")
            return True
        return False

    def handle_command(self, command: str) -> None:
        command = command.strip().lower()
        if not command:
            return
        if command in {"w", "a", "s", "d"}:
            self.move_player(command)
        elif command == "scan":
            self.scan()
        elif command == "stabilize":
            self.stabilize()
        elif command == "recharge":
            self.recharge()
        elif command == "wait":
            self.wait()
        elif command == "log":
            print("\n".join(self.player.history[-10:]) or "No logs yet.")
            input("(press Enter) ")
        else:
            self.player.log("Unknown command.")

    def run(self) -> None:
        while True:
            self.draw_grid()
            if self.check_endgame():
                break
            command = input("Action > ")
            self.handle_command(command)
            self.random_events()
            self.turn += 1


def main() -> int:
    random.seed()
    game = MarcbotGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nSession terminated. Marcbot powers down gently.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
