# Solana Arbitrage Scanner - AI Review Hub

This repo coordinates multiple AI systems reviewing the same codebase to catch bugs, verify logic, and suggest improvements.

## Structure

```
shared/           # Context and code for all AIs to review
├── context.md    # Project overview
├── code/         # Current scanner code snapshot
└── data/         # Sample JSON outputs

gemini/           # Google Gemini prompts & reports
chatgpt/          # OpenAI ChatGPT prompts & reports  
xai/              # xAI Grok prompts & reports

comparison/       # Side-by-side analysis of findings
```

## Workflow

1. Copy latest code to `shared/code/`
2. Run prompts through each AI
3. Save responses to `{ai}/reports/`
4. Compare findings in `comparison/`

## Review Types

- **Code Review**: Bugs, edge cases, error handling
- **Logic Analysis**: Math verification, arbitrage calculations
- **Optimization**: Performance, efficiency improvements
- **Feature Ideas**: Missing opportunities, enhancements

## Scanner Repo

Main project: https://github.com/Silverstacker/solana-arbitrage-scanner
