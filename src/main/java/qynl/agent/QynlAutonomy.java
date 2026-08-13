package qynl.agent;
import net.minecraft.server.MinecraftServer;import net.minecraft.server.network.ServerPlayerEntity;import net.minecraft.text.Text;import java.util.concurrent.*;
public final class QynlAutonomy{
 private final OllamaClient ollama=new OllamaClient("http://127.0.0.1:11434","llama3.2-vision:11b");private final ExecutorService ai=Executors.newSingleThreadExecutor();private volatile String goal="idle";private volatile long cooldown;
 public void chat(ServerPlayerEntity p,String text){if(!text.toLowerCase().contains("@qynl"))return;String q=text.replaceFirst("(?i)@qynl\\s*","").trim();if(q.isEmpty())return;if(q.matches("(?i)stop|halt")){goal="stop";p.sendMessage(Text.literal("[Qynl] Stopping."),false);return;}ai.submit(()->{String r=ollama.generate("You are a Minecraft co-op companion. Convert this request into one safe goal: follow, stay, gather, mine, craft, build, explore, guard, eat, return, stop, or idle. Request: "+q);goal=extractGoal(r);p.sendMessage(Text.literal("[Qynl] Goal: "+goal),false);});}
 public void tick(MinecraftServer s){if(s==null)return;long t=s.getOverworld().getTime();if(t<cooldown)return;cooldown=t+5;CompanionManager.tickAutonomy(s,goal);}
 private static String extractGoal(String s){if(s==null)return "idle";for(String g:new String[]{"follow","stay","gather","mine","craft","build","explore","guard","eat","return","stop"})if(s.toLowerCase().contains(g))return g;return "idle";}
 public void shutdown(){ai.shutdownNow();}
}
