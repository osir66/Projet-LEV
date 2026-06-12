import javafx.application.Platform;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.control.*;
import javafx.geometry.Pos;

public class interfaceCommande extends VBox {
    TextField urlBase;
    TextField port;
    TextField temps;
    TextField equipe;
    TextField nomMission;
    Button btnRechercher;
    Button Envoyer;
    ListView<semaphore> listeSemaphores;
    ToggleGroup groupSemaphores;
    ListView<forme.FormeList> listeFormes;
    ToggleGroup groupFormes;

    public interfaceCommande() {
        this.getStylesheets().add(
                getClass().getResource("/style.css").toExternalForm());
        // Titre
        Label titre = new Label("Panneau de commande de MASSILIA");
        titre.getStyleClass().add("nom_controller");
        // Champ IP et Port
        Label ipeLabel = new Label("IP :");
        urlBase = new TextField("192.168.1.101");
        Label portLabel = new Label("Port :");
        port = new TextField("8000");
        port.setTextFormatter(new TextFormatter<>(change ->
        change.getControlNewText().matches("\\d*") ? change : null
        ));

        btnRechercher = new Button("Rechercher");
        btnRechercher.setOnAction(e -> {
            String ip = urlBase.getText().trim();
            String portVal = port.getText().trim();
            btnRechercher.setDisable(true);
            new Thread(() -> {
                Communication1 comm = new Communication1(ip, portVal);
                semaphore.charger(comm);
                forme.charger(comm);
                Platform.runLater(() -> {
                    listeSemaphores.getItems().setAll(semaphore.getSemaphores());
                    listeFormes.getItems().setAll(forme.getFormes());
                    btnRechercher.setDisable(false);
                });
            }).start();
        });

        HBox recherche = new HBox(ipeLabel, urlBase, portLabel, port, btnRechercher);
        recherche.setSpacing(10);
        recherche.setAlignment(Pos.CENTER);
        recherche.getStyleClass().add("barre_recherche");
        // Nom de mission
        nomMission = new TextField();
        nomMission.getStyleClass().add("nom_mission");
        Label nomMissionLabel = new Label("Nom de la mission :");
        HBox mission = new HBox(nomMissionLabel, nomMission);
        mission.setSpacing(10);
        mission.setAlignment(Pos.CENTER);
        Label tempsLabel = new Label("Temps (s) :");
        // Temps
        temps = new TextField();
        temps.setTextFormatter(new TextFormatter<>(change ->
        change.getControlNewText().matches("\\d*") ? change : null
        ));
        HBox hboxtemps = new HBox(tempsLabel, temps);
        hboxtemps.setAlignment(Pos.CENTER);
        hboxtemps.setSpacing(10);

        // Équipe
        Label equipeLabel = new Label("Équipe :");
        equipe = new TextField("Massilia");
        equipe.setAlignment(Pos.CENTER);
        HBox hboxEquipe = new HBox(equipeLabel, equipe);
        hboxEquipe.setAlignment(Pos.CENTER);
        hboxEquipe.setSpacing(10);
        // Liste sémaphores avec RadioButton
        groupSemaphores = new ToggleGroup();
        listeSemaphores = new ListView<>();
        listeSemaphores.setPrefHeight(150);
        listeSemaphores.setCellFactory(lv -> new ListCell<semaphore>() {
            private final RadioButton rb = new RadioButton();
            {
                rb.setToggleGroup(groupSemaphores);
            }

            @Override
            protected void updateItem(semaphore s, boolean empty) {
                super.updateItem(s, empty);
                if (empty || s == null) {
                    setGraphic(null);
                    return;
                }
                rb.setText(s.getNom());
                rb.setUserData(s);
                setGraphic(rb);
            }
        });

        // Liste formes avec RadioButton
        groupFormes = new ToggleGroup();
        listeFormes = new ListView<>();
        listeFormes.setPrefHeight(150);
        listeFormes.setCellFactory(lv -> new ListCell<forme.FormeList>() {
            private final RadioButton rb = new RadioButton();
            {
                rb.setToggleGroup(groupFormes);
            }

            @Override
            protected void updateItem(forme.FormeList f, boolean empty) {
                super.updateItem(f, empty);
                if (empty || f == null) {
                    setGraphic(null);
                    return;
                }
                rb.setText(f.nom());
                rb.setUserData(f);
                setGraphic(rb);
            }
        });

        // Les deux listes côte à côte
        VBox colonneGauche = new VBox(5, new Label("Sémaphore :"), listeSemaphores);
        VBox colonneDroite = new VBox(5, new Label("Forme :"), listeFormes);
        HBox listes = new HBox(20, colonneGauche, colonneDroite);
        listes.setAlignment(Pos.CENTER);

        // Bouton Envoyer
        Envoyer = new Button("Envoyer");
        HBox hboxEnvoyer = new HBox(Envoyer);
        hboxEnvoyer.setAlignment(Pos.CENTER);
        Envoyer.setOnAction(e -> {
            Toggle toggleSem = groupSemaphores.getSelectedToggle();
            Toggle toggleForme = groupFormes.getSelectedToggle();
            if (toggleSem == null || toggleForme == null) {
                System.out.println("Sélectionnez un sémaphore et une forme.");
                return;
            }
            semaphore semSelect = (semaphore) toggleSem.getUserData();
            forme.FormeList formeSelect = (forme.FormeList) toggleForme.getUserData();

            String ip = urlBase.getText().trim();
            String portVal = port.getText().trim();

            new Thread(() -> {
                try {
                    new Communication1(ip, portVal).envoieMission(
                            nomMission.getText().trim(),
                            semSelect.getSemaphore_id(),
                            Integer.parseInt(temps.getText().isEmpty() ? "0" : temps.getText()),
                            equipe.getText().trim(),
                            formeSelect.id()
                    );
                } catch (Exception ex) {
                    System.out.println("Erreur : " + ex.toString());
                }
            }).start();
        });

        
        this.getChildren().addAll(
                titre,
                recherche,
                mission,
                listes,
                hboxtemps,
                hboxEquipe,
                hboxEnvoyer
        );
        this.setSpacing(10);
    }
}