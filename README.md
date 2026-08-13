# AgentQynl V3.8

Autonomous Minecraft co-op companion for Fabric 1.21.1.

## Build

Install Java 21, then run `gradlew build` (Windows) or `./gradlew build` (Linux/macOS). The jar is written to `build/libs/`.

## Use

Install the jar with Fabric API. Start Minecraft and use `/qynl spawn` or chat `@qynl spawn`.

Natural commands include `@qynl follow me`, `@qynl get wood`, `@qynl find stone`, `@qynl get food`, `@qynl fight`, `@qynl explore`, `@qynl craft`, `@qynl build`, `@qynl come here`, `@qynl stay`, and `@qynl stop`.

## Autonomous systems

Server-side navigation, resource gathering, mining, food recovery, combat, exploration, simple crafting, simple building, state extraction, Ollama action selection, persistent world memory, and bounded recovery are included. Ollama is optional: if it is offline, deterministic behaviors continue.

Default Ollama endpoint: `http://127.0.0.1:11434`. Default model: `llama3.2-vision:11b`.

Qynl never executes arbitrary model-generated Java, shell, or operating-system commands.
