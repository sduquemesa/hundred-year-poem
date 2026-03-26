from __future__ import annotations

import argparse
import importlib
import pkgutil
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


VOWEL_SHIFT = str.maketrans(
    {
        "a": "e",
        "e": "i",
        "i": "o",
        "o": "u",
        "u": "a",
        "A": "E",
        "E": "I",
        "I": "O",
        "O": "U",
        "U": "A",
    }
)


@dataclass
class PoemState:
    current_text: str = ""
    output: List[str] = field(default_factory=list)
    trace: List[str] = field(default_factory=list)

    def emit(self, text: str) -> None:
        self.output.append(text)

    def log(self, message: str) -> None:
        self.trace.append(message)


class Primitive:
    name = ""
    help_text = ""

    def apply(self, state: PoemState, args: str) -> None:
        raise NotImplementedError


class Seed(Primitive):
    name = "seed"
    help_text = 'seed "text"'

    def apply(self, state: PoemState, args: str) -> None:
        text = parse_quoted_text(args)
        state.current_text = text
        state.emit(text)
        state.log(f'seed -> "{text}"')


class Repeat(Primitive):
    name = "repeat"
    help_text = "repeat N"

    def apply(self, state: PoemState, args: str) -> None:
        count = int(args.strip())
        for _ in range(count):
            state.emit(state.current_text)
        state.log(f"repeat -> {count}")


class Pause(Primitive):
    name = "pause"
    help_text = "pause"

    def apply(self, state: PoemState, args: str) -> None:
        state.emit("")
        state.log("pause")


class Shift(Primitive):
    name = "shift"
    help_text = "shift vowel|upper|lower|swapcase"

    def apply(self, state: PoemState, args: str) -> None:
        mode = args.strip().lower()
        if mode == "vowel":
            state.current_text = state.current_text.translate(VOWEL_SHIFT)
        elif mode == "upper":
            state.current_text = state.current_text.upper()
        elif mode == "lower":
            state.current_text = state.current_text.lower()
        elif mode == "swapcase":
            state.current_text = state.current_text.swapcase()
        else:
            raise ValueError(f"unknown shift mode: {mode}")
        state.emit(state.current_text)
        state.log(f"shift -> {mode}")


class Erase(Primitive):
    name = "erase"
    help_text = "erase every Nth word"

    def apply(self, state: PoemState, args: str) -> None:
        match = re.fullmatch(r"every\s+(\d+)(?:st|nd|rd|th)?\s+word", args.strip())
        if not match:
            raise ValueError(f"unsupported erase pattern: {args}")
        interval = int(match.group(1))
        words = state.current_text.split()
        kept = [word for index, word in enumerate(words, start=1) if index % interval != 0]
        state.current_text = " ".join(kept)
        state.emit(state.current_text)
        state.log(f"erase -> every {interval}th word")


class Echo(Primitive):
    name = "echo"
    help_text = 'echo "from" -> "to"'

    def apply(self, state: PoemState, args: str) -> None:
        parts = re.fullmatch(r'"(.*)"\s*->\s*"(.*)"', args.strip())
        if not parts:
            raise ValueError(f"unsupported echo pattern: {args}")
        source, target = parts.group(1), parts.group(2)
        state.current_text = state.current_text.replace(source, target)
        state.emit(state.current_text)
        state.log(f'echo -> "{source}" to "{target}"')


class Address(Primitive):
    name = "address"
    help_text = 'address "target"'

    def apply(self, state: PoemState, args: str) -> None:
        target = parse_quoted_text(args)
        state.current_text = f"to {target}: {state.current_text}"
        state.emit(state.current_text)
        state.log(f'address -> "{target}"')


def parse_quoted_text(args: str) -> str:
    tokens = shlex.split(args)
    if len(tokens) != 1:
        raise ValueError(f"expected one quoted string, got: {args}")
    return tokens[0]


def builtins() -> Dict[str, Primitive]:
    return {
        primitive.name: primitive
        for primitive in [Seed(), Repeat(), Pause(), Shift(), Erase(), Echo(), Address()]
    }


def load_plugins() -> Dict[str, Primitive]:
    registry: Dict[str, Primitive] = {}
    package = importlib.import_module("src.plugins")
    for module_info in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"src.plugins.{module_info.name}")
        register = getattr(module, "register", None)
        if register is None:
            continue
        primitive = register()
        registry[primitive.name] = primitive
    return registry


def parse_program(text: str) -> List[tuple[str, str]]:
    commands: List[tuple[str, str]] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        name = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        commands.append((name, args))
    return commands


def run_program(text: str, include_trace: bool = False) -> PoemState:
    registry = builtins()
    registry.update(load_plugins())
    state = PoemState()
    for name, args in parse_program(text):
        primitive = registry.get(name)
        if primitive is None:
            raise ValueError(f"unknown primitive: {name}")
        primitive.apply(state, args)
    return state


def render_trace(state: PoemState) -> str:
    return "\n".join(f"- {entry}" for entry in state.trace)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run a minimal poetry program.")
    parser.add_argument("path", nargs="?", help="Path to a .poem file")
    parser.add_argument("--trace", action="store_true", help="Print the execution trace")
    parser.add_argument(
        "--list-primitives",
        action="store_true",
        help="List built-in and plugin primitives",
    )
    args = parser.parse_args(argv)

    registry = builtins()
    registry.update(load_plugins())

    if args.list_primitives:
        for name in sorted(registry):
            print(f"{name}: {registry[name].help_text}")
        return 0

    if not args.path:
        parser.error("path is required unless --list-primitives is used")

    text = Path(args.path).read_text()
    state = run_program(text, include_trace=args.trace)
    print("\n".join(state.output))
    if args.trace:
        print("\nTRACE")
        print(render_trace(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
