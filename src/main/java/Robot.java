import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;

/**
Représente un robot autonome.
Implémente l'interface Runnable pour pouvoir être exécuté dans un Thread séparé.
**/
public class Robot implements Runnable {
    private String id;
    private String nom;
    private int x, y;
    private boolean actif;
    private Missions missionActuelle;
    private Carte carte;
    private Web webClient;
    private boolean retourBase;

    public Robot(String nom, int startX, int startY, Carte carte, Web webClient) {
        this.nom = nom;
        this.id = nom;
        this.x = startX;
        this.y = startY;
        this.carte = carte;
        this.webClient = webClient;
        this.actif = true;
        this.retourBase = false;
    }

    public String getNom() { return nom; }
    public int getX() { return this.x; }
    public int getY() { return this.y; }
    public Missions getMissionActuelle() { return this.missionActuelle; }
    public void setIdServeur(String idServeur) { this.id = idServeur; }

    /**
    La boucle principale du robot (exécutée par le Thread).
    **/
    @Override
    public void run() {
        try {
            notifierPosition("Available");
        } catch (Exception e) {
            System.err.println("Erreur notification initiale (" + nom + ") : " + e.getMessage());
        }

        // Le robot boucle indéfiniment tant qu'il est actif
        while (actif) {
            try {
                // Le robot est inactif à la base et cherche une mission
                if (missionActuelle == null && !retourBase) {
                    notifierPosition("Available");
                    
                    // On verrouille la carte pour chercher les missions
                    synchronized (carte) {
                        try {
                            String reponseMissions = this.webClient.requeteGet("/api/list_missions");
                            java.util.List<Missions> listeMissionsDuServeur = parserToutesMissions(reponseMissions);
                            
                            for (Missions m : listeMissionsDuServeur) {
                                if (m.getStatut() != null && m.getStatut().equalsIgnoreCase("Awaiting")) {
                                    
                                    // Tente de réserver la mission
                                    if (this.carte.reserverMission(m.getIdMission())) {
                                        this.missionActuelle = m;
                                        this.missionActuelle.setDateDebut(LocalDateTime.now().toString());
                                        
                                        System.out.println(String.format("[%s] Mission %s acceptée. Cible: (%d, %d)", 
                                                this.nom, m.getIdMission(), m.getCibleX(), m.getCibleY()));
                                        
                                        // Avertit le serveur que la mission est prise
                                        changerEtatMission(this.missionActuelle, "Pending_robot");
                                        break; // Sort de la boucle, le robot a trouvé une mission
                                    }
                                }
                            }
                        } catch (Exception e) {
                            System.err.println("Erreur lors de la vérification des missions (" + this.nom + ") : " + e.getMessage());
                        }
                    }

                // Le robot a une mission et se dirige vers la cible
                } else if (missionActuelle != null) {
                    avancerVersCible();

                // La mission est finie, le robot rentre à la base
                } else if (retourBase) {
                    int bx = carte.getBaseX();
                    int by = carte.getBaseY();
                    
                    faireUnPasVers(bx, by);
                    notifierPosition("Returning");

                    // Si le robot a atteint les coordonnées de la base (0,0)
                    if (this.x == bx && this.y == by) {
                        retourBase = false;
                        System.out.println(String.format("[%s] De retour à la base et disponible.", this.nom));
                    }
                }
                
                // Le robot attend avant de faire le prochain pas
                Thread.sleep(1000); // 1 pas/seconde
                
            } catch (Exception e) {
                System.err.println("Erreur boucle robot (" + nom + ") : " + e.getMessage());
            }
        }
    }

    /**
    Gère la progression vers la cible et la complétion de la mission.
    **/
    private void avancerVersCible() throws Exception {
        if (this.missionActuelle == null) return;

        int cx = this.missionActuelle.getCibleX();
        int cy = this.missionActuelle.getCibleY();

        faireUnPasVers(cx, cy);
        notifierPosition("Occupied");

        // Si le robot est arrivé sur le sémaphore
        if (this.x == cx && this.y == cy) {
            System.out.println(String.format("[%s] Mission %s complétée !", this.nom, this.missionActuelle.getIdMission()));
            
            allumerSemaphore();
            changerEtatMission(this.missionActuelle, "Pending_semaphore");
            
            // Libère la mission pour que la mémoire de la carte ne sature pas
            this.carte.libererMission(this.missionActuelle.getIdMission());
            this.missionActuelle = null;
            this.retourBase = true; // Déclenche le processus de retour
        }
    }

    /**
    Déplacement orthogonal avec gestion du point de transit (0,1) et des collisions.
    **/
    private void faireUnPasVers(int cibleX, int cibleY) {
        int tempCibleX = cibleX;
        int tempCibleY = cibleY;

        // Gestion du point de transit : on ne sort ou on ne rentre à la base (0,0) que par la case (0,1)
        if (this.x == 0 && this.y == 0) {
            tempCibleX = 0;
            tempCibleY = 1;
        } else if (cibleX == 0 && cibleY == 0 && (this.x != 0 || this.y != 1)) {
            tempCibleX = 0;
            tempCibleY = 1;
        }

        // Calcul de la case idéale selon la distance
        int prochainX = this.x;
        int prochainY = this.y;

        if (this.x != tempCibleX) {
            prochainX = (this.x < tempCibleX) ? this.x + 1 : this.x - 1;
        } else if (this.y != tempCibleY) {
            prochainY = (this.y < tempCibleY) ? this.y + 1 : this.y - 1;
        } else {
            return; // Déjà sur la cible
        }

        // Demande l'autorisation à la carte (système de collisions)
        // Si true : met à jour les coordonnées. Si false : le robot est bloqué sur place.
        if (this.carte.demanderDeplacement(this.x, this.y, prochainX, prochainY)) {
            this.x = prochainX;
            this.y = prochainY;
        }
    }

