# NukhbaPrompt Desktop Roadmap

## Product Direction

NukhbaPrompt Desktop should evolve from a clipboard utility into a cross-app personal AI assistant with memory, rules, context, and multiple action modes.

The long-term architecture should stay:

- local-first
- shortcut-first
- context-aware
- cloud-optional

## V1.1 - Daily Use Utility

Objective:
Make the product genuinely useful many times per day.

Features:

- Multi-shortcuts
  - `Ctrl+Shift+O` Optimize
  - `Ctrl+Shift+S` Summarize
  - `Ctrl+Shift+T` Translate
  - `Ctrl+Shift+R` Reply professionally
  - `Ctrl+Shift+G` Grammar fix
- Action modes
  - Optimize
  - Summarize
  - Translate
  - Reply
  - Grammar fix
- Selection-first flow
  - auto copy
  - clipboard fallback
  - auto paste
- Undo last optimization
- Clipboard history
- Preview before replace
- Startup on login
- App blacklist / whitelist
- Tone presets
- Length control

## V1.2 - Context and Rules

Objective:
Make the assistant act more like the user.

Features:

- Profile memory
  - role
  - domains
  - preferred language
  - writing preferences
- Rules engine
  - global rules
  - mode-specific rules
  - language-specific rules
- Additional context blocks
- Context packs
  - DevOps
  - freelance
  - client communication
  - email
- Saved snippets
- Prompt history and regeneration

## V1.3 - Local Memory

Objective:
Introduce useful persistent memory with retrieval.

Features:

- SQLite memory store
- tagged memory items
- local semantic retrieval
- auto-attach top relevant memories
- explain why context was attached
- memory controls
  - pin
  - archive
  - delete
  - disable

## V2 - Hybrid Memory with Supabase

Objective:
Add sync and cloud retrieval without losing local speed.

Recommended split:

- SQLite
  - runtime settings
  - shortcuts
  - local history
  - recent memory cache
  - undo stack
- Supabase
  - synced profiles
  - synced rules
  - long-term memories
  - vector embeddings with `pgvector`
  - cross-device sync

Recommended flow:

1. capture selected text
2. detect action mode
3. load local rules/profile from SQLite
4. query local memory cache
5. if cloud memory enabled, query Supabase vector memory
6. merge top relevant context
7. assemble final prompt
8. call LLM
9. write and paste result
10. save local history
11. sync selected memory back to Supabase

## Suggested Feature Clusters

### Daily Productivity

- Undo last change
- Clipboard history
- Preview mode
- Startup on login
- Smart retry on paste failure

### Writing Assistant

- Professional rewrite
- Concise rewrite
- Friendly rewrite
- Executive rewrite
- Translation
- Grammar fix
- Summarization

### Developer / DevOps Assistant

- Incident update rewrite
- RCA formatting
- Ticket generation
- Commit message cleanup
- Deployment note cleanup
- Log summary
- Meeting notes to action items

### Professional Communication

- Absence message rewrite
- Client-safe rewrite
- escalation rewrite
- email polish
- reply generation

## Suggested Local Tables

- `settings`
- `shortcuts`
- `profiles`
- `rules`
- `context_packs`
- `snippets`
- `prompt_history`
- `memory_items`
- `undo_stack`
- `app_preferences`

## Suggested Supabase Tables

- `users`
- `profiles`
- `rules`
- `context_packs`
- `memory_items`
- `memory_embeddings`
- `prompt_history`
- `devices`
- `sync_state`

## Best Next Execution Order

1. Multi-shortcuts plus action modes
2. Settings expansion for profile and rules
3. Undo and clipboard history
4. SQLite local memory
5. Vector retrieval
6. Supabase sync and `pgvector`
