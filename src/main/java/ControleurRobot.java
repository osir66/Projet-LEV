import javafx.animation.AnimationTimer;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;

public class ControleurRobot extends BorderPane {
    private final Carte carte;
    private final AffichageCarte affichageCarte;
    private final ListView<String> listeConsoleStatut;

    public ControleurRobot(Carte carte) {
    this.carte = carte;

    int largeurPixels = carte.getLargeurX() * 40;
    int hauteurPixels = carte.getHauteurY() * 40;

    this.affichageCarte = new AffichageCarte(carte, largeurPixels, hauteurPixels);
    this.setCenter(affichageCarte);

    this.setPrefSize(largeurPixels + 240, hauteurPixels);

    VBox panneauInfos = new VBox(10);
    panneauInfos.setStyle("-fx-padding: 10; -fx-background-color: #f8f9fa; -fx-border-color: #e0e0e0; -fx-border-width: 0 0 0 1;");
    panneauInfos.setPrefWidth(240);
    panneauInfos.setMinHeight(hauteurPixels); 

    Label titrePanneau = new Label("Moniteur d'activité (Threads)");
    titrePanneau.setStyle("-fx-font-weight: bold; -fx-font-size: 13px;");

    this.listeConsoleStatut = new ListView<>();
    listeConsoleStatut.setStyle("-fx-font-family: 'Courier New'; -fx-font-size: 11px;");
    listeConsoleStatut.setPrefHeight(hauteurPixels - 40); 

    panneauInfos.getChildren().addAll(titrePanneau, listeConsoleStatut);
    this.setRight(panneauInfos);

    AnimationTimer boucleSimulation = new AnimationTimer() {
        @Override
        public void handle(long now) {
            rafraichirIHM();
        }
    };
    boucleSimulation.start();
    }
    
    private void rafraichirIHM() {
        affichageCarte.dessiner();

        listeConsoleStatut.getItems().clear();
        synchronized (carte) {
            for (Robot robot : carte.getRobots()) {
                String logRobot = String.format("[%s] Pos: (%d,%d)", robot.getNom(), robot.getX(), robot.getY());
                
                if (robot.getMissionActuelle() != null) {
                    logRobot += " -> Cible: " + robot.getMissionActuelle().getSymbole();
                } else {
                    logRobot += " -> En attente";
                }
                listeConsoleStatut.getItems().add(logRobot);
            }
        }
    }
}