package qynl.agent;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;

/** Deterministic Minecraft-side companion loop. */
public final class AutonomousBrain {
    private ServerPlayerEntity companion;
    private ServerPlayerEntity owner;
    private String goal = "idle";
    private long nextTick;

    public void attach(ServerPlayerEntity companion, ServerPlayerEntity owner) { this.companion=companion; this.owner=owner; }
    public void setGoal(String goal) { this.goal=goal == null ? "idle" : goal; }

    public void tick(MinecraftServer server) {
        if (companion == null || companion.isRemoved() || owner == null || owner.isRemoved()) return;
        long now=server.getOverworld().getTime();
        if (now < nextTick) return;
        nextTick=now+2;
        if ("follow".equals(goal) || "come_here".equals(goal)) follow();
        else if ("stay".equals(goal) || "stop".equals(goal)) stop();
    }

    private void follow() {
        double d=companion.squaredDistanceTo(owner);
        if (d > 144) {
            companion.teleport((ServerWorld)owner.getWorld(), owner.getX(), owner.getY(), owner.getZ(), owner.getYaw(), owner.getPitch());
            return;
        }
        if (d > 16) {
            double dx=owner.getX()-companion.getX(), dz=owner.getZ()-companion.getZ();
            double len=Math.sqrt(dx*dx+dz*dz);
            if (len > 0.001) companion.setVelocity(dx/len*0.22, companion.getVelocity().y, dz/len*0.22);
        } else stop();
    }
    private void stop() { companion.setVelocity(0, companion.getVelocity().y, 0); }
}
