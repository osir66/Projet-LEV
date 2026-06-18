import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
Classe utilitaire gérant toutes les communications HTTP avec le serveur.
**/
public class Web {
    private final HttpClient httpClient;
    private final String baseUrl;

    public Web(String baseUrl) {
        this.httpClient = HttpClient.newHttpClient();
        this.baseUrl = baseUrl;
    }

    /**
    Envoie une requête HTTP GET pour récupérer des données.
    **/
    public String requeteGet(String endpoint) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + endpoint))
                .GET()
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    /**
    Envoie une requête HTTP POST pour créer des données.
    **/
    public String requetePost(String endpoint, String jsonBody) throws Exception {
        String body = (jsonBody == null) ? "" : jsonBody;
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + endpoint))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    /**
    Envoie une requête HTTP PUT pour mettre à jour l'état sur le serveur.
    **/
    public String requetePut(String endpoint, String jsonBody) throws Exception {
        String body = (jsonBody == null) ? "" : jsonBody;
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + endpoint))
                .header("Content-Type", "application/json")
                .PUT(HttpRequest.BodyPublishers.ofString(body))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}