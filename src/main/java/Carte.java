// voir pour utiliser une matrice à la place d'une carte et des coordonnées

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Carte {
    private List<Robot> listeRobots;
    private Set<String> missionsEnCours;

    private final int baseX = 0;
    private final int baseY = 0;

    public Carte() {
        this.listeRobots = new ArrayList<>();
        this.missionsEnCours = new HashSet<>();
    }

    public synchronized void ajouterRobot(Robot r) {
        listeRobots.add(r);
    }

    public synchronized List<Robot> getRobots() {
        return listeRobots;
    }

    public synchronized boolean reserverMission(String idMission) {
        if (missionsEnCours.contains(idMission)) {
            return false; // mission déjà prise
        }
        missionsEnCours.add(idMission);
        return true;
    }

    public synchronized void libererMission(String idMission) {
        missionsEnCours.remove(idMission);
    }

    public int getBaseX() { 
        return baseX; 
    }
    
    public int getBaseY() {
        return baseY; 
    }
}