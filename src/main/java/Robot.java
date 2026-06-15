import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;

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

    @Override
    public void run() {
        try {
            notifierPosition("Available");
        } catch (Exception e) {
            System.err.println("Erreur notification initiale (" + nom + ") : " + e.getMessage());
        }

        while (actif) {
            try {
                if (missionActuelle == null && !retourBase) {
                    notifierPosition("Available");
                    
                    synchronized (carte) {
                        try {
                            String reponseMissions = this.webClient.requeteGet("/api/list_missions");
                            java.util.List<Missions> listeMissionsDuServeur = parserToutesMissions(reponseMissions);
                            
                            for (Missions m : listeMissionsDuServeur) {
                                if (m.getStatut() != null && m.getStatut().equalsIgnoreCase("Awaiting")) {
                                    
                                    if (this.carte.reserverMission(m.getIdMission())) {
                                        this.missionActuelle = m;
                                        this.missionActuelle.setDateDebut(Instant.now().toString());
                                        
                                        System.out.println(String.format("[%s] Mission %s acceptée. Cible: (%d, %d)", 
                                                this.nom, m.getIdMission(), m.getCibleX(), m.getCibleY()));
                                        
                                        changerEtatMission(this.missionActuelle, "Pending_robot", "");
                                        
                                        break; 
                                    }
                                }
                            }
                        } catch (Exception e) {
                            System.err.println("Erreur lors de la vérification des missions (" + this.nom + ") : " + e.getMessage());
                        }
                    }

                } else if (missionActuelle != null) {
                    avancerVersCible();
                } else if (retourBase) {
                    // Retour base
                    int bx = carte.getBaseX();
                    int by = carte.getBaseY();
                    if (this.x < bx) this.x++;
                    else if (this.x > bx) this.x--;
                    else if (this.y < by) this.y++;
                    else if (this.y > by) this.y--;

                    notifierPosition("Returning");

                    if (this.x == bx && this.y == by) {
                        retourBase = false;
                        System.out.println(String.format("[%s] De retour à la base et disponible.", this.nom));
                    }
                }
                Thread.sleep(100); // 10 pas/seconde
            } catch (Exception e) {
                System.err.println("Erreur boucle robot (" + nom + ") : " + e.getMessage());
            }
        }
    }

    private void verifierNouvelleMission() {
        try {
            String reponseMissions = this.webClient.requeteGet("/api/list_missions");
            java.util.List<Missions> listeMissionsDuServeur = parserToutesMissions(reponseMissions);
            
            for (Missions m : listeMissionsDuServeur) {
                if (m.getStatut() != null && m.getStatut().equalsIgnoreCase("Awaiting")) {
                    
                    if (this.carte.reserverMission(m.getIdMission())) {
                        this.missionActuelle = m;
                        this.missionActuelle.setDateDebut(Instant.now().toString());
                        
                        System.out.println(String.format("[%s] Mission %s acceptée. Cible: (%d, %d)", 
                                this.nom, m.getIdMission(), m.getCibleX(), m.getCibleY()));
                        
                        changerEtatMission(this.missionActuelle, "Pending_robot", "");
                        break;
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Erreur lors de la vérification des missions (" + this.nom + ") : " + e.getMessage());
        }
    }

    private void avancerVersCible() throws Exception {
        if (this.missionActuelle == null) return;

        int cx = this.missionActuelle.getCibleX();
        int cy = this.missionActuelle.getCibleY();

        if (this.x < cx) this.x++;
        else if (this.x > cx) this.x--;
        else if (this.y < cy) this.y++;
        else if (this.y > cy) this.y--;

        notifierPosition("Occupied");

        if (this.x == cx && this.y == cy) {
            System.out.println(String.format("[%s] Mission %s complétée !", this.nom, this.missionActuelle.getIdMission()));
            
            allumerSemaphore();
            
            String dateFin = Instant.now().toString();
            changerEtatMission(this.missionActuelle, "Pending_semaphore", dateFin);
            
            this.carte.libererMission(this.missionActuelle.getIdMission());
            this.missionActuelle = null;
            this.retourBase = true;
        }
    }

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

    private void changerEtatMission(Missions m, String etat, String dateFin) throws Exception {
        String dDebut = m.getDateDebut() != null ? m.getDateDebut() : Instant.now().toString();
        String dFin = dateFin != null ? dateFin : "";
        
        String url = String.format("/api/update_mission/%s?state=%s&robot_id=%s&start_date=%s&end_date=%s",
                m.getIdMission(), 
                URLEncoder.encode(etat, StandardCharsets.UTF_8),
                URLEncoder.encode(this.id, StandardCharsets.UTF_8),
                URLEncoder.encode(dDebut, StandardCharsets.UTF_8),
                URLEncoder.encode(dFin, StandardCharsets.UTF_8));
                
        this.webClient.requetePut(url, ""); 
    }

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

                int cx = Math.abs(idSemaphore.hashCode() % maxX); 
                int cy = Math.abs(idSemaphore.hashCode() % maxY);
    
                Missions m = new Missions(idMission, idSemaphore, symbole, cx, cy);
                m.setStatut(status.isEmpty() ? "Awaiting" : status);
                liste.add(m);
            }
        }
        return liste;
    }
}