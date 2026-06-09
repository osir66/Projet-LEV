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

    public String getNom() {
    return nom;
}

    public void setIdServeur(String idServeur) {
        this.id = idServeur;
    }

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
                    verifierNouvelleMission();
                } else if (missionActuelle != null && !retourBase) {
                    // déplacement
                    seDeplacerVers(missionActuelle.getCibleX(), missionActuelle.getCibleY());
                    notifierPosition("Pending");

                    if (x == missionActuelle.getCibleX() && y == missionActuelle.getCibleY()) {
                        allumerSemaphore();
                        
                        String dateFin = Instant.now().toString(); 
                        terminerMission(dateFin);
                        
                        carte.libererMission(missionActuelle.getIdMission());

                        retourBase = true;
                    }
                } else if (retourBase) {
                    // retour base
                    seDeplacerVers(carte.getBaseX(), carte.getBaseY());
                    notifierPosition("Returning To Base");

                    if (x == carte.getBaseX() && y == carte.getBaseY()) {
                        System.out.println("Robot " + nom + " est rentré à la base.");
                        missionActuelle = null;
                        retourBase = false;
                        notifierPosition("Available");
                    }
                }
                Thread.sleep(1000); // 1 pas/seconde
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            } catch (Exception e) {
                System.err.println("Erreur boucle (Robot " + nom + ") : " + e.getMessage());
            }
        }
    }

    private void seDeplacerVers(int cibleX, int cibleY) {
        if (x < cibleX) x++;
        else if (x > cibleX) x--;
        if (y < cibleY) y++;
        else if (y > cibleY) y--;
    }

    private void verifierNouvelleMission() {
        try {
            String url = "/api/list_missions";
            String reponse = webClient.requeteGet(url);
            
            if (reponse != null && !reponse.trim().isEmpty() && !reponse.trim().equals("[]") && !reponse.contains("detail")) {
                
                java.util.List<Missions> missionsDisponibles = parserToutesMissions(reponse);
                
                for (Missions missionPotentielle : missionsDisponibles) {
                    if (missionPotentielle != null && missionPotentielle.getIdMission() != null && !missionPotentielle.getIdMission().isEmpty()) {
                        
                        if (carte.reserverMission(missionPotentielle.getIdMission())) {
                            missionPotentielle.setDateDebut(Instant.now().toString());
                            this.missionActuelle = missionPotentielle;
                            System.out.println("Robot " + nom + " a intercepté la mission ID: " + missionActuelle.getIdMission());
                            
                            String urlUpdate = String.format("/api/update_semaphore/%s?state=Pending", missionActuelle.getIdSemaphore());
                            webClient.requetePut(urlUpdate, ""); 
                            
                            break;
                        }
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Erreur vérification mission (" + nom + ") : " + e.getMessage());
        }
    }

    private void notifierPosition(String etat) throws Exception {
        String url = String.format("/api/update_robot/%s?state=%s&position_x=%d&position_y=%d",
                id, URLEncoder.encode(etat, StandardCharsets.UTF_8), x, y);
        
        webClient.requetePut(url, ""); 
        System.out.println("Robot " + nom + " (ID Serveur: " + id + ") [" + etat + "] position : (" + x + ", " + y + ")");
    }

    private void allumerSemaphore() throws Exception {
        System.out.println("Robot " + nom + " active le sémaphore " + missionActuelle.getIdSemaphore());
        String url = String.format("/api/update_semaphore/%s?state=Pending",
                missionActuelle.getIdSemaphore());
        webClient.requetePut(url, ""); 
    }
    
    private void terminerMission(String dateFin) throws Exception {
        String dateDebutEncodee = URLEncoder.encode(missionActuelle.getDateDebut(), StandardCharsets.UTF_8);
        String dateFinEncodee = URLEncoder.encode(dateFin, StandardCharsets.UTF_8);
        
        String url = String.format("/api/update_mission/%s?state=%s&robot_id=%s&start_date=%s&end_date=%s",
                missionActuelle.getIdMission(), 
                URLEncoder.encode("Pending", StandardCharsets.UTF_8),
                URLEncoder.encode(this.id, StandardCharsets.UTF_8),
                dateDebutEncodee,
                dateFinEncodee);
                
        webClient.requetePut(url, ""); 
        System.out.println("Mission " + missionActuelle.getIdMission() + " validée par " + nom + " (Début: " + missionActuelle.getDateDebut() + " | Fin: " + dateFin + ")");
    }

    private Missions parseJsonMission(String json) {
        try {
            String idMission = extractValue(json, "id");
            if (idMission.isEmpty()) idMission = extractValue(json, "idMission");
            
            String idSemaphore = extractValue(json, "semaphore_id");
            String symbole = extractValue(json, "shapes_id");
            
            int cibleX = Math.abs(idSemaphore.hashCode() % 15) + 2; 
            int cibleY = Math.abs(idSemaphore.hashCode() % 15) + 2;

            if (idMission.isEmpty() || idSemaphore.isEmpty()) {
                return null;
            }
            return new Missions(idMission, idSemaphore, symbole, cibleX, cibleY);
        } catch (Exception e) {
            return null; 
        }
    }

    private String extractValue(String json, String key) {
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
        if (cleanJson.startsWith("[")) 
            cleanJson = cleanJson.substring(1);
        if (cleanJson.endsWith("]")) 
            cleanJson = cleanJson.substring(0, cleanJson.length() - 1);

        String jsonModifie = cleanJson.replace("},{", "}SPLIT{").replace("}, {", "}SPLIT{");
        
        String[] blocs = jsonModifie.split("SPLIT");

        for (String bloc : blocs) {
            Missions m = parseJsonMission(bloc);
            if (m != null) {
                liste.add(m);
            }
        }
        return liste;
    }
}