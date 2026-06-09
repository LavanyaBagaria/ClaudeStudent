import io
import unittest
from unittest import mock

import claude_student


class ClaudeStudentTests(unittest.TestCase):
    def _run_main(self, argv, call_side_effect=None):
        stderr = io.StringIO()
        with mock.patch("sys.argv", argv):
            with mock.patch("sys.stderr", stderr):
                if call_side_effect is None:
                    rc = claude_student.main()
                else:
                    with mock.patch("claude_student.call_claude", side_effect=call_side_effect):
                        rc = claude_student.main()
        return rc, stderr.getvalue()

    def test_main_rejects_non_positive_max_tokens(self):
        rc, stderr = self._run_main(["claude_student.py", "hello", "--max-tokens", "0"])
        self.assertEqual(rc, 2)
        self.assertIn("--max-tokens must be a positive integer.", stderr)

    def test_main_surfaces_runtime_error(self):
        rc, stderr = self._run_main(["claude_student.py", "hello"], call_side_effect=RuntimeError("boom"))
        self.assertEqual(rc, 2)
        self.assertIn("boom", stderr)

    def test_call_claude_requires_api_key(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError) as exc:
                claude_student.call_claude("hello", 10, "model")

        self.assertIn("Missing ANTHROPIC_API_KEY", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
