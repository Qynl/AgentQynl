package qynl.agent;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.message.v1.ServerMessageEvents;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class AgentQynlMod implements ModInitializer {
    public static final String MOD_ID = "agentqynl";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);
    private static volatile MinecraftServer server;
    private static final CompanionBridge BRIDGE = new CompanionBridge();

    @Override public void onInitialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(s -> { server = s; BRIDGE.start(s); LOGGER.info("Qynl companion bridge ready on localhost"); });
        ServerLifecycleEvents.SERVER_STOPPING.register(s -> { BRIDGE.stop(); server = null; });
        ServerPlayConnectionEvents.JOIN.register((handler, sender, s) -> BRIDGE.onPlayerJoin(handler.getPlayer()));
        ServerPlayConnectionEvents.DISCONNECT.register((handler, s) -> BRIDGE.onPlayerLeave(handler.getPlayer()));
        ServerMessageEvents.CHAT_MESSAGE.register((message, player, params) -> BRIDGE.onChat(player, message.getContent().getString()));
    }

    public static MinecraftServer server() { return server; }
}
