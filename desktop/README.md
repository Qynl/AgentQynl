# Qynl BedWars Desktop

Native Tauri wrapper around the React/TSX Qynl training control center.

## Development

1. Install Node.js and Rust/Tauri prerequisites.
2. From `desktop/`, install dependencies with your package manager.
3. Run the frontend in development mode.
4. Run the Tauri development command to open the native window.
5. The private training client must expose the loopback IPC endpoint on `127.0.0.1:18791`.

## Production

Build the frontend first, then run the Tauri build command to produce the platform-specific application bundle.

The app is intentionally scoped to private training environments. It does not implement public-server automation or anti-cheat bypassing.
