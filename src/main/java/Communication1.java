import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class Communication1 {

    private String ip;
    private String port;
    private String urlBase;

    public Communication1(String ip, String port) {
        this.ip = ip;
        this.port = port;
        this.urlBase = "http://" + this.ip + ":" + this.port + "/api/";
    }

    // LES MÉTHODES
    public void envoieMission(String name, String semaphore_id, int time, String team, String shape_id) {
        try {
            String adresse = this.urlBase + "add_mission" +
                    "?name=" + URLEncoder.encode(name, StandardCharsets.UTF_8) +
                    "&semaphore_id=" + URLEncoder.encode(semaphore_id, StandardCharsets.UTF_8) +
                    "&time=" + time +
                    "&team=" + URLEncoder.encode(team, StandardCharsets.UTF_8) +
                    "&shape_id=" + URLEncoder.encode(shape_id, StandardCharsets.UTF_8);

            System.out.println("Envoi vers " + adresse);

            URL url = new URL(adresse);
            HttpURLConnection connexion = (HttpURLConnection) url.openConnection();

            connexion.setRequestMethod("POST");
            connexion.setDoOutput(true);

            int codeReponse = connexion.getResponseCode();
            String reponse = connexion.getResponseMessage();

            if (codeReponse == 200) {
                System.out.println("Mission envoyé avec succès");
            } else {
                System.out.println("Erreur envoie de missions " + codeReponse + " : " + reponse);
            }

        } catch (Exception erreur) {
            System.out.println("Impossible : " + erreur.getMessage());
        }
    }

    public String getListSemaphores() {
        try {
            String lien = this.urlBase + "list_semaphore";
            System.out.println("Recherche sur : " + lien);
URL url = new URL(lien);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            int code = conn.getResponseCode();

            if (code == 200) {
                BufferedReader lecteur = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String reponse = lecteur.readLine();
                lecteur.close();
                System.err.println("Réponse brute : " + reponse);
                return reponse;
            } else {
                return "Erreur serveur : " + code;
            }

        } catch (Exception e) {
            return "Impossible de joindre l'IP : " + e.getMessage();
        }
    }

    public String getMissionsByTeam(String team) {
        try {
            String lien = this.urlBase + "list_missions_by_team?team=" + URLEncoder.encode(team, StandardCharsets.UTF_8);
            URL url = new URL(lien);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            int code = conn.getResponseCode();
            if (code == 200) {
                BufferedReader lecteur = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String reponse = lecteur.readLine();
                lecteur.close();
                return reponse;
            } else {
                return "Erreur serveur : " + code;
            }
        } catch (Exception e) {
            return "Impossible de joindre l'IP : " + e.getMessage();
        }
    }

    public String getListSymboles() {
        try {
            String lien = this.urlBase + "list_shapes";
            System.out.println("Recherche sur : " + lien);

            URL url = new URL(lien);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            int code = conn.getResponseCode();

            if (code == 200) {
                BufferedReader lecteur = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String reponse = lecteur.readLine();
                lecteur.close();
                return reponse;
            } else {
                return "Erreur serveur : " + code;
            }

        } catch (Exception e) {
            return "Impossible de joindre l'IP : " + e.getMessage();
        }
    }
}