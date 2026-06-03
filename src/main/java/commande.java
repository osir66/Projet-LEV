import javafx.scene.layout.VBox;
import javafx.scene.control.*;
import java.net.http.*;
import java.net.URI;

public class commande extends VBox {

    private Label titre;
    private Button btnAjouter;
    private ListView<String> historique;

    public commande() {
        titre = new Label();
        btnAjouter = new Button("Ajouter sémaphore");
        historique = new ListView<>();

        btnAjouter.setOnAction(e -> {
            try {
                String url = "http://localhost:8000/ajouter_semaphore?etat=true&dessin_forme=carre&matrice=1.2";
                HttpClient client = HttpClient.newHttpClient();
                HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .POST(HttpRequest.BodyPublishers.noBody())
                    .build();
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                historique.getItems().add("Réponse : " + response.body());
            } catch (Exception ex) {
                historique.getItems().add("Erreur : " + ex.getMessage());
            }
        });

        this.getChildren().addAll(titre, btnAjouter, historique);
        this.setSpacing(10);
    }

    public void setTitre(String text) {
        titre.setText(text);
    }

    public void setBoutonLabel(String text) {
        btnAjouter.setText(text);
    }
}
