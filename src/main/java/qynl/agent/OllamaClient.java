package qynl.agent;
import java.net.URI;import java.net.http.*;import java.time.Duration;
/** Local-only Ollama client. */
public final class OllamaClient{
 private final HttpClient http=HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(2)).build();private final String endpoint,model;
 public OllamaClient(String endpoint,String model){this.endpoint=endpoint;this.model=model;}
 public String generate(String prompt){String body="{\"model\":\""+esc(model)+"\",\"prompt\":\""+esc(prompt)+"\",\"stream\":false,\"format\":\"json\"}";try{var req=HttpRequest.newBuilder(URI.create(endpoint+"/api/generate")).timeout(Duration.ofSeconds(20)).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(body)).build();return http.send(req,HttpResponse.BodyHandlers.ofString()).body();}catch(Exception e){return null;}}
 private static String esc(String s){return s.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n");}
}
