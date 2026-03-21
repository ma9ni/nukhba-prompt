# AGENTS.md — NukhbaPrompt

## 🧠 Mission

NukhbaPrompt is a Chrome extension designed to transform weak or unclear prompts into high-quality, structured prompts for AI tools like ChatGPT and Claude.

The goal is simple:
help users get better AI responses without needing to learn prompt engineering.

---

## 🏗️ System Architecture

The system is composed of three main agents:

### 1. Content Agent (content.js)
Responsible for:
- detecting prompt input fields in web pages
- injecting the "Optimize" button or icon
- reading the current prompt
- replacing the prompt with the optimized version

Supported targets:
- ChatGPT
- Claude

---

### 2. Background Agent (background.js)
Responsible for:
- handling communication between UI and API
- calling OpenRouter
- managing configuration (API key, model, system prompt)
- returning optimized prompt results

---

### 3. Enhancement Agent (services layer)

#### prompt-optimizer.js
- builds the messages sent to the model
- applies system prompt rules
- ensures output is clean (no explanations, no formatting noise)

#### openrouter-provider.js
- handles HTTP calls to OpenRouter
- injects API key and model dynamically
- supports configurable models
- handles errors and fallback

---

## ⚙️ Enhancement Strategy

Each prompt is transformed using:

- clarity improvements
- structure (steps, constraints)
- specificity
- expert framing

Example:

User Input:
"explain docker"

Optimized Prompt:
"You are a DevOps expert. Explain Docker using a simple analogy, then provide a technical breakdown, followed by real-world use cases."

---

## 🔐 Security Constraints

- API key stored in chrome.storage.local (MVP only)
- no hardcoded secrets
- OpenRouter calls handled in background script
- future version should use backend proxy

---

## 🧩 Future Agents

### Memory Agent
- store prompt history
- save user preferences

### Context Agent
- detect site (ChatGPT, Claude)
- adapt prompt style dynamically

### AI Agent (advanced)
- multi-model routing
- prompt comparison
- cost optimization

---

## 🎯 Design Principles

- minimal friction
- one-click optimization
- predictable output
- no unnecessary UI
- clean separation of concerns

---

## 🚀 MVP Scope

- inject inline button near prompt field
- read prompt from page
- send to OpenRouter
- receive optimized prompt
- replace original prompt
- simple options page for configuration

---

## 🧪 Testing Strategy

Test on:
- ChatGPT
- Claude

Validate:
- button injection
- prompt detection
- API call success
- correct replacement
- error handling

---

## 📈 Long-Term Vision

NukhbaPrompt becomes a universal layer between humans and AI.

It evolves into:
- a prompt optimization engine
- a personal AI interaction assistant
- a productivity multiplier for professionals

---

## 🏷️ Branding

Name: NukhbaPrompt

Meaning:
- "Nukhba" = elite, refined, high-quality

The product must reflect:
- precision
- clarity
- professionalism