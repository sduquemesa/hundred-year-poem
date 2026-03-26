# Presentation

## Five-Minute Script

I want to start with the workshop question: what would a computational poem need in order to last 100 years?

Our answer is that what lasts is not full context, not perfect interpretation, and not one preserved machine. What lasts is recoverable pattern.

So the claim behind this project is:

Poetry is a compact system for changing attention, expectation, and feeling through patterned language.

That definition lets us connect poetry and code without collapsing one into the other. Code already contains poetic devices. Loops can act like refrain. Conditionals create tension. Recursion can feel obsessive. Comments introduce a second voice. Variable names can work like metaphor.

From there, the move is simple: if code already contains poetic devices, we can extract some of those actions into a minimal poetry language.

The language we built is intentionally small. Each line is one action. It is readable as plain text, executable by a machine, and still interpretable if the exact runtime disappears.

It borrows from programming languages, but differently. There is no heavy control flow, no deep nesting, and no block structure in this MVP. That is deliberate. Flat structure makes the poem easier to read, perform, and reconstruct later. Instead of building a general-purpose language, we kept a stable grammar and let the vocabulary grow through small primitives like `seed`, `repeat`, `pause`, `shift`, `erase`, `echo`, and `address`.

So in this project, the poem is also a protocol. It tells a machine what to do, but it also tells a future reader how to re-perform the work even if the original runtime is gone.

## Demo

Show this poem and read it once as code:

```txt
seed "river remembers the route"
repeat 2
pause
shift vowel
erase every 4th word
echo "river" -> "route"
address "future reader"
```

Then read it again as a score:

- introduce a phrase
- restate it
- make a pause
- mutate the sound
- remove part of it
- let one word resonate into another
- send it toward someone not yet here

Then run the interpreter and show that the execution trace is just another reading of the poem.

## Live Room Demo

If there is time, do a second poem with the room.

Ask the room for:

- one seed phrase
- one repetition count
- one transformation primitive
- one destination for `address`

Then write a four-line poem live and run it immediately.

A safe room-friendly template is:

```txt
seed "<phrase from the room>"
repeat 2
shift upper
address "<target from the room>"
```

If you want a slightly richer version:

```txt
seed "<phrase from the room>"
repeat 1
pause
echo "<word a>" -> "<word b>"
address "<target from the room>"
```

The point of the demo is not complexity. The point is that the room can see poetry become both instruction and performance.

## Closing

The poem lasts not because we preserve one machine forever, but because we preserve a pattern that can be re-read, re-built, and re-performed.

So the final question is larger than this interpreter.

If poetry is not only a human art, but a patterned way of shaping attention across a channel, how would we define poetry when the communicating parties are not human?

What does poetry look like when a human and a compiler are communicating?

What does poetry look like when both parties are machines?

That question lets the project end where it began: not with a finished definition, but with a protocol that can be tested across different kinds of minds.
