import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Carte {
    private List<Robot> listeRobots;
    private Set<String> missionsEnCours;
    private Map<String, int[]> positionsSemaphores; 
    
    private Set<String> positionsOccupees;

    private String nomGrille = "Defaut";
    private int largeurX = 15;
    private int hauteurY = 15;

    private final int baseX = 0;
    private final int baseY = 0;

    public Carte() {
        this.listeRobots = new ArrayList<>();
        this.missionsEnCours = new HashSet<>();
        this.positionsSemaphores = new HashMap<>();
        this.positionsOccupees = new HashSet<>();
    }

    public synchronized boolean demanderDeplacement(int xActuel, int yActuel, int xCible, int yCible) {
        String cleCible = xCible + "," + yCible;
        String cleActuelle = xActuel + "," + yActuel;

        if (xCible == 0 && yCible == 0) {
            if (!(xActuel == 0 && yActuel == 0)) {
                positionsOccupees.remove(cleActuelle);
            }
            return true;
        }

        if (positionsOccupees.contains(cleCible)) {
            return false;
        }

        if (!(xActuel == 0 && yActuel == 0)) {
            positionsOccupees.remove(cleActuelle); 
        }
        positionsOccupees.add(cleCible);
        
        return true;
    }

    public synchronized void ajouterPositionSemaphore(String id, int x, int y) {
        positionsSemaphores.put(id, new int[]{x, y});
    }

    public synchronized int getSemaphoreX(String id, int valeurParDefaut) {
        if (positionsSemaphores.containsKey(id)) {
            return positionsSemaphores.get(id)[0];
        }
        return valeurParDefaut;
    }

    public synchronized int getSemaphoreY(String id, int valeurParDefaut) {
        if (positionsSemaphores.containsKey(id)) {
            return positionsSemaphores.get(id)[1];
        }
        return valeurParDefaut;
    }

    public void setConfiguration(String nom, int x, int y) {
        this.nomGrille = nom;
        this.largeurX = x;
        this.hauteurY = y;
    }

    public int getLargeurX() { 
        return largeurX; 
    }

    public int getHauteurY() { 
        return hauteurY; 
    }

    public String getNomGrille() { 
        return nomGrille; 
    }
    
    public synchronized void ajouterRobot(Robot r) { 
        listeRobots.add(r); 
    }

    public synchronized List<Robot> getRobots() { 
        return listeRobots; 
    }

    public synchronized boolean reserverMission(String idMission) {
        if (missionsEnCours.contains(idMission)) {
            return false;
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