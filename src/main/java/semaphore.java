import javafx.scene.layout.VBox;
import java.util.ArrayList;
import java.util.List;

public class semaphore extends VBox {

    record Semaphore(String id, int etat, String forme, double matrice, String nom) {}

    public List<Semaphore> semaphores = new ArrayList<>(List.of(
        new Semaphore("edaa6453-bec9-4fef-bfb1-e9ecbc6edcdd", 1, "carre", 1.2, "Nom1"),
        new Semaphore("de0dcb56-4379-4434-8401-cc2fc2c9fc92", 1, "carre", 1.2, "Nom2"),
        new Semaphore("3affbbb9-940c-478b-9536-8cf579c32eda", 1, "carre", 1.2, "Nom3"),
        new Semaphore("c58bc953-c2f0-464a-b9f9-400860368c8f", 1, "carre", 1.2, "Nom4")
    ));

    public List<Semaphore> getSemaphores() {
        return semaphores;
    }
}
