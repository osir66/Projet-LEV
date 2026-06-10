import javafx.animation.*;
import javafx.application.Platform;
import javafx.geometry.*;
import javafx.scene.Node;
import javafx.scene.canvas.*;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.util.Duration;
import java.util.Random;

public class interfaceCommande extends StackPane {

    // ---- Champs UI ----
    TextField           urlBase;
    TextField           port;
    TextField           equipe;
    TextField           nomMission;
    Spinner<Integer>    tempsSpinner;
    Button              btnRechercher;
    Button              Envoyer;
    ComboBox<semaphore>       comboSemaphores;
    ComboBox<forme.FormeList> comboFormes;
    Label               terminal;
    boolean             transmissionEnCours = false;

    // ---- Overlay rain ----
    private StackPane      overlayPane;
    private Canvas         rainCanvas;
    private VBox           skullBox;
    private AnimationTimer rainTimer;
    private int[]          cols;
    private boolean        skullVisible = false;

    private static final Random RAND  = new Random();
    private static final String CHARS =
        "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン" +
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*<>?/|{}";

    private static final String SKULL_ART =
        "      ░▒▓████████████▓▒░\n" +
        "    ░▒▓██░░░░░░░░░░░░██▓▒░\n" +
        "   ░▒██░░░░░░░░░░░░░░░░██▒░\n" +
        "  ░▒██░░░▄████▄ ▄████▄░░░██▒░\n" +
        "  ░▒██░░░██████ ░██████░░░██▒░\n" +
        "  ░▒██░░░▀████▀ ░▀████▀░░░██▒░\n" +
        "  ░▒██░░░░░░░░ ▲ ░░░░░░░░░██▒░\n" +
        "   ░▒██░░░░░╰─────╯░░░░░██▒░\n" +
        "    ░▒▓██░░░░░░░░░░░░░██▓▒░\n" +
        "      ░▒▓████████████▓▒░\n" +
        "        ▓██░░░░░░░░██▓\n" +
        "      ▓████░░░░░░████▓\n" +
        "     ▓██░░████████░░██▓\n" +
        "      ▀▀▀▀▀▀░░░░▀▀▀▀▀▀";

