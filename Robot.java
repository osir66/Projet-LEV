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

    public void setIdServeur(String idServeur) {
        this.id = idServeur;
    }

    @Override
    public void run() {
        try {
            notifierPosition("Disponible");
        } catch (Exception e) {
            System.err.println("Erreur notification initiale (" + nom + ") : " + e.getMessage());
        }

        while (actif) {
            try {
                if (missionActuelle == null && !retourBase) {
                    notifierPosition("Disponible");
                    verifierNouvelleMission();
                } else if (missionActuelle != null && !retourBase) {
                    // déplacement
                    seDeplacerVers(missionActuelle.getCibleX(), missionActuelle.getCibleY());
                    notifierPosition("En cours");

                    if (x == missionActuelle.getCibleX() && y == missionActuelle.getCibleY()) {
                        allumerSemaphore();
                        
                        String dateFin = Instant.now().toString(); 
                        terminerMission(dateFin);
                        
                        retourBase = true;
                    }
                } else if (retourBase) {
                    // retour base
                    seDeplacerVers(carte.getBaseX(), carte.getBaseY());
                    notifierPosition("Retour Base");

                    if (x == carte.getBaseX() && y == carte.getBaseY()) {
                        System.out.println("Robot " + nom + " est rentré à la base.");
                        missionActuelle = null;
                        retourBase = false;
                        notifierPosition("Disponible");
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
                Missions nouvelleMission = parseJsonMission(reponse);
                if (nouvelleMission != null && nouvelleMission.getIdMission() != null && !nouvelleMission.getIdMission().isEmpty()) {
                    
                    nouvelleMission.setDateDebut(Instant.now().toString());
                    
                    this.missionActuelle = nouvelleMission;
                    System.out.println("Robot " + nom + " a intercepté la mission ID: " + missionActuelle.getIdMission());
                }
            }
        } catch (Exception e) {
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
        String url = String.format("/api/update_semaphore/%s?state=%s",
                missionActuelle.getIdSemaphore(), URLEncoder.encode(missionActuelle.getSymbole(), StandardCharsets.UTF_8));
        webClient.requetePut(url, ""); 
    }
    
    private void terminerMission(String dateFin) throws Exception {
        String dateDebutEncodee = URLEncoder.encode(missionActuelle.getDateDebut(), StandardCharsets.UTF_8);
        String dateFinEncodee = URLEncoder.encode(dateFin, StandardCharsets.UTF_8);
        
        String url = String.format("/api/update_mission/%s?state=%s&robot_id=%s&start_date=%s&end_date=%s",
                missionActuelle.getIdMission(), 
                URLEncoder.encode("Terminee", StandardCharsets.UTF_8),
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
}