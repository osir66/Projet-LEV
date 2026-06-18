/**
  Classe de lancement principale.
  Elle permet d'appeler la classe JavaFX (Simulateur) de manière indirecte,
  ce qui évite l'erreur "JavaFX runtime components are missing" si les 
  modules ne sont pas parfaitement configurés dans le chemin d'exécution.
 **/
public class Launcher {
    public static void main(String[] args) {
        Simulateur.main(args);
    }
}