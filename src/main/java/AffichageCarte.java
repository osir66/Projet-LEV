import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public class AffichageCarte extends Canvas {
    private final Carte carte;
    private static final int TAILLE_CASE = 35; // Distance entre 2 routes (px)

    public AffichageCarte(Carte carte, double width, double height) {
        super(width, height);
        this.carte = carte;
    }

    private double getPixelX(int gridX) {
        double centerX = getWidth() / 2.0;
        return centerX + (gridX * TAILLE_CASE);
    }

    private double getPixelY(int gridY) {
        double centerY = getHeight() / 2.0;
        return centerY + (gridY * TAILLE_CASE);
    }

    public void dessiner() {
        GraphicsContext gc = this.getGraphicsContext2D();
        gc.clearRect(0, 0, getWidth(), getHeight());

        int demiX = carte.getLargeurX() / 2;
        int demiY = carte.getHauteurY() / 2;

        double coordMinX = getPixelX(-demiX);
        double coordMaxX = getPixelX(demiX);
        double coordMinY = getPixelY(-demiY);
        double coordMaxY = getPixelY(demiY);

        gc.setStroke(Color.LIGHTGRAY);
        gc.setLineWidth(1.5);

        for (int i = -demiX; i <= demiX; i++) {
            double posX = getPixelX(i);
            gc.strokeLine(posX, coordMinY, posX, coordMaxY);
        }

        for (int j = -demiY; j <= demiY; j++) {
            double posY = getPixelY(j);
            gc.strokeLine(coordMinX, posY, coordMaxX, posY);
        }

        double baseX = getPixelX(carte.getBaseX());
        double baseY = getPixelY(carte.getBaseY());
        
        gc.setFill(Color.DARKGREEN);
        gc.fillOval(baseX - 15, baseY - 15, 30, 30);
        
        
        gc.setFill(Color.WHITE);
        gc.fillText("BASE", baseX - 14, baseY + 5);

        synchronized (carte) {
            for (Robot robot : carte.getRobots()) {
                double rx = getPixelX(robot.getX());
                double ry = getPixelY(robot.getY());

                if (robot.getMissionActuelle() != null) {
                    Missions m = robot.getMissionActuelle();
                    double cx = getPixelX(m.getCibleX());
                    double cy = getPixelY(m.getCibleY());

                    gc.setStroke(Color.RED);
                    gc.setLineWidth(2);
                    gc.strokeRect(cx - 10, cy - 10, 20, 20);
                    gc.setFill(Color.RED);
                    gc.fillText("Sém: " + m.getSymbole(), cx + 12, cy - 4);

                    gc.setStroke(Color.rgb(255, 0, 0, 0.25));
                    gc.setLineWidth(1);
                    gc.strokeLine(rx, ry, cx, cy);
                }

                gc.setFill(Color.DODGERBLUE);
                gc.fillOval(rx - 8, ry - 8, 16, 16);
                
                gc.setStroke(Color.BLACK);
                gc.setLineWidth(1);
                gc.strokeOval(rx - 8, ry - 8, 16, 16);
                
                gc.setFill(Color.BLACK);
                gc.fillText(robot.getNom(), rx + 12, ry + 5);
            }
        }
    }
}