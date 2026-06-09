import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class main extends Application {
    @Override
    public void start(Stage stage) {
        interfaceCommance panneau = new interfaceCommance();

        stage.setScene(new Scene(panneau, 800, 300));
        stage.setTitle("Projet LEV");
        stage.show();
    }

    public static void main(String[] args) { launch(args); }
}
