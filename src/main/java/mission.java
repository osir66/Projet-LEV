import javafx.application.Platform;
import java.net.http.*;
import java.util.*;

public class mission {
    private String shape_id;
    private String nom;
    private String ip;
    private String semaphore_id;
    private String team;
    private String time;
    private String port;

    public mission(String shape_id, String nom, String ip, String semaphore_id , String time, String port) {
        this.shape_id = shape_id;
        this.nom = nom;
        this.ip = ip;
        this.semaphore_id = semaphore_id;
        this.team = "Massilia";
        this.time = time;
        this.port = port;
    }

    public String getShape_id() {
        return shape_id;
    }
    public String getNom() {
            return nom;
        }
    public String getIp() {
        return ip;
    }
    public String getSemaphore_id() {
        return semaphore_id;
    }
    public String getTeam() {
        return team;
    }
    public String getTime() {
        return time;
    }
    public void setShape_id(String shape_id) {
        this.shape_id = shape_id;
    }
    public void setNom(String nom) {
        this.nom = nom;
    }
    public void setIp(String ip) {
        this.ip = ip;
    }
    public void setPort(String port) {
        this.port = port;
    }

    public void sendMission() {
        new Communication1(ip, port).envoieMission(shape_id, nom, Integer.parseInt(time), team, semaphore_id);
    }
}
