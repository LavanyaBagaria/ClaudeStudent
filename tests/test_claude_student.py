import io
import unittest
from unittest import mock

import claude_student


class ClaudeStudentTests(unittest.TestCase):
    def test_main_rejects_non_positive_max_tokens(self):
        stderr = io.StringIO()
        with mock.patch("sys.argv", ["claude_student.py", "hello", "--max-tokens", "0"]), mock.patch("sys.stderr", stderr):
            rc = claude_student.main()

        self.assertEqual(rc, 2)
        self.assertIn("--max-tokens must be a positive integer.", stderr.getvalue())

    def test_main_surfaces_runtime_error(self):
        stderr = io.StringIO()
        with mock.patch("sys.argv", ["claude_student.py", "hello"]), mock.patch("claude_student.call_claude", side_effect=RuntimeError("boom")), mock.patch("sys.stderr", stderr):
            rc = claude_student.main()

        self.assertEqual(rc, 2)
        self.assertIn("boom", stderr.getvalue())

    def test_call_claude_requires_api_key(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError) as exc:
                claude_student.call_claude("hello", 10, "model")

        self.assertIn("Missing ANTHROPIC_API_KEY", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
