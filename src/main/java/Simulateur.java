import java.util.ArrayList;
import java.util.List;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

// Application principale.
public class Simulateur extends Application {

    private static final String URL_SERVEUR = "http://192.168.1.22:8000";

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println("Démarrage du Simulateur de Robots");
        System.out.println("=========================================");
        
        launch(args); // Méthode de JavaFX qui prépare l'environnement puis appelle start()
    }

    /**
    Méthode appelée automatiquement par launch().
    Construit l'interface graphique et lance la logique.
    **/
    @Override
<<<<<<< Updated upstream
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
=======
    public void start(Stage primaryStage) {
        // Boîte de dialogue pour la connexion
        
        // Dictionnaire reliant des noms aux adresses IP
        Map<String, String> configurationsServeurs = new HashMap<>();
        configurationsServeurs.put("Massilia (http://192.168.1.22:8000)", "http://192.168.1.22:8000");
        configurationsServeurs.put("Les K-talents (http://192.168.1.14:8000)", "http://192.168.1.14:8000");
        configurationsServeurs.put("Comment Bien Manger Une Tourte ? (http://192.168.1.24:8000)", "http://192.168.1.24:8000");
        configurationsServeurs.put("Lux sky Trooper (http://192.168.1.96:8000)", "http://192.168.1.96:8000");

        Dialog<String> dialog = new Dialog<>();
        dialog.setTitle("Configuration du Serveur");
        dialog.setHeaderText("Connexion au serveur de simulation");
        dialog.getDialogPane().getButtonTypes().addAll(ButtonType.OK, ButtonType.CANCEL);

        ComboBox<String> comboBoxNom = new ComboBox<>();
        comboBoxNom.getItems().addAll(configurationsServeurs.keySet());
        
        // Editable permet à l'utilisateur de taper manuellement une IP non répertoriée
        comboBoxNom.setEditable(true); 
        comboBoxNom.getSelectionModel().selectFirst(); 
        comboBoxNom.setPrefWidth(250);

        VBox vbox = new VBox(10);
        vbox.getChildren().addAll(new Label("Choisissez un profil de serveur :"), comboBoxNom);
        dialog.getDialogPane().setContent(vbox);

        // Convertit le clic sur le bouton OK en la valeur contenue dans la ComboBox
        dialog.setResultConverter(dialogButton -> {
            if (dialogButton == ButtonType.OK) {
                String choixUtilisateur = comboBoxNom.getValue();
                // Récupère l'URL si elle est dans la Map, sinon utilise le texte brut saisi (Fallback)
                return configurationsServeurs.getOrDefault(choixUtilisateur, choixUtilisateur);
            }
            return null;
        });

        // Bloque le thread graphique tant que l'utilisateur n'a pas répondu
        Optional<String> result = dialog.showAndWait();
        
        if (!result.isPresent()) {
            System.out.println("Démarrage annulé.");
            Platform.exit(); // Arrête l'application
            return;
        }

        // Initialisation de la simulation
        String urlServeur = result.get();
        System.out.println("-> Connexion établie via l'adresse : " + urlServeur);

        Web clientWeb = new Web(urlServeur);
        Carte carte = new Carte();

        try {
            // Récupération de la taille de la carte
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
                System.out.println("   [Avertissement] Échec d'extraction. Utilisation du fallback par défaut (15x15).");
            }

            // Récupération des positions des sémaphores
            try {
                String reponseSemaphores = clientWeb.requeteGet("/api/list_semaphore");
                chargerSemaphoresServeur(reponseSemaphores, carte);
            } catch (Exception e) {
                System.err.println("   [Erreur Sémaphores] " + e.getMessage());
            }

            // Récupération et lancement des robots
            System.out.println("\n-> Récupération des robots depuis le serveur...");
            String reponseRobots = clientWeb.requeteGet("/api/list_robots");
            List<Robot> robotsDuServeur = parserRobotsServeur(reponseRobots, carte, clientWeb);
            
            for (Robot r : robotsDuServeur) {
                carte.ajouterRobot(r);
                new Thread(r).start(); // Lancement du Thread individuel pour chaque robot
            }

            // Création et affichage de la fenêtre
            ControleurRobot controleur = new ControleurRobot(carte);
            Scene scene = new Scene(controleur);

            primaryStage.setTitle("Simulateur de Robots - Grille : " + carte.getNomGrille());
            primaryStage.setScene(scene);
            
            primaryStage.sizeToScene(); // Ajuste la fenêtre pour correspondre au contenu
            primaryStage.show();
            primaryStage.setResizable(false); // Empêche l'utilisateur de changer l'affichage en redimensionnant

        } catch (Exception e) {
            System.err.println("Erreur fatale lors de l'initialisation : " + e.getMessage());
            e.printStackTrace();
        }
>>>>>>> Stashed changes
    }

    // Analyse le JSON contenant les robots et crée les objets Robot correspondants.
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

<<<<<<< Updated upstream
=======
    // Analyse le JSON des sémaphores et enregistre leurs coordonnées dans la carte.
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

    // Méthode utilitaire maison pour extraire la valeur d'une clé dans un format JSON simple.
>>>>>>> Stashed changes
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