    public interfaceCommande() {

        this.getStylesheets().add(
            getClass().getResource("style.css").toExternalForm());

        // ============================================================
        // OVERLAY — canvas rain + skull (couche haute)
        // ============================================================
        rainCanvas = new Canvas();

        Label skullLabel = new Label(SKULL_ART);
        skullLabel.getStyleClass().add("skull-art");

        Label skullMessage = new Label("Envoi de la requête ultra-confidentielle sécurisé");
        skullMessage.getStyleClass().add("skull-message");

        Label skullCloseHint = new Label("[ CLIQUER POUR FERMER ]");
        skullCloseHint.getStyleClass().add("skull-close-hint");

        skullBox = new VBox(24, skullLabel, skullMessage, skullCloseHint);
        skullBox.setAlignment(Pos.CENTER);
        skullBox.setVisible(false);

        overlayPane = new StackPane(rainCanvas, skullBox);
        overlayPane.setVisible(false);
        overlayPane.setOnMouseClicked(e -> closeOverlay());

        rainCanvas.widthProperty().bind(overlayPane.widthProperty());
        rainCanvas.heightProperty().bind(overlayPane.heightProperty());

        // ============================================================
        // CONTENU PRINCIPAL (couche basse — l'ancien VBox)
        // ============================================================
        VBox contenu = new VBox();
        contenu.getStyleClass().add("panneau-principal");

        // ============================================================
        // BARRE DE SIGNAL animée
        // ============================================================
        HBox signalBar = new HBox(5);
        signalBar.setAlignment(Pos.CENTER_LEFT);
        for (int i = 0; i < 14; i++) {
            Region block = new Region();
            block.getStyleClass().add("signal-block");
            block.setPrefSize(20, 5);
            FadeTransition ft = new FadeTransition(Duration.millis(350 + i * 100), block);
            ft.setFromValue(0.1);
            ft.setToValue(1.0);
            ft.setAutoReverse(true);
            ft.setCycleCount(Animation.INDEFINITE);
            ft.setDelay(Duration.millis(i * 80));
            ft.play();
            signalBar.getChildren().add(block);
        }

        // ============================================================
        // EN-TÊTE avec shimmer
        // ============================================================
        Label titre = new Label("NEXUS // C2");
        titre.getStyleClass().add("titre-nexus");

        Label sousTitre = new Label("SYSTÈME DE COMMANDEMENT TACTIQUE  ·  NIVEAU 5");
        sousTitre.getStyleClass().add("sous-titre-nexus");

        VBox entete = new VBox(4, titre, sousTitre);
        entete.setAlignment(Pos.CENTER);
        entete.getStyleClass().add("entete");

        Timeline shimmer = new Timeline(
            new KeyFrame(Duration.ZERO,
                e -> titre.setStyle("-fx-text-fill:#00f5ff; -fx-effect:dropshadow(gaussian,#00f5ff,22,0.6,0,0);")),
            new KeyFrame(Duration.millis(900),
                e -> titre.setStyle("-fx-text-fill:#a040ff; -fx-effect:dropshadow(gaussian,#a040ff,22,0.6,0,0);")),
            new KeyFrame(Duration.millis(1800),
                e -> titre.setStyle("-fx-text-fill:#ff00ff; -fx-effect:dropshadow(gaussian,#ff00ff,22,0.6,0,0);")),
            new KeyFrame(Duration.millis(2700),
                e -> titre.setStyle("-fx-text-fill:#a040ff; -fx-effect:dropshadow(gaussian,#a040ff,22,0.6,0,0);")),
            new KeyFrame(Duration.millis(3600),
                e -> titre.setStyle("-fx-text-fill:#00f5ff; -fx-effect:dropshadow(gaussian,#00f5ff,22,0.6,0,0);"))
        );
        shimmer.setCycleCount(Timeline.INDEFINITE);
        shimmer.play();

        // ============================================================
        // PANEL — LIAISON RADIO
        // ============================================================
        urlBase = new TextField("192.168.1.101");
        port = new TextField("8000");
        port.setMaxWidth(100);
        port.setTextFormatter(new TextFormatter<>(c ->
            c.getControlNewText().matches("\\d*") ? c : null));

        btnRechercher = new Button("◈  ÉTABLIR LA LIAISON");
        btnRechercher.getStyleClass().add("btn-liaison");
        btnRechercher.setMaxWidth(Double.MAX_VALUE);

        VBox panelLiaison = panel("☰  LIAISON RADIO",
            ligne("ADRESSE IP", urlBase),
            ligne("PORT",       port),
            btnRechercher);

        // ============================================================
        // PANEL — DÉSIGNATION DE LA CIBLE
        // ============================================================
        comboSemaphores = new ComboBox<>();
        comboSemaphores.setPromptText("Sélectionner…");
        comboSemaphores.setMaxWidth(Double.MAX_VALUE);
        comboSemaphores.setCellFactory(lv -> new ListCell<semaphore>() {
            @Override protected void updateItem(semaphore s, boolean empty) {
                super.updateItem(s, empty);
                setText(empty || s == null ? null : "▸  " + s.getNom());
            }
        });
        comboSemaphores.setButtonCell(new ListCell<semaphore>() {
            @Override protected void updateItem(semaphore s, boolean empty) {
                super.updateItem(s, empty);
                setText(empty || s == null ? null : s.getNom());
            }
        });

        comboFormes = new ComboBox<>();
        comboFormes.setPromptText("Sélectionner…");
        comboFormes.setMaxWidth(Double.MAX_VALUE);
        comboFormes.setCellFactory(lv -> new ListCell<forme.FormeList>() {
            @Override protected void updateItem(forme.FormeList f, boolean empty) {
                super.updateItem(f, empty);
                setText(empty || f == null ? null : "▸  " + f.nom());
            }
        });
        comboFormes.setButtonCell(new ListCell<forme.FormeList>() {
            @Override protected void updateItem(forme.FormeList f, boolean empty) {
                super.updateItem(f, empty);
                setText(empty || f == null ? null : f.nom());
            }
        });

        VBox panelCible = panel("◎  DÉSIGNATION DE LA CIBLE",
            ligne("SÉMAPHORE", comboSemaphores),
            ligne("FORME",     comboFormes));

        // ============================================================
        // PANEL — ORDRE DE MISSION
        // ============================================================
        nomMission = new TextField();
        nomMission.setPromptText("CODE OPÉRATION…");

        equipe = new TextField("Massilia");

        tempsSpinner = new Spinner<>(0, 9999, 30, 5);
        tempsSpinner.setEditable(true);
        tempsSpinner.setMaxWidth(120);

        VBox panelMission = panel("⚑  ORDRE DE MISSION",
            ligne("MISSION",   nomMission),
            ligne("ÉQUIPE",    equipe),
            ligne("TEMPS (s)", tempsSpinner));

        // ============================================================
        // GRILLE CENTRALE  (Liaison | Cible) / Mission
        // ============================================================
        GridPane grid = new GridPane();
        grid.setHgap(14);
        grid.setVgap(14);

        ColumnConstraints col0 = new ColumnConstraints();
        col0.setPercentWidth(42);
        col0.setHgrow(Priority.ALWAYS);
        ColumnConstraints col1 = new ColumnConstraints();
        col1.setPercentWidth(58);
        col1.setHgrow(Priority.ALWAYS);
        grid.getColumnConstraints().addAll(col0, col1);

        RowConstraints row0 = new RowConstraints();
        row0.setVgrow(Priority.ALWAYS);
        RowConstraints row1 = new RowConstraints();
        row1.setVgrow(Priority.ALWAYS);
        grid.getRowConstraints().addAll(row0, row1);

        GridPane.setHgrow(panelLiaison, Priority.ALWAYS);
        GridPane.setHgrow(panelCible,   Priority.ALWAYS);
        GridPane.setHgrow(panelMission, Priority.ALWAYS);
        GridPane.setVgrow(panelLiaison, Priority.ALWAYS);
        GridPane.setVgrow(panelCible,   Priority.ALWAYS);
        GridPane.setVgrow(panelMission, Priority.ALWAYS);

        grid.add(panelLiaison, 0, 0);
        grid.add(panelCible,   1, 0);
        grid.add(panelMission, 0, 1, 2, 1);
        VBox.setVgrow(grid, Priority.ALWAYS);

        // ============================================================
        // BOUTON TRANSMETTRE
        // ============================================================
        Envoyer = new Button("➤  TRANSMETTRE L'ORDRE");
        Envoyer.getStyleClass().add("btn-transmettre");
        Envoyer.setMaxWidth(Double.MAX_VALUE);

        ScaleTransition pulse = new ScaleTransition(Duration.millis(1100), Envoyer);
        pulse.setFromX(1.0); pulse.setFromY(1.0);
        pulse.setToX(1.02);  pulse.setToY(1.02);
        pulse.setAutoReverse(true);
        pulse.setCycleCount(Animation.INDEFINITE);
        pulse.play();

        // ============================================================
        // TERMINAL LOG
        // ============================================================
        terminal = new Label("> SYSTÈME PRÊT — EN ATTENTE D'ORDRES…");
        terminal.getStyleClass().add("terminal-log");
        terminal.setMaxWidth(Double.MAX_VALUE);
        terminal.setAlignment(Pos.CENTER_LEFT);
        terminal.setWrapText(true);

        // ============================================================
        // ACTIONS
        // ============================================================
        btnRechercher.setOnAction(e -> {
            String ip      = urlBase.getText().trim();
            String portVal = port.getText().trim();
            btnRechercher.setDisable(true);
            termLog("> BALAYAGE DU RÉSEAU EN COURS…", null);
            new Thread(() -> {
                try {
                    Communication1 comm = new Communication1(ip, portVal);
                    semaphore.charger(comm);
                    forme.charger(comm);
                    Platform.runLater(() -> {
                        comboSemaphores.getItems().setAll(semaphore.getSemaphores());
                        comboFormes.getItems().setAll(forme.getFormes());
                        btnRechercher.setDisable(false);
                        termLog("> LIAISON ÉTABLIE — "
                            + comboSemaphores.getItems().size()
                            + " SÉMAPHORE(S) DÉTECTÉ(S)", "ok");
                    });
                } catch (Exception ex) {
                    Platform.runLater(() -> {
                        btnRechercher.setDisable(false);
                        termLog("> ÉCHEC DE LIAISON : " + ex.toString(), "err");
                    });
                }
            }).start();
        });

        Envoyer.setOnAction(e -> {
            semaphore       semSelect   = comboSemaphores.getValue();
            forme.FormeList formeSelect = comboFormes.getValue();
            if (semSelect == null || formeSelect == null) {
                termLog("> ⚠ SÉLECTIONNEZ UN SÉMAPHORE ET UNE FORME", "err");
                return;
            }
            if (transmissionEnCours) return;
            transmissionEnCours = true;

            lancerRideau(); // overlay AVANT la logique réseau

            Envoyer.setDisable(true);
            pulse.stop();

            String ip      = urlBase.getText().trim();
            String portVal = port.getText().trim();
            try { tempsSpinner.commitValue(); } catch (Exception ignored) {}
            int    tempsVal  = tempsSpinner.getValue();
            String mission   = nomMission.getText().trim();
            String equipeVal = equipe.getText().trim();
            String semId     = semSelect.getSemaphore_id();
            String nomSem    = semSelect.getNom();
            String formeId   = formeSelect.id();

            String[] msgs = {
                "> [CHIFFREMENT AES-256]  Chiffrement de la transmission…",
                "> [ROUTAGE TOR]          Établissement du tunnel sécurisé…",
                "> [TRANSMISSION]         Envoi de l'ordre à « " + nomSem + " »…",
                "> [CONFIRMATION]         ✓ MISSION TRANSMISE AVEC SUCCÈS"
            };

            Timeline anim = new Timeline();
            for (int i = 0; i < msgs.length; i++) {
                final String msg   = msgs[i];
                final boolean last = (i == msgs.length - 1);
                anim.getKeyFrames().add(
                    new KeyFrame(Duration.millis(700L * (i + 1)),
                        ev -> termLog(msg, last ? "ok" : null)));
            }
            anim.setOnFinished(ev -> new Thread(() -> {
                try {
                    new Communication1(ip, portVal)
                        .envoieMission(mission, semId, tempsVal, equipeVal, formeId);
                } catch (Exception ex) {
                    Platform.runLater(() ->
                        termLog("> ✖ ERREUR RÉSEAU : " + ex.toString(), "err"));
                }
                Platform.runLater(() -> {
                    Envoyer.setDisable(false);
                    transmissionEnCours = false;
                    pulse.play();
                });
            }).start());
            anim.play();
        });

        // ============================================================
        // ASSEMBLAGE
        // ============================================================
        contenu.setSpacing(14);
        contenu.setPadding(new Insets(20));
        contenu.getChildren().addAll(signalBar, entete, grid, Envoyer, terminal);

        this.getChildren().addAll(contenu, overlayPane);
    }

