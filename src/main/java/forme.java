import java.util.ArrayList;
import java.util.List;

public class forme {

    record FormeList(String id, String nom) {}

    // regarder HashMap pour faire un truc plus propre buchon pour le jalon 2
    public List<FormeList> formes = new ArrayList<>(List.of(
        new FormeList("edaa6453-bec9-4fef-bfb1-e9ecbc6edcdd", "carre"),
        new FormeList("de0dcb56-4379-4434-8401-cc2fc2c9fc92", "carre"),
        new FormeList("3affbbb9-940c-478b-9536-8cf579c32eda", "carre"),
        new FormeList("c58bc953-c2f0-464a-b9f9-400860368c8f", "carre")
    ));
    
    public List<FormeList> getFormes() {
        return formes;
    }

    
}
