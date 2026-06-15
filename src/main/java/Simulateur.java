import java.util.ArrayList;
import java.util.List;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Simulateur extends Application {

    private static final String URL_SERVEUR = "http://192.168.1.22:8000";

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println("Démarrage du Simulateur de Robots");
        System.out.println("=========================================");
        
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        Web clientWeb = new Web(URL_SERVEUR);
        Carte carte = new Carte();

        try {
            System.out.println("-> Récupération de la configuration de la grille...");
            String jsonConfig = clientWeb.requeteGet("/api/get_config");
            
            if (jsonConfig != null) {
                jsonConfig = jsonConfig.trim();
                if (jsonConfig.startsWith("[")) {
                    int dernierObjetDebut = jsonConfig.lastIndexOf("{");
                    int dernierObjetFin = jsonConfig.lastIndexOf("}");
                    if (dernierObjetDebut != -1 && dernierObjetFin != -1 && dernierObjetFin > dernierObjetDebut) {
                        jsonConfig = jsonConfig.substring(dernierObjetDebut, dernierObjetFin + 1);
                    }
                }
            }

            System.out.println("[DEBUG] JSON à analyser : " + jsonConfig);

            String nomGrille = extraireValeur(jsonConfig, "grille");
            String xStr = extraireValeur(jsonConfig, "nombre_x");
            String yStr = extraireValeur(jsonConfig, "nombre_y");

            if (!xStr.isEmpty() && !yStr.isEmpty()) {
                int tailleX = (int) Double.parseDouble(xStr);
                int tailleY = (int) Double.parseDouble(yStr);
                String nom = nomGrille.isEmpty() ? "Inconnue" : nomGrille;
                
                carte.setConfiguration(nom, tailleX, tailleY);
                System.out.println(String.format("   [OK] Grille '%s' configurée en %dx%d", nom, tailleX, tailleY));
            } else {
                System.out.println("   [Avertissement] Échec d'extraction. Utilisation du fallback (15x15).");
            }

            try {
                String reponseSemaphores = clientWeb.requeteGet("/api/list_semaphore");
                chargerSemaphoresServeur(reponseSemaphores, carte);
            } catch (Exception e) {
                System.err.println("   [Erreur Sémaphores] " + e.getMessage());
            }

            System.out.println("\n-> Récupération des robots depuis le serveur...");
            String reponseRobots = clientWeb.requeteGet("/api/list_robots");
            List<Robot> robotsDuServeur = parserRobotsServeur(reponseRobots, carte, clientWeb);
            
            for (Robot r : robotsDuServeur) {
                carte.ajouterRobot(r);
                new Thread(r).start();
            }

            ControleurRobot controleur = new ControleurRobot(carte);
            Scene scene = new Scene(controleur);

            primaryStage.setTitle("Simulateur de Robots - Grille : " + carte.getNomGrille());
            primaryStage.setScene(scene);
            
            primaryStage.sizeToScene();
            primaryStage.show();
            primaryStage.setResizable(false);

        } catch (Exception e) {
            System.err.println("Erreur fatale lors de l'initialisation : " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static List<Robot> parserRobotsServeur(String jsonTableau, Carte carte, Web clientWeb) {
    List<Robot> liste = new ArrayList<>();
    if (jsonTableau == null || jsonTableau.trim().isEmpty() || jsonTableau.trim().equals("[]") || jsonTableau.contains("detail")) {
        return liste;
    }
    String cleanJson = jsonTableau.trim();
    if (cleanJson.startsWith("[")) cleanJson = cleanJson.substring(1);
    if (cleanJson.endsWith("]")) cleanJson = cleanJson.substring(0, cleanJson.length() - 1);
    String jsonModifie = cleanJson.replace("},{", "}SPLIT{").replace("}, {", "}SPLIT{");
    String[] blocs = jsonModifie.split("SPLIT");
    for (String bloc : blocs) {
        String id = extraireValeur(bloc, "id");
        String name = extraireValeur(bloc, "name");
        String xStr = extraireValeur(bloc, "position_x");
        String yStr = extraireValeur(bloc, "position_y");
        
        if (!name.isEmpty()) {
            int startX = xStr.isEmpty() ? carte.getBaseX() : (int) Double.parseDouble(xStr);
            int startY = yStr.isEmpty() ? carte.getBaseY() : (int) Double.parseDouble(yStr);
            
            Robot robot = new Robot(name, startX, startY, carte, clientWeb);
            if (!id.isEmpty()) {
                robot.setIdServeur(id);
            }
            liste.add(robot);
        }
    }
    return liste;
    }

    private static void chargerSemaphoresServeur(String jsonTableau, Carte carte) {
        if (jsonTableau == null || jsonTableau.trim().isEmpty() || jsonTableau.trim().equals("[]") || jsonTableau.contains("detail")) {
            return;
        }
        String cleanJson = jsonTableau.trim();
        if (cleanJson.startsWith("[")) cleanJson = cleanJson.substring(1);
        if (cleanJson.endsWith("]")) cleanJson = cleanJson.substring(0, cleanJson.length() - 1);
        
        String jsonModifie = cleanJson.replace("},{", "}SPLIT{").replace("}, {", "}SPLIT{");
        String[] blocs = jsonModifie.split("SPLIT");
        
        int compteur = 0;
        for (String bloc : blocs) {
            String id = extraireValeur(bloc, "id");
            String xStr = extraireValeur(bloc, "coord_x");
            String yStr = extraireValeur(bloc, "coord_y");
            
            if (!id.isEmpty() && !xStr.isEmpty() && !yStr.isEmpty()) {
                int x = (int) Double.parseDouble(xStr);
                int y = (int) Double.parseDouble(yStr);
                carte.ajouterPositionSemaphore(id, x, y);
                compteur++;
            }
        }
        System.out.println("   [OK] " + compteur + " sémaphore(s) positionné(s) sur la carte.");
    }

    private static String extraireValeur(String json, String key) {
        int keyIndex = json.lastIndexOf("\"" + key + "\"");
        if (keyIndex == -1) return "";
        int colonIndex = json.indexOf(":", keyIndex);
        if (colonIndex == -1) return "";
        int start = colonIndex + 1;
        while (start < json.length() && (json.charAt(start) == ' ' || json.charAt(start) == '"')) {
            start++;
        }
        int end = start;
        while (end < json.length() && json.charAt(end) != '"' && json.charAt(end) != ',' && json.charAt(end) != '}') {
            end++;
        }
        return json.substring(start, end).trim();
    }
}