    // ================================================================
    // Rain Overlay
    // ================================================================

    private void lancerRideau() {
        cols         = null;
        skullVisible = false;
        skullBox.setVisible(false);
        overlayPane.setOpacity(0);
        overlayPane.setVisible(true);

        FadeTransition ftIn = new FadeTransition(Duration.millis(300), overlayPane);
        ftIn.setFromValue(0);
        ftIn.setToValue(1);
        ftIn.play();

        rainTimer = new AnimationTimer() {
            private long lastNano = 0;
            @Override public void handle(long now) {
                if (now - lastNano < 45_000_000L) return; // ~22 fps
                lastNano = now;
                dessinePluie();
            }
        };
        rainTimer.start();

        PauseTransition pause = new PauseTransition(Duration.seconds(3.5));
        pause.setOnFinished(e -> revealSkull());
        pause.play();
    }

    private void revealSkull() {
        skullVisible = true;
        skullBox.setOpacity(0);
        skullBox.setVisible(true);
        FadeTransition ft = new FadeTransition(Duration.millis(700), skullBox);
        ft.setFromValue(0);
        ft.setToValue(1);
        ft.play();
    }

    private void closeOverlay() {
        if (rainTimer != null) {
            rainTimer.stop();
            rainTimer = null;
        }
        FadeTransition ftOut = new FadeTransition(Duration.millis(400), overlayPane);
        ftOut.setFromValue(overlayPane.getOpacity());
        ftOut.setToValue(0);
        ftOut.setOnFinished(e -> {
            overlayPane.setVisible(false);
            skullBox.setVisible(false);
            skullVisible = false;
            cols = null;
        });
        ftOut.play();
    }

