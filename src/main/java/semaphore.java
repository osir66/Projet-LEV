import java.util.ArrayList;
import java.util.List;

public class semaphore {
    public String semaphore_id;
    public String state;
    public String nom;
    public int duration;
    public String type;

    public semaphore(String semaphore_id, String state, String nom, int duration, String type) {
        this.semaphore_id = semaphore_id;
        this.state = state;
        this.nom = nom;
        this.duration = duration;
        this.type = type;
    }

    public static final List<semaphore> semaphores = new ArrayList<>();

    public static List<semaphore> getSemaphores() {
        return semaphores;
    }

    public static void charger(Communication1 comm) {
        String json = comm.getListSemaphores();
        List<semaphore> result = new ArrayList<>();
        int start = 0;
        while (true) {
            int debut = json.indexOf('{', start);
            int fin   = json.indexOf('}', debut);
            if (debut == -1 || fin == -1) break;
            String obj = json.substring(debut, fin + 1);
            String id       = extraireString(obj, "id");
            String nom      = extraireString(obj, "name");
            String state    = extraireString(obj, "state");
            int    duration = extraireInt(obj, "duration");
            String type     = extraireString(obj, "type");
            result.add(new semaphore(id, state, nom, duration, type));
            start = fin + 1;
        }
        semaphores.clear();
        semaphores.addAll(result);
    }

    private static String extraireString(String obj, String key) {
        String search = "\"" + key + "\":\"";
        int s = obj.indexOf(search);
        if (s == -1) return "";
        s += search.length();
        int e = obj.indexOf('"', s);
        return e == -1 ? "" : obj.substring(s, e);
    }

    private static int extraireInt(String obj, String key) {
        String search = "\"" + key + "\":";
        int s = obj.indexOf(search);
        if (s == -1) return 0;
        s += search.length();
        int e = s;
        while (e < obj.length() && Character.isDigit(obj.charAt(e))) e++;
        try { return Integer.parseInt(obj.substring(s, e)); } catch (Exception ex) { return 0; }
    }

    public String getSemaphore_id() { 
        return semaphore_id; }
    public String getState()        { 
        return state; }
    public String getNom()          { 
        return nom; }
    public int    getDuration()     { 
        return duration; }
    public String getType()         { 
        return type; }
}