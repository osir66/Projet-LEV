import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;

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
                    "?name=" + name +
                    "&semaphore_id=" + semaphore_id +
                    "&time=" + time +
                    "&team=" + team +
                    "&shape_id=" + shape_id;

            adresse = adresse.replace(" ", "%20");
            System.out.println("Envoi vers " + adresse);

            URL url = new URL(adresse);
            HttpURLConnection connexion = (HttpURLConnection) url.openConnection();

            connexion.setRequestMethod("POST");
            connexion.setDoOutput(true);

            int codeReponse = connexion.getResponseCode();

            if (codeReponse == 200) {
                System.out.println("Mission envoyé avec succès");
            } else {
                System.out.println("Erreur envoie de missions " + codeReponse);
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
                System.out.println(reponse);
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