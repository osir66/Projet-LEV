import java.util.ArrayList;
import java.util.List;

public class Simulateur {
    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println("Démarrage du Simulateur de Robots");
        System.out.println("=========================================");

        String urlServeur = "http://192.168.1.101:8000";
        Web clientWeb = new Web(urlServeur);
        Carte carte = new Carte();

        try {
            System.out.println("-> Récupération des robots depuis le serveur...");
            String reponseRobots = clientWeb.requeteGet("/api/list_robots");
            
            List<Robot> robotsDuServeur = parserRobotsServeur(reponseRobots, carte, clientWeb);
            
            if (robotsDuServeur.isEmpty()) {
                System.out.println("Aucun robot trouvé sur le serveur.");
                return;
            }

            System.out.println("-> Lancement de " + robotsDuServeur.size() + " thread(s) de robot(s) :");
            for (Robot robot : robotsDuServeur) {
                carte.ajouterRobot(robot);
                
                Thread t = new Thread(robot);
                t.setName("Thread-" + robot.getNom());
                t.start();
                
                System.out.println("   [ONLINE] " + robot.getNom() + " (ID: " + robot.getNom() + ") démarré.");
            }

        } catch (Exception e) {
            System.err.println("Erreur lors de l'initialisation du simulateur : " + e.getMessage());
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
                int startX = xStr.isEmpty() ? carte.getBaseX() : Integer.parseInt(xStr);
                int startY = yStr.isEmpty() ? carte.getBaseY() : Integer.parseInt(yStr);
                
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