import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

/**
Composant graphique responsable de dessiner la grille,
la base, les robots et les lignes de missions à chaque rafraîchissement d'image.
**/
public class AffichageCarte extends Canvas {
    private final Carte carte;
<<<<<<< Updated upstream
    private static final int TAILLE_CASE = 40; 
=======
    private static final int TAILLE_CASE = 35; // Taille visuelle en pixels d'un segment de grille
>>>>>>> Stashed changes

    public AffichageCarte(Carte carte, double width, double height) {
        super(width, height);
        this.carte = carte;
    }

<<<<<<< Updated upstream
    public void dessiner() {
        GraphicsContext gc = this.getGraphicsContext2D();
        
        gc.clearRect(0, 0, getWidth(), getHeight());
=======
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
>>>>>>> Stashed changes
        
        // Ligne connectant la base (0, 0) à l'entrée de la grille (0,1)
        gc.setStroke(Color.LIGHTGRAY);
        gc.setLineWidth(0.5);
        for (int x = 0; x < getWidth(); x += TAILLE_CASE) {
            gc.strokeLine(x, 0, x, getHeight());
        }
        for (int y = 0; y < getHeight(); y += TAILLE_CASE) {
            gc.strokeLine(0, y, getWidth(), y);
        }

        int baseX = carte.getBaseX() * TAILLE_CASE;
        int baseY = carte.getBaseY() * TAILLE_CASE;
        gc.setFill(Color.DARKGREEN);
        gc.fillRect(baseX, baseY, TAILLE_CASE, TAILLE_CASE);
        gc.setFill(Color.WHITE);
        gc.fillText("BASE", baseX + 5, baseY + 24);

        // Dessin des robots et des missions
        synchronized (carte) {
            for (Robot robot : carte.getRobots()) {
                int rx = robot.getX() * TAILLE_CASE;
                int ry = robot.getY() * TAILLE_CASE;

                // Si le robot a une cible, on dessine un marqueur rouge et une ligne
                if (robot.getMissionActuelle() != null) {
                    Missions m = robot.getMissionActuelle();
                    int cx = m.getCibleX() * TAILLE_CASE;
                    int cy = m.getCibleY() * TAILLE_CASE;

                    gc.setStroke(Color.RED);
                    gc.setLineWidth(2);
                    gc.strokeRect(cx + 2, cy + 2, TAILLE_CASE - 4, TAILLE_CASE - 4);
                    gc.setFill(Color.RED);
                    gc.fillText("Sém: " + m.getSymbole(), cx + 2, cy - 4);

<<<<<<< Updated upstream
                    gc.setStroke(Color.rgb(255, 0, 0, 0.3));
=======
                    // Ligne liant le robot à son objectif
                    gc.setStroke(Color.rgb(255, 0, 0, 0.25));
>>>>>>> Stashed changes
                    gc.setLineWidth(1);
                    gc.strokeLine(rx + (TAILLE_CASE / 2.0), ry + (TAILLE_CASE / 2.0), cx + (TAILLE_CASE / 2.0), cy + (TAILLE_CASE / 2.0));
                }

                // Dessin du robot
                gc.setFill(Color.DODGERBLUE);
                gc.fillOval(rx + 6, ry + 6, TAILLE_CASE - 12, TAILLE_CASE - 12);
                
                gc.setStroke(Color.BLACK);
<<<<<<< Updated upstream
                gc.setLineWidth(1.5);
                gc.strokeOval(rx + 6, ry + 6, TAILLE_CASE - 12, TAILLE_CASE - 12);

=======
                gc.setLineWidth(1);
                gc.strokeOval(rx - 8, ry - 8, 16, 16);
                
                // Étiquette du nom
>>>>>>> Stashed changes
                gc.setFill(Color.BLACK);
                gc.fillText(robot.getNom(), rx, ry - 4);
            }
        }
    }
}