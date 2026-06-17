import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

public class listeMissions extends VBox {

    private final TextField urlBase;
    private final TextField port;
    private final TextField equipe;
    private final ListView<String> listView;

    public listeMissions() {
        this.getStylesheets().add(
                getClass().getResource("/style.css").toExternalForm());

        // Titre
        Label titre = new Label("Liste des missions");
        titre.getStyleClass().add("nom_controller");

        // IP / Port
        Label ipLabel = new Label("IP :");
        urlBase = new TextField("192.168.1.101");
        Label portLabel = new Label("Port :");
        port = new TextField("8000");
        port.setTextFormatter(new TextFormatter<>(change ->
                change.getControlNewText().matches("\\d*") ? change : null));

        // Équipe
        Label equipeLabel = new Label("Équipe :");
        equipe = new TextField("Massilia");

        Button btnActualiser = new Button("Actualiser");

        HBox barreHaut = new HBox(10, ipLabel, urlBase, portLabel, port, equipeLabel, equipe, btnActualiser);
        barreHaut.setAlignment(Pos.CENTER);

        // Liste
        listView = new ListView<>();
        listView.setStyle("-fx-font-family: 'Courier New'; -fx-font-size: 12px;");

        btnActualiser.setOnAction(e -> actualiser());

        this.getChildren().addAll(titre, barreHaut, listView);
        this.setSpacing(10);
    }

    private void actualiser() {
        String ip = urlBase.getText().trim();
        String portVal = port.getText().trim();
        String team = equipe.getText().trim();

        Communication1 comm = new Communication1(ip, portVal);
        String json = comm.getMissionsByTeam(team);
        listView.getItems().setAll(parseJson(json));
    }

    // Parse simplifié : extrait name + state de chaque objet JSON
    private java.util.List<String> parseJson(String json) {
        java.util.List<String> result = new java.util.ArrayList<>();
        if (json == null || json.isBlank() || json.equals("[]")) {
            result.add("Aucune mission.");
            return result;
        }
        String[] blocs = json.replace("[", "").replace("]", "")
                             .replace("},{", "}SPLIT{").split("SPLIT");
        for (String bloc : blocs) {
            String name  = extraire(bloc, "name");
            String state = extraire(bloc, "state");
            result.add(String.format("[%s] %s",
                    state.isEmpty() ? "?" : state,
                    name.isEmpty()  ? "(sans nom)" : name));
        }
        return result;
    }

    private String extraire(String json, String key) {
        int idx = json.indexOf("\"" + key + "\"");
        if (idx == -1) return "";
        int colon = json.indexOf(":", idx);
        if (colon == -1) return "";
        int start = colon + 1;
        while (start < json.length() && (json.charAt(start) == ' ' || json.charAt(start) == '"')) start++;
        int end = start;
        while (end < json.length() && json.charAt(end) != '"' && json.charAt(end) != ',' && json.charAt(end) != '}') end++;
        return json.substring(start, end).trim();
    }
}
