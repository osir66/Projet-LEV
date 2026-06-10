import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class main extends Application {
    @Override
    public void start(Stage stage) {
        interfaceCommande panneau = new interfaceCommande();

        stage.setScene(new Scene(panneau, 1200, 700));
        stage.setTitle("NEXUS // C2");
        stage.show();
    }

    public static void main(String[] args) { launch(args); }
}
