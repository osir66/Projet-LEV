import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.scene.control.*;
import java.util.List;
import java.util.ArrayList;

public class interfaceCommance extends VBox {

    TextField urlBase;
    Button btnRechercher;
    ListView<String> historique;
    ListView<String> listeSemaphoresUI;
    semaphore semaphores = new semaphore();
    List<semaphore.Semaphore> listSemaphores = new ArrayList<>(semaphores.getSemaphores());

    public interfaceCommance() {


        listeSemaphoresUI = new ListView<>();
        for (semaphore.Semaphore s : listSemaphores) {
            listeSemaphoresUI.getItems().add(" | état=" + s.etat() + " | nom=" + s.nom());
        }

        this.getChildren().addAll( new Label("Sémaphores :"), listeSemaphoresUI);
        this.setSpacing(10);
    }
}
