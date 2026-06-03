import javafx.application.Platform;
import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.scene.control.*;
import java.net.http.*;
import java.net.URI;

public class commande extends VBox {

    private TextField urlBase;
    private Button btnAjouter;
    private ListView<String> historique;

    public commande() {
        urlBase = new TextField("localhost:8000");
        urlBase.setPromptText("ex: 192.168.1.101:8000");

        Label lblUrl = new Label("URL du serveur : ");
        HBox urlBar = new HBox(5, lblUrl, urlBase);

        btnAjouter = new Button("Ajouter sémaphore");
        historique = new ListView<>();

        btnAjouter.setOnAction(e -> {
            String base = urlBase.getText().trim();
            String url = "http://" + base + "/ajouter_semaphore?etat=true&dessin_forme=carre&matrice=1.2";
            System.out.println("Envoi de la requête a : " + url);
            btnAjouter.setDisable(true);

            new Thread(() -> {
                String resultat;
                try {
                    HttpClient client = HttpClient.newHttpClient();
                    HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .POST(HttpRequest.BodyPublishers.noBody())
                        .build();
                    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                    String body = response.body();
                    resultat = "[" + response.statusCode() + "] " + (body.isEmpty() ? "OK (réponse vide)" : body);
                } catch (Exception ex) {
                    resultat = "Erreur : " + ex.toString();
                }
                String msg = resultat;
                Platform.runLater(() -> {
                    historique.getItems().add(msg);
                    btnAjouter.setDisable(false);
                });
            }).start();
        });

        this.getChildren().addAll(urlBar, btnAjouter, historique);
        this.setSpacing(10);
    }
}
