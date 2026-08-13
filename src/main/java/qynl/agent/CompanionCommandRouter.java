package qynl.agent;

import net.minecraft.server.command.ServerCommandSource;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;
import static net.minecraft.server.command.CommandManager.literal;

/** Safe, explicit Minecraft-side commands for the companion. */
public final class CompanionCommandRouter {
    private CompanionCommandRouter() {}
    public static void register(net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback dispatcher) {
        dispatcher.register((commandDispatcher, registryAccess, environment) -> commandDispatcher.register(
            literal("qynl").then(literal("follow").executes(c -> set(c.getSource(), "follow")))
                .then(literal("stay").executes(c -> set(c.getSource(), "stay")))
                .then(literal("stop").executes(c -> set(c.getSource(), "stop")))
        ));
    }
    private static int set(ServerCommandSource source, String goal) {
        ServerPlayerEntity p=source.getPlayer();
        if (p != null) p.sendMessage(Text.literal("[Qynl] goal="+goal), false);
        return 1;
    }
}
