# Hundred Year Poem

This project proposes a minimal poetry language designed to last.

The core claim is simple:

Poetry is a compact system for changing attention, expectation, and feeling through patterned language.

If a computational poem is going to last 100 years, it should not depend on one runtime, one machine, or one perfect interpretation. It should survive partial understanding. Its patterns should remain legible even when its original context is gone.

## Design

This language is intentionally:

- Plain-text
- Line-oriented
- Readable as a score by a human
- Executable as a program by a machine
- Extensible through small primitives

Each line is one action.

```txt
seed "river"
repeat 3
pause
shift vowel
erase every 4th word
echo "river" -> "route"
```

The default primitives are:

- `seed "text"`: set the current text and emit it
- `repeat n`: restate the current text `n` times
- `pause`: emit a blank beat
- `shift mode`: transform the current text
- `erase every Nth word`: remove words by interval
- `echo "a" -> "b"`: replace one phrase with another and emit the variation
- `address "target"`: direct the current line toward someone or something

The interpreter also loads plugin primitives from [`src/plugins`](./src/plugins).

## Comparison To Programming Languages

This language borrows some ideas from programming languages, but it uses them differently.

- Control flow: traditional languages use control flow to direct execution toward a computational result. This language uses simple sequencing to shape rhythm, repetition, mutation, and attention.
- Block structure: most languages use blocks to create scope, grouping, and hierarchy. This language currently avoids blocks on purpose so each line remains legible as both instruction and score.
- Nesting: nesting can express rich structure, but it also makes recovery harder. Here, flat composition is a durability feature.
- Context and state: programming languages often carry large hidden state across execution. This language keeps a very small visible state, mainly the current text and the emitted lines.
- Abstraction: general-purpose languages introduce functions, types, and reusable logic. This language prefers named poetic actions such as `repeat`, `pause`, and `echo`.
- Extensibility: instead of adding more syntax, new behavior enters through primitives. That keeps the grammar stable while allowing the vocabulary to grow.

In that sense, this is less a general programming language than a protocol for poetic transformation.

## Why This Could Last

- The syntax stays close to ordinary language.
- The operations are poetic verbs, not runtime internals.
- A future reader could still perform the poem by hand.
- Extensibility is isolated in primitives rather than parser complexity.

## Project Layout

- [`AGENTS.md`](/Users/sduquemesa/Projects/a-hundred-years-poetry/AGENTS.md): design contract for humans and agents
- [`PRESENTATION.md`](/Users/sduquemesa/Projects/a-hundred-years-poetry/PRESENTATION.md): short talk track
- [`examples/river.poem`](/Users/sduquemesa/Projects/a-hundred-years-poetry/examples/river.poem): minimal demo poem
- [`examples/compiler-and-human.poem`](/Users/sduquemesa/Projects/a-hundred-years-poetry/examples/compiler-and-human.poem): example with a plugin primitive
- [`src/main.py`](/Users/sduquemesa/Projects/a-hundred-years-poetry/src/main.py): parser, registry, runtime, and CLI

## Run

Run a poem:

```bash
python3 src/main.py examples/river.poem
```

Run with an execution trace:

```bash
python3 src/main.py examples/river.poem --trace
```

List built-in and plugin primitives:

```bash
python3 src/main.py --list-primitives
```

Run tests:

```bash
python3 -m unittest discover -s tests
```
