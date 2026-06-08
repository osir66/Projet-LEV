import java.net.http.*;
import java.net.URI;

public class request {

    static HttpResponse<String> get(String url) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build();
        return client.send(req, HttpResponse.BodyHandlers.ofString());
    }

    static HttpResponse<String> post(String url) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .POST(HttpRequest.BodyPublishers.noBody())
            .build();
        return client.send(req, HttpResponse.BodyHandlers.ofString());
    }
}
