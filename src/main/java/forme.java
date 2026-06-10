import java.util.ArrayList;
import java.util.List;

public class forme {

    record FormeList(String id, String nom) {}

    public static final List<FormeList> formes = new ArrayList<>();

    public static List<FormeList> getFormes() {
        return formes;
    }

    public static void charger(Communication1 comm) {
        String json = comm.getListSymboles();
        List<FormeList> result = new ArrayList<>();
        int start = 0;
        while (true) {
            int debut = json.indexOf('{', start);
            int fin   = json.indexOf('}', debut);
            if (debut == -1 || fin == -1) break;
            String obj = json.substring(debut, fin + 1);
            String id  = extraireString(obj, "id");
            String nom = extraireString(obj, "name");
            result.add(new FormeList(id, nom));
            start = fin + 1;
        }
        formes.clear();
        formes.addAll(result);
    }

    private static String extraireString(String obj, String key) {
        String search = "\"" + key + "\":\"";
        int s = obj.indexOf(search);
        if (s == -1) return "";
        s += search.length();
        int e = obj.indexOf('"', s);
        return e == -1 ? "" : obj.substring(s, e);
    }
}
