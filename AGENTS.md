# AGENTS

This file defines the design contract for extending this poetry system.

## Purpose

This language is a durable poetry protocol between human and machine.

Programs in this language should be:

- Readable as plain text
- Executable by a small interpreter
- Interpretable even under partial understanding

## Invariants

- Keep the syntax line-oriented and minimal.
- Each primitive should name an observable poetic action.
- Favor plain words like `repeat`, `pause`, and `erase` over technical jargon.
- New primitives should transform attention, rhythm, pattern, or address.
- A poem should still make sense if someone reads it without running it.

## Primitive Contract

Each primitive must provide:

- A `name`
- A `help_text`
- An `apply(state, args)` method

The `apply` method receives and returns the poem state. It may mutate the state in place.

## How To Add A Primitive

1. Choose a short verb-like name.
2. Define its semantics in one sentence.
3. Implement the primitive in `src/plugins/` or in the built-in registry.
4. Add one example poem that uses it.
5. Add at least one test covering its behavior.

## Avoid

- Parser changes unless they are strictly necessary
- Hidden semantics that only exist in prompts or documentation
- Generic programming features that push the language toward a full language runtime
- Primitives that require network access or external services

## Durability Standard

If the runtime disappeared, a human should still be able to reconstruct the likely action of the primitive from its name and one example.