    private void dessinePluie() {
        GraphicsContext gc = rainCanvas.getGraphicsContext2D();
        double w = rainCanvas.getWidth();
        double h = rainCanvas.getHeight();
        if (w <= 0 || h <= 0) return;

        if (cols == null) {
            int n = Math.max(1, (int)(w / 16) + 1);
            cols = new int[n];
            for (int i = 0; i < n; i++) {
                cols[i] = -(int)(RAND.nextFloat() * h);
            }
        }

        // Overlay semi-transparent : plus opaque quand le skull est visible
        gc.setFill(Color.rgb(3, 0, 15, skullVisible ? 0.22 : 0.13));
        gc.fillRect(0, 0, w, h);

        gc.setFont(Font.font("Consolas", 14));

        for (int i = 0; i < cols.length; i++) {
            int x  = i * 16;
            int hy = cols[i];

            // Trail — 12 caractères cyan avec alpha décroissant
            for (int t = 12; t >= 1; t--) {
                int ty = hy - t * 16;
                if (ty < 0 || ty > h) continue;
                double alpha = ((12.0 - t + 1.0) / 13.0) * 0.75;
                gc.setFill(Color.color(0.0, 245.0 / 255, 1.0, alpha));
                gc.fillText(randomChar(), x, ty);
            }

            // Tête — blanc ou magenta (20 % de chance)
            if (hy >= 0 && hy <= h + 16) {
                gc.setFill(RAND.nextFloat() < 0.2f ? Color.web("#ff00ff") : Color.WHITE);
                gc.fillText(randomChar(), x, hy);
            }

            cols[i] += 16;
            if (cols[i] > h + 12 * 16) {
                cols[i] = -(int)(RAND.nextFloat() * 300);
            }
        }
    }

