// voir pour utiliser une matrice à la place d'une carte et des coordonnées

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
Modèle de données centralisé.
Toutes les méthodes modifiant l'état sont "synchronized" pour les Threads,
car plusieurs robots (Threads) peuvent tenter d'y accéder en même temps.
**/
public class Carte {
    private List<Robot> listeRobots;
<<<<<<< Updated upstream
    private Set<String> missionsEnCours;
=======
    private Set<String> missionsEnCours; // Évite que 2 robots prennent la même mission
    private Map<String, int[]> positionsSemaphores; // Dictionnaire ID_Sémaphore -> [x,y]
    
    // Registre des cases actuellement occupées (Système de collisions)
    private Set<String> positionsOccupees;
>>>>>>> Stashed changes

    // Dimensions et nom récupérés depuis l'API /api/get_config
    private String nomGrille = "Defaut";
    private int largeurX = 15;
    private int hauteurY = 15;

    // La base est fixe
    private final int baseX = 0;
    private final int baseY = 0;

    public Carte() {
        this.listeRobots = new ArrayList<>();
        this.missionsEnCours = new HashSet<>();
<<<<<<< Updated upstream
=======
        this.positionsSemaphores = new HashMap<>();
        this.positionsOccupees = new HashSet<>();
    }

    /**
    Tente de réserver une case sur la grille pour un robot.
    return true si le mouvement est autorisé, false si la case est bloquée.
    **/
    public synchronized boolean demanderDeplacement(int xActuel, int yActuel, int xCible, int yCible) {
        String cleCible = xCible + "," + yCible;
        String cleActuelle = xActuel + "," + yActuel;

        // La base (0,0) est une zone partagée (donc pas de collision possible).
        if (xCible == 0 && yCible == 0) {
            // Si le robot n'était pas déjà à la base, on libère sa case précédente.
            if (!(xActuel == 0 && yActuel == 0)) {
                positionsOccupees.remove(cleActuelle);
            }
            return true;
        }

        // Si la cible est déjà dans la liste des cases occupées, mouvement refusé.
        if (positionsOccupees.contains(cleCible)) {
            return false;
        }

        // Mouvement autorisé. Libération de l'ancienne case et verrouillage de la nouvelle.
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
        return valeurParDefaut; // Renvoie un sémaphore "Fallback" si le sémaphore n'existe pas encore
    }

    public synchronized int getSemaphoreY(String id, int valeurParDefaut) {
        if (positionsSemaphores.containsKey(id)) {
            return positionsSemaphores.get(id)[1];
        }
        return valeurParDefaut;
>>>>>>> Stashed changes
    }

    public void setConfiguration(String nom, int x, int y) {
        this.nomGrille = nom;
        this.largeurX = x;
        this.hauteurY = y;
    }

<<<<<<< Updated upstream
    public int getLargeurX() {
        return largeurX;
=======
    // Getters et Setters
    public int getLargeurX() { 
        return largeurX; 
>>>>>>> Stashed changes
    }

    public int getHauteurY() {
        return hauteurY;
    }

<<<<<<< Updated upstream
    public String getNomGrille() {
        return nomGrille;
=======
    public String getNomGrille() { 
        return nomGrille; 
    }

    public synchronized void ajouterRobot(Robot r) { 
        listeRobots.add(r); 
>>>>>>> Stashed changes
    }

    public synchronized void ajouterRobot(Robot r) {
        listeRobots.add(r);
    }

    public synchronized List<Robot> getRobots() {
        return listeRobots;
    }


    /**
    Tente de réserver une mission.
    return true si la mission a pu être verrouillée, false si un autre robot l'a déjà prise.
    **/
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

<<<<<<< Updated upstream
    public int getBaseX() { 
        return baseX; 
    }
    
    public int getBaseY() {
        return baseY; 
    }
=======
    public int getBaseX() { return baseX; }
    public int getBaseY() { return baseY; }
>>>>>>> Stashed changes
}