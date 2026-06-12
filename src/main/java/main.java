import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.stage.Stage;

public class main extends Application {

    private int compteur = 1;
    
    @Override
    public void start(Stage stage) {
        TabPane tabPane = new TabPane();
        // Onglet + fixe, toujours en dernier
        Tab btnAjouter = new Tab("+");
        btnAjouter.setClosable(false);
        tabPane.getTabs().add(btnAjouter);
        // Premier onglet au démarrage
        ajouterOnglet(tabPane, btnAjouter);
        // Clic sur "+" → nouvel onglet
        tabPane.getSelectionModel().selectedItemProperty().addListener(
                (obs, ancien, nouveau) -> {
                    if (nouveau == btnAjouter) {
                        ajouterOnglet(tabPane, btnAjouter);
                    }
                }
        );
        stage.setScene(new Scene(tabPane, 1000, 500));
        stage.setTitle("Panneau de commande de MASSILIA");
        stage.show();
    }

    private void ajouterOnglet(TabPane tabPane, Tab btnAjouter) {
        Tab tab = new Tab("Mission " + compteur++, new interfaceCommande());
        tab.setClosable(compteur > 2); // le premier onglet n'est pas fermable
        // Insérer juste avant le "+"
        tabPane.getTabs().add(tabPane.getTabs().size() - 1, tab);
        tabPane.getSelectionModel().select(tab);
    }

    public static void main(String[] args) {
        launch(args);
    }

}