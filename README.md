# ClaudeStudent

A tiny starter project for sending prompts to Claude.

## Quick start

1. Export your Anthropic API key:
   ```bash
   export ANTHROPIC_API_KEY="your_key_here"
   ```
2. Run the script:
   ```bash
   python3 claude_student.py "Explain recursion in one sentence"
   ```

### Optional settings

- `CLAUDE_MODEL` (default: `claude-3-5-sonnet-latest`)
- `--max-tokens` (default: `512`)
