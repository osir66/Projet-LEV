import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.ButtonType;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Dialog;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class Simulateur extends Application {

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println("Démarrage du Simulateur de Robots");
        System.out.println("=========================================");
        
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
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
        
        comboBoxNom.setEditable(true); 
        comboBoxNom.getSelectionModel().selectFirst();
        comboBoxNom.setPrefWidth(250);

        VBox vbox = new VBox(10);
        vbox.getChildren().addAll(new Label("Choisissez l'adresse du serveur :"), comboBoxNom);
        dialog.getDialogPane().setContent(vbox);

        dialog.setResultConverter(dialogButton -> {
            if (dialogButton == ButtonType.OK) {
                String choixUtilisateur = comboBoxNom.getValue();
                
                return configurationsServeurs.getOrDefault(choixUtilisateur, choixUtilisateur);
            }
            return null;
        });

        Optional<String> result = dialog.showAndWait();
        
        if (!result.isPresent()) {
            System.out.println("Démarrage annulé.");
            Platform.exit();
            return;
        }

        String urlServeur = result.get();
        System.out.println("-> Connexion établie via l'adresse : " + urlServeur);

        Web clientWeb = new Web(urlServeur);
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
                System.out.println("   [Avertissement] Échec de l'extraction. Utilisation du fallback (15x15).");
            }

            try {
                String reponseSemaphores = clientWeb.requeteGet("/api/list_semaphore");
                chargerSemaphoresServeur(reponseSemaphores, carte);
            } catch (Exception e) {
                System.err.println("   [Erreur Sémaphores] " + e.getMessage());
            }

            System.out.println("-> Récupération des robots depuis le serveur...");
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
            System.err.println("Erreur lors de l'initialisation : " + e.getMessage());
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