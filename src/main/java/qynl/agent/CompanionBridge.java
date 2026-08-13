package qynl.agent;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/** Local companion bridge. Transport is intentionally loopback-only by default. */
public final class CompanionBridge {
    private final AtomicBoolean running = new AtomicBoolean(false);
    private MinecraftServer server;
    private String token;

    public void start(MinecraftServer server) {
        this.server = server;
        this.token = UUID.randomUUID().toString();
        running.set(true);
        AgentQynlMod.LOGGER.info("Companion bridge session initialized");
    }

    public void stop() { running.set(false); server = null; token = null; }
    public boolean isRunning() { return running.get(); }

    public void onPlayerJoin(ServerPlayerEntity player) {
        if (!running.get()) return;
        player.sendMessage(Text.literal("[Qynl] Companion bridge ready. Desktop runtime can connect locally."), false);
    }

    public void onPlayerLeave(ServerPlayerEntity player) { }

    public void onChat(ServerPlayerEntity player, String text) {
        if (!running.get()) return;
        if (text.startsWith("@qynl ")) {
            String command = text.substring(6).trim();
            player.sendMessage(Text.literal("[Qynl] Received: " + command), false);
        }
    }

    public String sessionToken() { return token; }
}
