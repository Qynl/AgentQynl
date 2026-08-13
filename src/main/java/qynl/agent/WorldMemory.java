package qynl.agent;

import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public final class WorldMemory {
    private final Path file;
    private final Map<String,String> facts = new LinkedHashMap<>();
    public WorldMemory(Path worldRoot) { file=worldRoot.resolve("qynl_memory.properties"); load(); }
    public synchronized void put(String key,String value){ facts.put(key,value); save(); }
    public synchronized String get(String key){ return facts.get(key); }
    public synchronized Map<String,String> snapshot(){ return Map.copyOf(facts); }
    private void load(){ if(!Files.exists(file))return; try{ for(String line:Files.readAllLines(file)){int i=line.indexOf('=');if(i>0)facts.put(line.substring(0,i),line.substring(i+1));} }catch(IOException ignored){} }
    private void save(){ try{ List<String> out=new ArrayList<>();facts.forEach((k,v)->out.add(k+"="+v.replace("\n"," ")));Files.write(file,out,StandardOpenOption.CREATE,StandardOpenOption.TRUNCATE_EXISTING); }catch(IOException ignored){} }
}
