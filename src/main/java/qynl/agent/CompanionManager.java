package qynl.agent;
import net.minecraft.entity.EntityType;import net.minecraft.entity.SpawnGroup;import net.minecraft.registry.Registries;import net.minecraft.registry.Registry;import net.minecraft.server.MinecraftServer;import net.minecraft.server.network.ServerPlayerEntity;import net.minecraft.server.world.ServerWorld;import net.minecraft.util.Identifier;
public final class CompanionManager{
 public static final EntityType<QynlEntity> QYNL=Registry.register(Registries.ENTITY_TYPE,Identifier.of(AgentQynlMod.MOD_ID,"qynl"),EntityType.Builder.create(QynlEntity::new,SpawnGroup.CREATURE).dimensions(.6f,1.8f).build());
 private static QynlEntity active;private CompanionManager(){}
 public static void spawn(MinecraftServer s,ServerPlayerEntity owner){ServerWorld w=owner.getServerWorld();if(active!=null&&!active.isRemoved())active.discard();active=new QynlEntity(QYNL,w);active.refreshPositionAndAngles(owner.getX()+1,owner.getY(),owner.getZ()+1,owner.getYaw(),0);active.setOwner(owner);active.setGoal("follow");w.spawnEntity(active);owner.sendMessage(net.minecraft.text.Text.literal("[Qynl] Companion joined your world."),false);}
 public static QynlEntity get(){return active;}public static void goal(String g,ServerPlayerEntity owner){if(active==null||active.isRemoved())spawn(owner.getServer(),owner);if(active!=null){active.setOwner(owner);active.setGoal(g);owner.sendMessage(net.minecraft.text.Text.literal("[Qynl] "+g),false);}}
 public static void tickAutonomy(MinecraftServer s,String goal){if(active==null||active.isRemoved())return;ServerPlayerEntity o=active.getOwner();if(o==null)return;active.setGoal(goal);active.tick();}
}