    // Méthodes réseau pour informer le serveur

    private void notifierPosition(String etat) throws Exception {
        String url = String.format("/api/update_robot/%s?state=%s&position_x=%d&position_y=%d",
                id, URLEncoder.encode(etat, StandardCharsets.UTF_8), x, y);
        this.webClient.requetePut(url, ""); 
    }

    private void allumerSemaphore() {
        try {
            if (missionActuelle != null) {
                String url = String.format("/api/update_semaphore/%s?state=On&coord_x=%d&coord_y=%d", 
                    missionActuelle.getIdSemaphore(),
                    missionActuelle.getCibleX(),
                    missionActuelle.getCibleY()
                );
                this.webClient.requetePut(url, "");
                System.out.println("-> Robot " + nom + " a activé le sémaphore " + missionActuelle.getIdSemaphore());
            }
        } catch (Exception e) {
            System.err.println("Erreur activation sémaphore (" + nom + ") : " + e.getMessage());
        }
    }

    private void changerEtatMission(Missions m, String etat) throws Exception {
        String dDebut = m.getDateDebut() != null ? m.getDateDebut() : LocalDateTime.now().toString();
        
        String url = String.format("/api/update_mission/%s?state=%s&robot_id=%s&start_date=%s",
                m.getIdMission(), 
                URLEncoder.encode(etat, StandardCharsets.UTF_8),
                URLEncoder.encode(this.id, StandardCharsets.UTF_8),
                URLEncoder.encode(dDebut, StandardCharsets.UTF_8));
                
        this.webClient.requetePut(url, ""); 
    }

    // Parsing JSON "simple"

    private String extraireValeur(String json, String key) {
        int keyIndex = json.indexOf("\"" + key + "\"");
        if (keyIndex == -1) return "";
        
        int colonIndex = json.indexOf(":", keyIndex);
        if (colonIndex == -1) return "";
        
        int start = colonIndex + 1;
        while (start < json.length() && (json.charAt(start) == ' ' || json.charAt(start) == '\r' || json.charAt(start) == '\n')) {
            start++;
        }
        
        if (start < json.length() && json.charAt(start) == '"') {
            start++; 
            int end = json.indexOf('"', start);
            if (end == -1) return "";
            return json.substring(start, end);
        } else {
            int end = start;
            while (end < json.length() && (Character.isDigit(json.charAt(end)) || json.charAt(end) == '-' || json.charAt(end) == '.' || Character.isLetter(json.charAt(end)))) {
                end++;
            }
            return json.substring(start, end).trim();
        }
    }

    private java.util.List<Missions> parserToutesMissions(String jsonTableau) {
        java.util.List<Missions> liste = new java.util.ArrayList<>();

        String cleanJson = jsonTableau.trim();
        if (cleanJson.startsWith("[")) cleanJson = cleanJson.substring(1);
        if (cleanJson.endsWith("]")) cleanJson = cleanJson.substring(0, cleanJson.length() - 1);

        String jsonModifie = cleanJson.replace("},{", "}SPLIT{").replace("}, {", "}SPLIT{");
        String[] blocs = jsonModifie.split("SPLIT");
        
        for (String bloc : blocs) {
            String idMission = extraireValeur(bloc, "id");
            if (idMission.isEmpty()) idMission = extraireValeur(bloc, "idMission");
            
            String idSemaphore = extraireValeur(bloc, "semaphore_id");
            String symbole = extraireValeur(bloc, "shapes_id");
            
            String status = extraireValeur(bloc, "state");
            if (status.isEmpty()) status = extraireValeur(bloc, "status");
            if (status.isEmpty()) status = extraireValeur(bloc, "statut");
            
            if (!idMission.isEmpty() && !idSemaphore.isEmpty()) {
                int maxX = this.carte.getLargeurX();
                int maxY = this.carte.getHauteurY();

                // Récupération des coordonnées du sémaphore stockées dans la carte
                int cx = this.carte.getSemaphoreX(idSemaphore, Integer.MIN_VALUE);
                int cy = this.carte.getSemaphoreY(idSemaphore, Integer.MIN_VALUE);

                // Fallback si le sémaphore n'est pas trouvé dans la carte
                if (cx == Integer.MIN_VALUE) {
                    int demiX = maxX / 2;
                    // Permet d'avoir des coordonnées négatives à gauche
                    cx = (Math.abs(idSemaphore.hashCode()) % maxX) - demiX;
                }
                if (cy == Integer.MIN_VALUE) {
                    cy = (Math.abs(idSemaphore.hashCode()) % maxY) + 1;
                }
    
                Missions m = new Missions(idMission, idSemaphore, symbole, cx, cy);
                m.setStatut(status.isEmpty() ? "Awaiting" : status);
                liste.add(m);
            }
        }
        return liste;
    }
}