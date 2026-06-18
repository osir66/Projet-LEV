import javafx.animation.AnimationTimer;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;

/**
Le panneau principal de l'interface.
Il sépare l'écran en deux : la zone de dessin au centre,
et un panneau d'informations sur le côté droit.
**/
public class ControleurRobot extends BorderPane {
    private final Carte carte;
    private final AffichageCarte affichageCarte;
    private final ListView<String> listeConsoleStatut; // Affiche les logs en direct

    public ControleurRobot(Carte carte) {
        this.carte = carte;

        // Calcul dynamique de la taille de la fenêtre en fonction de la grille
        int largeurPixels = carte.getLargeurX() * 40;
        int hauteurPixels = carte.getHauteurY() * 40;

        // Initialisation de la zone de dessin
        this.affichageCarte = new AffichageCarte(carte, largeurPixels, hauteurPixels);
        this.setCenter(affichageCarte); // Place le canvas au centre

        this.setPrefSize(largeurPixels + 240, hauteurPixels);

        // Création du panneau latéral
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
        this.setRight(panneauInfos); // Place le menu à droite

        // Boucle de l'animation
        AnimationTimer boucleSimulation = new AnimationTimer() {
            @Override
            public void handle(long now) {
                rafraichirIHM(); // Met à jour l'écran et les textes
            }
        };
        boucleSimulation.start();
    }
    
    // Rafraîchit les éléments visuels de la fenêtre.
    private void rafraichirIHM() {
        // Redessine le Canvas
        affichageCarte.dessiner();

        // Met à jour la liste des logs
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