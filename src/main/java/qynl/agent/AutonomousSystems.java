package qynl.agent;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.entity.mob.HostileEntity;
import net.minecraft.entity.ItemEntity;
import net.minecraft.item.*;
import net.minecraft.block.Blocks;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Box;
import net.minecraft.text.Text;
import java.util.*;

public final class AutonomousSystems {
 private final QynlConfig cfg=new QynlConfig(); private final OllamaBrain ai=new OllamaBrain(cfg); private WorldMemory memory; private long nextThink; private String goal="idle";
 public void start(ServerWorld w){memory=new WorldMemory(w.getServer().getSavePath(net.minecraft.util.WorldSavePath.ROOT));}
 public void goal(String g){goal=g==null?"idle":g.toLowerCase();}
 public String goal(){return goal;}
 public void tick(MinecraftServer s,QynlEntity q,ServerPlayerEntity owner){
  if(q==null||owner==null||q.isRemoved())return; ServerWorld w=(ServerWorld)q.getWorld();
  if(memory==null)start(w); long t=w.getTime();
  if(t>=nextThink){nextThink=t+cfg.thinkEveryTicks; if(cfg.ollama && !goal.equals("idle")){String action=ai.think(state(q,owner),goal); if(action.length()<40)goal=action;}}
  act(w,q,owner);
 }
 private String state(QynlEntity q,ServerPlayerEntity p){return "player="+p.getBlockPos()+" companion="+q.getBlockPos()+" health="+q.getHealth()+" goal="+goal+" inv="+inventory(q);}
 private String inventory(QynlEntity q){StringBuilder b=new StringBuilder();for(int i=0;i<q.inventory().size();i++){ItemStack st=q.inventory().getStack(i);if(!st.isEmpty())b.append(st.getItem()).append('x').append(st.getCount()).append(',');}return b.toString();}
 private void act(ServerWorld w,QynlEntity q,ServerPlayerEntity p){
  switch(goal){
   case "follow","come_here"->follow(q,p);
   case "gather_wood"->gatherBlock(w,q,Blocks.OAK_LOG);
   case "gather_stone","mine"->gatherBlock(w,q,Blocks.STONE);
   case "eat"->eat(q);
   case "attack"->combat(w,q);
   case "explore"->explore(q);
   case "craft"->craft(q);
   case "build"->build(w,q,p);
   case "return"->q.getNavigation().startMovingTo(p,1.2);
   default->q.getNavigation().stop();
  }
 }
 private void follow(QynlEntity q,ServerPlayerEntity p){double d=q.squaredDistanceTo(p);if(d>400){q.teleport(p.getX(),p.getY(),p.getZ());q.getNavigation().stop();}else if(d>20)q.getNavigation().startMovingTo(p,1.15);else q.getNavigation().stop();q.getLookControl().lookAt(p,30,30);}
 private void gatherBlock(ServerWorld w,QynlEntity q,net.minecraft.block.Block target){BlockPos best=null;double bd=Double.MAX_VALUE;BlockPos c=q.getBlockPos();for(BlockPos pos:BlockPos.iterateOutwards(c,cfg.searchRadius,cfg.searchRadius,cfg.searchRadius)){if(w.getBlockState(pos).isOf(target)){double d=pos.getSquaredDistance(q.getPos());if(d<bd){bd=d;best=pos;}}}if(best==null){explore(q);return;}if(bd>6){q.getNavigation().startMovingTo(best.getX()+.5,best.getY(),best.getZ()+.5,1.15);}else if(w.breakBlock(best,true,q))memory.put("last_"+target.getName().getString(),best.toShortString());}
 private void eat(QynlEntity q){if(q.getHealth()>=q.getMaxHealth()-1)return;for(int i=0;i<q.inventory().size();i++){ItemStack s=q.inventory().getStack(i);if(s.getItem().isFood()){s.decrement(1);q.heal(4);return;}}}
 private void combat(ServerWorld w,QynlEntity q){List<HostileEntity> mobs=w.getEntitiesByClass(HostileEntity.class,new Box(q.getBlockPos()).expand(10),e->e.isAlive());if(mobs.isEmpty()){goal="explore";return;}HostileEntity m=mobs.get(0);q.getNavigation().startMovingTo(m,1.2);if(q.squaredDistanceTo(m)<4)m.damage(w.getDamageSources().mobAttack(q),4);}
 private void explore(QynlEntity q){long seed=q.getWorld().getRandom().nextLong();double a=(seed%6283)/1000.0;double r=8+(Math.abs(seed)%12);q.getNavigation().startMovingTo(q.getX()+Math.cos(a)*r,q.getY(),q.getZ()+Math.sin(a)*r,1.0);}
 private void craft(QynlEntity q){for(int i=0;i<q.inventory().size();i++){ItemStack s=q.inventory().getStack(i);if(s.isOf(Items.OAK_LOG)){int n=s.getCount()/4;if(n>0){s.decrement(n*4);q.inventory().addStack(new ItemStack(Items.OAK_PLANKS,n*4));return;}}}for(int i=0;i<q.inventory().size();i++){ItemStack s=q.inventory().getStack(i);if(s.isOf(Items.OAK_PLANKS)&&s.getCount()>=2){int n=s.getCount()/2;s.decrement(n*2);q.inventory().addStack(new ItemStack(Items.STICK,n*4));return;}}}
 private void build(ServerWorld w,QynlEntity q,ServerPlayerEntity p){ItemStack block=findBlock(q);if(block.isEmpty()){goal="gather_wood";return;}BlockPos pos=p.getBlockPos().up();if(w.getBlockState(pos).isAir()){w.setBlockState(pos,((BlockItem)block.getItem()).getBlock().getDefaultState());block.decrement(1);}}
 private ItemStack findBlock(QynlEntity q){for(int i=0;i<q.inventory().size();i++){ItemStack s=q.inventory().getStack(i);if(s.getItem() instanceof BlockItem)return s;}return ItemStack.EMPTY;}
 public String status(QynlEntity q){return "goal="+goal+" pos="+q.getBlockPos()+" hp="+q.getHealth()+" inv="+inventory(q);}
}
