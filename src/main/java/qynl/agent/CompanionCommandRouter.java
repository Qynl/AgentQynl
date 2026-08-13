package qynl.agent;

import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.server.command.ServerCommandSource;
import net.minecraft.server.network.ServerPlayerEntity;
import static net.minecraft.server.command.CommandManager.literal;

/** Explicit, bounded commands for spawning and controlling the companion. */
public final class CompanionCommandRouter {
    private CompanionCommandRouter() {}
    public static void register() {
        CommandRegistrationCallback.EVENT.register((dispatcher, registryAccess, environment) -> dispatcher.register(
            literal("qynl")
                .then(literal("spawn").executes(c -> spawn(c.getSource())))
                .then(literal("follow").executes(c -> goal(c.getSource(), "follow")))
                .then(literal("stay").executes(c -> goal(c.getSource(), "stay")))
                .then(literal("stop").executes(c -> goal(c.getSource(), "stop")))
                .then(literal("come").executes(c -> goal(c.getSource(), "come_here")))
        ));
    }
    private static ServerPlayerEntity player(ServerCommandSource s) throws com.mojang.brigadier.exceptions.CommandSyntaxException { return s.getPlayerOrThrow(); }
    private static int spawn(ServerCommandSource s) throws com.mojang.brigadier.exceptions.CommandSyntaxException { ServerPlayerEntity p=player(s); CompanionManager.spawn(s.getServer(),p); return 1; }
    private static int goal(ServerCommandSource s,String g) throws com.mojang.brigadier.exceptions.CommandSyntaxException { ServerPlayerEntity p=player(s); CompanionManager.goal(g,p); return 1; }
}
