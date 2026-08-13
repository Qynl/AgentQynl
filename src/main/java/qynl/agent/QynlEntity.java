package qynl.agent;
import net.minecraft.entity.EntityType;import net.minecraft.entity.ai.pathing.PathAwareEntity;import net.minecraft.entity.player.PlayerEntity;import net.minecraft.server.network.ServerPlayerEntity;import net.minecraft.server.world.ServerWorld;import net.minecraft.world.World;import net.minecraft.inventory.SimpleInventory;import net.minecraft.item.ItemStack;import net.minecraft.util.Hand;import net.minecraft.util.ActionResult;import net.minecraft.text.Text;import java.util.UUID;
public final class QynlEntity extends PathAwareEntity{
 private UUID ownerUuid;private String goal="idle";private final SimpleInventory inventory=new SimpleInventory(27);private final AutonomousSystems systems=new AutonomousSystems();
 public QynlEntity(EntityType<? extends QynlEntity> type,World world){super(type,world);setPersistent();}
 public void setOwner(ServerPlayerEntity p){ownerUuid=p.getUuid();}
 public UUID getOwnerUuid(){return ownerUuid;}
 public SimpleInventory inventory(){return inventory;}
 public void setGoal(String g){goal=g==null?"idle":g;systems.goal(goal);}
 public String getGoal(){return goal;}
 @Override public void tick(){super.tick();if(getWorld().isClient||!(getWorld() instanceof ServerWorld w))return;ServerPlayerEntity owner=ownerUuid==null?null:w.getServer().getPlayerManager().getPlayer(ownerUuid);if(owner!=null)systems.tick(w.getServer(),this,owner);}
 @Override protected ActionResult interactMob(PlayerEntity p,Hand h){if(!getWorld().isClient&&p instanceof ServerPlayerEntity sp){if(ownerUuid==null){setOwner(sp);sp.sendMessage(Text.literal("[Qynl] Bound to you."),false);}else sp.sendMessage(Text.literal("[Qynl] "+systems.status(this)),false);return ActionResult.SUCCESS;}return ActionResult.PASS;}
}
