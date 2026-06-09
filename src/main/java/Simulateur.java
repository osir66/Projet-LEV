public class Simulateur {
    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println("Démarrage du Simulateur de Robots");
        System.out.println("=========================================");

        String urlServeur = "http://192.168.1.101:8000";
        int nombreDeRobots = 5;

        Web clientWeb = new Web(urlServeur);
        Carte carte = new Carte();

        for (int i = 1; i <= nombreDeRobots; i++) {
            String robotNom = "R" + i;
            
            Robot robot = new Robot(robotNom, carte.getBaseX(), carte.getBaseY(), carte, clientWeb);
            
            try {
                String urlAddRobot = String.format("/api/add_robot?name=%s&speed=1&position_x=%d&position_y=%d",
                        robotNom, carte.getBaseX(), carte.getBaseY());
                
                String reponseServeur = clientWeb.requetePost(urlAddRobot, "");
                System.out.println("Réponse création " + robotNom + " : " + reponseServeur);
                
                String idGenere = extraireIdDepuisReponse(reponseServeur);
                if (!idGenere.isEmpty()) {
                    robot.setIdServeur(idGenere);
                    System.out.println("-> " + robotNom + " synchronisé sur l'ID serveur : " + idGenere);
                } else {
                    System.out.println("-> Aucun ID détecté, conservation du nom par défaut.");
                }
                
            } catch (Exception e) {
                System.err.println("Impossible d'enregistrer " + robotNom + ". Erreur : " + e.getMessage());
            }

            carte.ajouterRobot(robot);
            Thread t = new Thread(robot);
            t.setName("Thread-" + robotNom);
            t.start();
        }
    }

    private static String extraireIdDepuisReponse(String reponse) {
        if (reponse == null || reponse.isEmpty()) return "";
        reponse = reponse.trim();
        
        if (reponse.contains("\"id\"")) {
            int index = reponse.indexOf("\"id\"");
            int colon = reponse.indexOf(":", index);
            int start = colon + 1;
            while (start < reponse.length() && (reponse.charAt(start) == ' ' || reponse.charAt(start) == '"')) {
                start++;
            }
            int end = start;
            while (end < reponse.length() && Character.isDigit(reponse.charAt(end))) {
                end++;
            }
            return reponse.substring(start, end);
        }
        
        String brut = reponse.replace("\"", "").trim();
        if (!brut.isEmpty() && Character.isDigit(brut.charAt(0))) {
            return brut;
        }
        
        return "";
    }
}