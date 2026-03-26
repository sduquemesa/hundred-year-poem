import unittest

from src.main import load_plugins, run_program


class RuntimeTests(unittest.TestCase):
    def test_builtin_flow(self) -> None:
        program = "\n".join(
            [
                'seed "river remembers the route"',
                "repeat 1",
                "shift upper",
                'echo "RIVER" -> "ROUTE"',
                'address "reader"',
            ]
        )
        state = run_program(program)
        self.assertEqual(state.output[0], "river remembers the route")
        self.assertIn("ROUTE REMEMBERS THE ROUTE", state.output)
        self.assertEqual(state.output[-1], "to reader: ROUTE REMEMBERS THE ROUTE")

    def test_erase_every_nth_word(self) -> None:
        program = "\n".join(
            [
                'seed "one two three four five six"',
                "erase every 2nd word",
            ]
        )
        state = run_program(program)
        self.assertEqual(state.output[-1], "one three five")

    def test_plugin_is_loaded(self) -> None:
        plugins = load_plugins()
        self.assertIn("glimpse", plugins)
        program = "\n".join(
            [
                'seed "compiler meets a human in the dark"',
                "glimpse 3",
            ]
        )
        state = run_program(program)
        self.assertEqual(state.output[-1], "compiler meets a")


if __name__ == "__main__":
    unittest.main()