    private String randomChar() {
        return String.valueOf(CHARS.charAt(RAND.nextInt(CHARS.length())));
    }

    // ================================================================
    // Helpers UI
    // ================================================================

    private VBox panel(String titre, Node... nodes) {
        Label titreLabel = new Label(titre);
        titreLabel.getStyleClass().add("panel-titre");
        titreLabel.setMaxWidth(Double.MAX_VALUE);
        VBox box = new VBox(10, titreLabel);
        box.getStyleClass().add("panel-cyber");
        box.getChildren().addAll(nodes);
        return box;
    }

    private HBox ligne(String labelTxt, Node champ) {
        Label lib = new Label(labelTxt);
        lib.getStyleClass().add("libelle");
        lib.setMinWidth(90);
        HBox.setHgrow(champ, Priority.ALWAYS);
        HBox row = new HBox(10, lib, champ);
        row.setAlignment(Pos.CENTER_LEFT);
        return row;
    }

    private void termLog(String msg, String state) {
        terminal.setText(msg);
        terminal.getStyleClass().removeAll("terminal-log-ok", "terminal-log-err");
        if ("ok".equals(state))  terminal.getStyleClass().add("terminal-log-ok");
        if ("err".equals(state)) terminal.getStyleClass().add("terminal-log-err");
    }
}
