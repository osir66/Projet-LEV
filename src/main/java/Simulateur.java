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
        
        String nomGrille = extraireValeur(jsonConfig, "grille");
        String xStr = extraireValeur(jsonConfig, "nb_x");
        String yStr = extraireValeur(jsonConfig, "nb_y");

        if (!xStr.isEmpty() && !yStr.isEmpty()) {
            int tailleX = (int) Double.parseDouble(xStr);
            int tailleY = (int) Double.parseDouble(yStr);
            String nom = nomGrille.isEmpty() ? "Inconnue" : nomGrille;
            
            carte.setConfiguration(nom, tailleX, tailleY);
            System.out.println(String.format("   [OK] Grille '%s' chargée : %dx%d", nom, tailleX, tailleY));
        } else {
            System.out.println("   [Avertissement] Configuration introuvable, utilisation de la grille par défaut.");
        }

        System.out.println("\n-> Récupération des robots depuis le serveur...");
        String reponseRobots = clientWeb.requeteGet("/api/list_robots");
        List<Robot> robotsDuServeur = parserRobotsServeur(reponseRobots, carte, clientWeb);
        
        if (robotsDuServeur.isEmpty()) {
            System.out.println("Aucun robot trouvé sur le serveur.");
        } else {
            System.out.println("-> Lancement de " + robotsDuServeur.size() + " thread(s) de robot(s) :");
            for (Robot robot : robotsDuServeur) {
                carte.ajouterRobot(robot);
                Thread t = new Thread(robot);
                t.setName("Thread-" + robot.getNom());
                t.setDaemon(true); 
                t.start();
                System.out.println("   [ONLINE] " + robot.getNom() + " démarré.");
            }
        }

        ControleurRobot root = new ControleurRobot(carte);
            
            // Calcul de la taille de la fenêtre globale :
            // Largeur = (Taille de la carte en pixels) + (240 pixels pour le panneau latéral) + (10 pixels de marge de sécurité)
            // Hauteur = (Taille de la carte en pixels) + (40 pixels pour la barre de titre Windows)
            int largeurFenetre = (carte.getLargeurX() * 40) + 250;
            int hauteurFenetre = (carte.getHauteurY() * 40) + 40;
            
            Scene scene = new Scene(root, largeurFenetre, hauteurFenetre);

            primaryStage.setTitle("Superviseur de la Simulation - Configuration : " + carte.getNomGrille());
            primaryStage.setScene(scene);
            
            primaryStage.setOnCloseRequest(event -> {
                System.out.println("Fermeture de l'application...");
                System.exit(0);
            });
            
            primaryStage.show();

    } catch (Exception e) {
        System.err.println("Erreur critique lors de l'initialisation : " + e.getMessage());
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

    private static String extraireValeur(String json, String key) {
        int keyIndex = json.indexOf("\"" + key + "\"");
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