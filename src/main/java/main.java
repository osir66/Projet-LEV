import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class main extends Application {
    @Override
    public void start(Stage stage) {
        commande panneau = new commande();

        // On personnalise depuis main
        panneau.setTitre("Contrôle Robot LEV");
        panneau.setBoutonLabel("Envoyer commande");

        stage.setScene(new Scene(panneau, 400, 300));
        stage.setTitle("Projet LEV");
        stage.show();
    }

    public static void main(String[] args) { launch(args); }
}
