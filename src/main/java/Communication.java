import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Communication {


    //private a mettre

public static void postMissionDirect(String shape_id, String nom, String ip, String semaphore_id, String team, String time) {
        HttpClient client = HttpClient.newHttpClient();
        
        // Concaténation pure de l'URL
        String url = "http://" + ip + "/api/add_mission?semaphore_id=" + semaphore_id +"&name=Massilia"+ "&shape_id=" + shape_id + "&team=" + team + "&time=" + time;
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .POST(HttpRequest.BodyPublishers.noBody()) 
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            
            System.out.println("Statut : " + response.statusCode());
            System.out.println("Corps : " + response.body());

        } catch (Exception e) {
            System.err.println("Erreur réseau : " + e.getMessage());
        }
    }

}