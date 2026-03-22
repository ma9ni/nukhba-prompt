# AGENTS.md — nukhba-prompt-desktop

## Mission

`nukhba-prompt-desktop` is the desktop companion application for NukhbaPrompt.

Its goal is to allow prompt optimization outside the browser, especially in desktop applications where browser extensions cannot run.

Main workflow:
1. user copies text
2. user triggers a shortcut or clicks a UI action
3. the app reads clipboard content
4. the app sends the text to the AI provider
5. the optimized result is written back to the clipboard
6. the user pastes the optimized text anywhere

---

## Module Scope

This subproject is responsible for:
- desktop UI
- system tray integration
- global or app-level shortcut orchestration
- clipboard read/write
- local settings persistence
- AI provider integration
- user notifications
- packaging into executable form

This subproject is NOT responsible for:
- browser DOM injection
- extension APIs
- web content scripts

---

## Agent Definitions

### 1. Desktop UI Agent
**Role**
- manages windows, dialogs, forms, and user actions
- displays settings, status, and logs when appropriate

**Responsibilities**
- main window lifecycle
- settings screen
- action buttons
- status feedback
- tray menu interactions

**Input**
- user events
- app state changes

**Output**
- commands to orchestration layer
- visual feedback to user

---

### 2. App Orchestrator Agent
**Role**
- coordinates all application workflows

**Responsibilities**
- startup sequence
- shutdown sequence
- connect UI with services
- trigger optimization workflow
- debounce duplicate actions
- centralize high-level business flow

**Input**
- shortcut events
- tray actions
- button clicks
- startup hooks

**Output**
- calls to clipboard, provider, storage, and notification services

---

### 3. Clipboard Agent
**Role**
- handles clipboard reading and writing safely

**Responsibilities**
- read current clipboard text
- validate content
- write optimized content back
- reject unsupported or empty payloads

**Input**
- clipboard access requests

**Output**
- plain text content
- clipboard update result

---

### 4. Shortcut Agent
**Role**
- handles shortcut registration and trigger events

**Responsibilities**
- register default shortcut
- validate shortcut availability
- emit optimization event when triggered
- avoid repeated accidental triggers

**Input**
- shortcut configuration
- system/user key events

**Output**
- shortcut action events

---

### 5. AI Provider Agent
**Role**
- communicates with external AI provider such as OpenRouter

**Responsibilities**
- load API settings
- build request payload
- call provider API
- parse response
- return optimized text only
- handle network/provider errors

**Input**
- user text
- selected model
- system prompt

**Output**
- optimized text
- structured error object

---

### 6. Prompt Optimization Agent
**Role**
- encapsulates the logic of prompt enhancement

**Responsibilities**
- prepare system prompt + user message
- normalize provider output
- ensure result is only optimized text
- preserve user intent
- optionally support optimization modes later

**Input**
- source text
- optimization settings

**Output**
- provider-ready payload
- cleaned optimized text

---

### 7. Storage Agent
**Role**
- persists local settings and preferences

**Responsibilities**
- load/save settings
- manage defaults
- validate configuration values
- support future migration of config schema

**Input**
- settings updates
- app startup load request

**Output**
- typed config object

---

### 8. Notification Agent
**Role**
- informs the user about important events

**Responsibilities**
- success notification
- clipboard empty notification
- missing API key notification
- network failure notification
- optimization failure notification

**Input**
- status events from orchestrator

**Output**
- desktop notification, tray message, or status message

---

### 9. Logging Agent
**Role**
- record diagnostic information without polluting user UX

**Responsibilities**
- structured logs
- warning/error logs
- optional debug mode
- sanitized logs without secrets

---

## Available Commands / Workflows

### Startup
- load settings
- initialize UI
- initialize tray
- initialize services
- register shortcut
- enter event loop

### Optimize Clipboard Workflow
1. read clipboard text
2. validate text
3. load config
4. call optimization service
5. write optimized text back to clipboard
6. notify user

### Open Settings Workflow
- open settings view
- display current config
- save and validate changes

### Quit Workflow
- stop listeners cleanly
- close services
- exit app safely

---

## Suggested Internal Project Structure

- `src/nukhba_prompt_desktop/app/`
  - application bootstrap and orchestrator

- `src/nukhba_prompt_desktop/ui/`
  - windows, dialogs, tray, widgets

- `src/nukhba_prompt_desktop/services/`
  - clipboard, shortcut, provider, notification, storage

- `src/nukhba_prompt_desktop/domain/`
  - prompt optimization rules and models

- `src/nukhba_prompt_desktop/config/`
  - settings loading and defaults

- `src/nukhba_prompt_desktop/utils/`
  - logger, helpers

---

## Conventions for This Module

### Architecture
- prefer clear layering:
  - UI
  - application orchestration
  - domain logic
  - infrastructure/services

### Separation of Concerns
- UI must not call provider HTTP logic directly
- clipboard logic must stay isolated
- storage must not be mixed with widgets
- optimization logic must remain testable without GUI

### Config
- support:
  - API key
  - model name
  - system prompt
  - shortcut
  - notification preferences

### Error Handling
- show short user message
- log technical details
- never expose raw secret values

---

## Testing Expectations

### Unit Tests
- config validation
- optimization payload building
- response parsing
- clipboard validation helpers

### Integration/Manual Tests
- startup
- tray presence
- settings persistence
- shortcut trigger
- clipboard replacement
- provider error behavior

---

## Packaging Expectations

The module should support packaging into executable form.

Typical targets:
- Windows `.exe`
- macOS `.app`
- Linux binary/package

Packaging notes should be documented separately.

---

## Future Evolution

Possible future additions:
- history of optimized prompts
- multiple optimization modes
- compare before/after
- local cache
- backend sync
- enterprise policy controls