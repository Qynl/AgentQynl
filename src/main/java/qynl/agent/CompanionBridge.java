package qynl.agent;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/** Local companion bridge and safe Minecraft-chat command gateway. */
public final class CompanionBridge {
    private final AtomicBoolean running = new AtomicBoolean(false);
    private MinecraftServer server;
    private String token;
    public void start(MinecraftServer server) { this.server=server; token=UUID.randomUUID().toString(); running.set(true); AgentQynlMod.LOGGER.info("Qynl autonomous companion ready"); }
    public void stop() { running.set(false); server=null; token=null; }
    public boolean isRunning() { return running.get(); }
    public void onPlayerJoin(ServerPlayerEntity player) { if(running.get()) player.sendMessage(Text.literal("[Qynl] I'm online. Use /qynl spawn or @qynl follow me."),false); }
    public void onPlayerLeave(ServerPlayerEntity player) { }

    public void onChat(ServerPlayerEntity player, String text) {
        if(!running.get() || !text.startsWith("@qynl ")) return;
        String command=text.substring(6).trim().toLowerCase();
        if(command.equals("spawn") || command.equals("come here") || command.equals("come_here")) CompanionManager.goal("come_here",player);
        else if(command.equals("follow") || command.equals("follow me")) CompanionManager.goal("follow",player);
        else if(command.equals("stay") || command.equals("stay here")) CompanionManager.goal("stay",player);
        else if(command.equals("stop")) CompanionManager.goal("stop",player);
        else player.sendMessage(Text.literal("[Qynl] I understand: follow, stay, come here, stop, spawn. Full Ollama task planning can extend this safely."),false);
    }
    public String sessionToken() { return token; }
}
