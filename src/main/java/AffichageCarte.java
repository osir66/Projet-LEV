import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

/**
Composant graphique responsable de dessiner la grille,
la base, les robots et les lignes de missions à chaque rafraîchissement d'image.
**/
public class AffichageCarte extends Canvas {
    private final Carte carte;
    private static final int TAILLE_CASE = 35; // Taille visuelle en pixels d'un segment de grille

    public AffichageCarte(Carte carte, double width, double height) {
        super(width, height);
        this.carte = carte;
    }

    /**
    Convertit une coordonnée de la grille X en un pixel.
    Le point 0 est centré horizontalement.
    **/
    private double getPixelX(int gridX) {
        double centerX = getWidth() / 2.0;
        return centerX + (gridX * TAILLE_CASE);
    }

    
    //Convertit une coordonnée de la grille Y en un pixel
    private double getPixelY(int gridY) {
        double paddingY = (getHeight() - (carte.getHauteurY() * TAILLE_CASE)) / 2.0;
        // La soustraction (getHeight() - ...) permet de placer le point (0) en bas de l'écran
        return getHeight() - paddingY - (gridY * TAILLE_CASE);
    }

    /**
    Méthode appelée à chaque frame par l'AnimationTimer du ControleurRobot.
    **/
    public void dessiner() {
        GraphicsContext gc = this.getGraphicsContext2D();
        
        // On efface l'écran précédent avant de redessiner
        gc.clearRect(0, 0, getWidth(), getHeight());

        int demiX = carte.getLargeurX() / 2;
        int maxY = carte.getHauteurY();

        // Limites de la grille (commence à Y = 1 pour laisser la base seule en Y = 0)
        double coordMinX = getPixelX(-demiX);
        double coordMaxX = getPixelX(demiX);
        double coordMinY = getPixelY(1);    
        double coordMaxY = getPixelY(maxY); 

        gc.setStroke(Color.LIGHTGRAY);
        gc.setLineWidth(1.5);

        // Dessin des colonnes
        for (int i = -demiX; i <= demiX; i++) {
            double posX = getPixelX(i);
            gc.strokeLine(posX, coordMinY, posX, coordMaxY);
        }

        // Dessin des lignes (de 1 à maxY)
        for (int j = 1; j <= maxY; j++) {
            double posY = getPixelY(j);
            gc.strokeLine(coordMinX, posY, coordMaxX, posY);
        }

        // Dessin de la base
        double baseX = getPixelX(carte.getBaseX());
        double baseY = getPixelY(carte.getBaseY());
        
        // Ligne connectant la base (0, 0) à l'entrée de la grille (0,1)
        gc.setStroke(Color.LIGHTGRAY);
        gc.strokeLine(baseX, baseY, baseX, getPixelY(1));

        gc.setFill(Color.DARKGREEN);
        gc.fillOval(baseX - 15, baseY - 15, 30, 30);
        
        gc.setFill(Color.WHITE);
        gc.fillText("BASE", baseX - 14, baseY + 5);

        // Dessin des robots et des missions
        synchronized (carte) {
            for (Robot robot : carte.getRobots()) {
                double rx = getPixelX(robot.getX());
                double ry = getPixelY(robot.getY());

                // Si le robot a une cible, on dessine un marqueur rouge et une ligne
                if (robot.getMissionActuelle() != null) {
                    Missions m = robot.getMissionActuelle();
                    double cx = getPixelX(m.getCibleX());
                    double cy = getPixelY(m.getCibleY());

                    gc.setStroke(Color.RED);
                    gc.setLineWidth(2);
                    gc.strokeRect(cx - 10, cy - 10, 20, 20);
                    gc.setFill(Color.RED);
                    gc.fillText("Sém: " + m.getSymbole(), cx + 12, cy - 4);

                    // Ligne liant le robot à son objectif
                    gc.setStroke(Color.rgb(255, 0, 0, 0.25));
                    gc.setLineWidth(1);
                    gc.strokeLine(rx, ry, cx, cy);
                }

                // Dessin du robot
                gc.setFill(Color.DODGERBLUE);
                gc.fillOval(rx - 8, ry - 8, 16, 16);
                
                gc.setStroke(Color.BLACK);
                gc.setLineWidth(1);
                gc.strokeOval(rx - 8, ry - 8, 16, 16);
                
                // Étiquette du nom
                gc.setFill(Color.BLACK);
                gc.fillText(robot.getNom(), rx + 12, ry + 5);
            }
        }
    }
}