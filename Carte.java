// Voir pour utiliser une matrice à la place d'une carte et des coordonnées

import java.util.ArrayList;
import java.util.List;

public class Carte {
    private List<Robot> listeRobots;

    private final int baseX = 0;
    private final int baseY = 0;

    public Carte() {
        this.listeRobots = new ArrayList<>();
    }

    public synchronized void ajouterRobot(Robot r) {
        listeRobots.add(r);
    }

    public synchronized List<Robot> getRobots() {
        return listeRobots;
    }

    public int getBaseX() { 
        return baseX; 
    }
    
    public int getBaseY() {
        return baseY; 
    }
}