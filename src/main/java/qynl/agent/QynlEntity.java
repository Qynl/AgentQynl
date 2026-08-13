package qynl.agent;

import net.minecraft.entity.EntityType;
import net.minecraft.entity.ai.pathing.PathNavigation;
import net.minecraft.entity.mob.PathAwareEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.Hand;
import net.minecraft.util.ActionResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraft.inventory.SimpleInventory;
import java.util.UUID;

/** A real server-side autonomous companion entity. */
public final class QynlEntity extends PathAwareEntity {
    private UUID ownerUuid;
    private String goal = "idle";
    private final SimpleInventory inventory = new SimpleInventory(9);
    private long nextBrainTick;

    public QynlEntity(EntityType<? extends QynlEntity> type, World world) { super(type, world); setPersistent(); }
    public void setOwner(ServerPlayerEntity player) { ownerUuid=player.getUuid(); }
    public UUID getOwnerUuid() { return ownerUuid; }
    public void setGoal(String goal) { this.goal=goal == null ? "idle" : goal; }
    public String getGoal() { return goal; }
    public SimpleInventory inventory() { return inventory; }

    @Override public void tick() {
        super.tick();
        if (getWorld().isClient || !(getWorld() instanceof ServerWorld world)) return;
        long t=world.getTime();
        if (t < nextBrainTick) return;
        nextBrainTick=t+2;
        ServerPlayerEntity owner = ownerUuid == null ? null : world.getServer().getPlayerManager().getPlayer(ownerUuid);
        if (owner == null) return;
        switch (goal) {
            case "follow", "come_here" -> follow(owner);
            case "stay", "stop", "idle" -> getNavigation().stop();
            default -> {
                if (getNavigation().isIdle() && squaredDistanceTo(owner) > 64) follow(owner);
            }
        }
    }

    private void follow(PlayerEntity owner) {
        double d=squaredDistanceTo(owner);
        if (d > 225) {
            teleport(owner.getX(), owner.getY(), owner.getZ());
            getNavigation().stop();
            return;
        }
        if (d > 12) getNavigation().startMovingTo(owner, 1.15D);
        else getNavigation().stop();
        getLookControl().lookAt(owner, 30.0F, 30.0F);
    }

    @Override protected ActionResult interactMob(PlayerEntity player, Hand hand) {
        if (!getWorld().isClient && player instanceof ServerPlayerEntity sp && ownerUuid == null) {
            setOwner(sp);
            sp.sendMessage(net.minecraft.text.Text.literal("[Qynl] You are now my owner."), false);
            return ActionResult.SUCCESS;
        }
        return ActionResult.PASS;
    }
}
