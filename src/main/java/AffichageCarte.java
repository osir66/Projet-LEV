import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public class AffichageCarte extends Canvas {
    private final Carte carte;
    private static final int TAILLE_CASE = 40; 

    public AffichageCarte(Carte carte, double width, double height) {
        super(width, height);
        this.carte = carte;
    }

    public void dessiner() {
        GraphicsContext gc = this.getGraphicsContext2D();
    
        gc.clearRect(0, 0, getWidth(), getHeight());
    
        int colonnes = carte.getLargeurX();
        int lignes = carte.getHauteurY();

        gc.setStroke(Color.LIGHTGRAY);
        gc.setLineWidth(0.5);
    
        for (int i = 0; i <= colonnes; i++) {
            int x = i * TAILLE_CASE;
            gc.strokeLine(x, 0, x, lignes * TAILLE_CASE);
        }
    
        for (int j = 0; j <= lignes; j++) {
            int y = j * TAILLE_CASE;
            gc.strokeLine(0, y, colonnes * TAILLE_CASE, y);
        }

        int baseX = carte.getBaseX() * TAILLE_CASE;
        int baseY = carte.getBaseY() * TAILLE_CASE;
        gc.setFill(Color.DARKGREEN);
        gc.fillRect(baseX, baseY, TAILLE_CASE, TAILLE_CASE);
        gc.setFill(Color.WHITE);
        gc.fillText("BASE", baseX + 5, baseY + 24);

        synchronized (carte) {
            for (Robot robot : carte.getRobots()) {
                int rx = robot.getX() * TAILLE_CASE;
                int ry = robot.getY() * TAILLE_CASE;

                if (robot.getMissionActuelle() != null) {
                    Missions m = robot.getMissionActuelle();
                    int cx = m.getCibleX() * TAILLE_CASE;
                    int cy = m.getCibleY() * TAILLE_CASE;

                    gc.setStroke(Color.RED);
                    gc.setLineWidth(2);
                    gc.strokeRect(cx + 2, cy + 2, TAILLE_CASE - 4, TAILLE_CASE - 4);
                    gc.setFill(Color.RED);
                    gc.fillText("Sém: " + m.getSymbole(), cx + 2, cy - 4);

                    gc.setStroke(Color.rgb(255, 0, 0, 0.3));
                    gc.setLineWidth(1);
                    gc.strokeLine(rx + (TAILLE_CASE / 2.0), ry + (TAILLE_CASE / 2.0), cx + (TAILLE_CASE / 2.0), cy + (TAILLE_CASE / 2.0));
                }

                gc.setFill(Color.DODGERBLUE);
                gc.fillOval(rx + 6, ry + 6, TAILLE_CASE - 12, TAILLE_CASE - 12);
                
                gc.setStroke(Color.BLACK);
                gc.setLineWidth(1.5);
                gc.strokeOval(rx + 6, ry + 6, TAILLE_CASE - 12, TAILLE_CASE - 12);

                gc.setFill(Color.BLACK);
                gc.fillText(robot.getNom(), rx, ry - 4);
            }
        }
    }
}