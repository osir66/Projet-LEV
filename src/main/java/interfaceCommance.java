import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.scene.control.*;

import java.util.List;
import java.util.ArrayList;

public class interfaceCommance extends VBox {

    TextField urlBase;
    TextField temps;
    Button btnRechercher;
    Button Envoyer;
    ListView<String> listeSemaphoresUI;
    ListView<String> listeFormesUI;
    semaphore semaphores = new semaphore();
    List<semaphore.Semaphore> listSemaphores = new ArrayList<>(semaphores.getSemaphores());
    forme formes = new forme();
    List<forme.FormeList> listFormes = new ArrayList<>(formes.getFormes());

    public interfaceCommance() {

        urlBase = new TextField("http://localhost:8080");
        temps = new TextField();

        // Limiter le champ de texte à n'accepter que des chiffres rond
        temps.setTextFormatter(new TextFormatter<>(change ->
            change.getControlNewText().matches("\\d*") ? change : null
        ));

        btnRechercher = new Button("Rechercher");
        listeSemaphoresUI = new ListView<>();
        for (semaphore.Semaphore s : listSemaphores) {
            listeSemaphoresUI.getItems().add(" | état=" + s.etat() + " | nom=" + s.nom());
        }

        listeFormesUI = new ListView<>();
        for (forme.FormeList f : listFormes) {
            listeFormesUI.getItems().add(" | nom=" + f.nom());
        }

        Envoyer = new Button("Envoyer");
        Envoyer.setOnAction(e -> {
            new Thread(() -> {
                try {
                    //bouchon pour le jalon 1
                    Communication.postMissionDirect("c2f75c2c-3ed1-4368-a062-002a3b37766e", "carre", "192.168.1.101:8000", "fe8c0f2e-b05b-4b2b-aac0-dbbf57bbd2c5", "GObelin", "180");
                } catch (Exception ex) {
                    System.out.println("Erreur : " + ex.toString());
                }
            }).start();
        });

        this.getChildren().addAll(urlBase, btnRechercher, new Label("Sémaphores :"), listeSemaphoresUI, new Label("Formes :"), listeFormesUI, new Label("Temps (en s):"), temps, Envoyer);
        this.setSpacing(10);
    }
}
