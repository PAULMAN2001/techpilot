# TechPilot Security Model

## Phase 1 Security

- Diagnostics are **read-only**
- The API does **not** accept shell commands
- CORS is limited to the local Vite development server
- Secrets and AI credentials are **not required**
- No automatic system modifications

## Future Phases

Future actions must:

1. Be explicitly registered in an allowlist
2. Be classified by risk level (READ_ONLY, SAFE, CONFIRMATION_REQUIRED, HIGH_RISK, BLOCKED)
3. Require user confirmation before execution
4. Be logged with timestamps and results
5. Include rollback information where possible
6. Never be auto-executed by the AI

## Privacy Principles

- Minimize collected data
- Prefer local processing
- Transparent external API calls
- User control over stored incidents
- No credential storage
