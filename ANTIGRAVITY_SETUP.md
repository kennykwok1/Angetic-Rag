# Opencode Antigravity Auth Plugin Setup

## Installation Complete

The `opencode-antigravity-auth@beta` plugin has been installed and configured with full model definitions.

**Configuration file:** `~/.config/opencode/opencode.json`

## Authentication Required

To use the Antigravity models, you need to authenticate with Google OAuth:

### Step-by-Step Authentication

1. **Run the authentication command:**
   ```bash
   opencode auth login
   ```

2. **Select Google as provider:**
   - Use the **down arrow key** 4 times to move from "OpenCode Zen (recommended)" to "Google"
   - Press **Enter** to confirm selection

3. **Complete browser OAuth flow:**
   - A browser window will open for Google authentication
   - Login with your Google account
   - Grant necessary permissions to the Opencode application

4. **Return to terminal:**
   - After successful authentication, return to your terminal
   - The plugin will save credentials to `~/.config/opencode/antigravity-accounts.json`

## Testing the Setup

After authentication, test with:

```bash
opencode run "Hello, test the Antigravity plugin" --model=google/antigravity-claude-sonnet-4-5-thinking --variant=max
```

## Available Models

Configured models include:

### Antigravity Quota (with Variants)
- `google/antigravity-gemini-3-pro` (low, high thinking levels)
- `google/antigravity-gemini-3-flash` (minimal, low, medium, high)
- `google/antigravity-claude-sonnet-4-5` (no thinking)
- `google/antigravity-claude-sonnet-4-5-thinking` (low, max thinking budgets)
- `google/antigravity-claude-opus-4-5-thinking` (low, max thinking budgets)

### Gemini CLI Quota
- `google/gemini-2.5-flash`
- `google/gemini-2.5-pro`
- `google/gemini-3-flash-preview`
- `google/gemini-3-pro-preview`

## Multi-Account Support

To add multiple Google accounts for higher quotas:

```bash
opencode auth login
```

When prompted, select "Add new account(s)" to add additional accounts.

## Troubleshooting

### Safari OAuth Issues
If using Safari on macOS, you may need to:
- Use Chrome/Firefox instead, or
- Temporarily disable Safari's "HTTPS-Only Mode"

### Port Already in Use
If OAuth fails with port binding errors:
```bash
lsof -i :8080  # Check what's using port 8080
kill -9 <PID>  # Terminate the process
```

### Model Not Found Error
If models don't appear in `opencode models`, verify the config file is valid JSON.

## Plugin Settings

Default settings are used. To customize, create `~/.config/opencode/antigravity.json` with options from the plugin README.

## Verification

Check installed models:
```bash
opencode models | grep google
```