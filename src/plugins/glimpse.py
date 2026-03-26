from src.main import Primitive, PoemState


class Glimpse(Primitive):
    name = "glimpse"
    help_text = "glimpse N"

    def apply(self, state: PoemState, args: str) -> None:
        count = max(1, int(args.strip()))
        words = state.current_text.split()
        snippet = " ".join(words[:count])
        state.emit(snippet)
        state.log(f"glimpse -> {count}")


def register() -> Primitive:
    return Glimpse()
