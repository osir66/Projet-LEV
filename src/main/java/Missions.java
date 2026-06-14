public class Missions {
    private String idMission;
    private String idSemaphore;
    private String symbole;
    private boolean termine;
    private int cibleX, cibleY;
    private String dateDebut;
    
    private String statut; 

    public Missions(String idMission, String idSemaphore, String symbole, int cibleX, int cibleY) {
        this.idMission = idMission;
        this.idSemaphore = idSemaphore;
        this.symbole = symbole;
        this.cibleX = cibleX;
        this.cibleY = cibleY;
        this.termine = false;
        this.statut = "Awaiting";
    }

    public String getIdMission() {
        return idMission;
    }

    public String getIdSemaphore() {
        return idSemaphore;
    }

    public String getSymbole() {
        return symbole;
    }

    public int getCibleX() { 
        return cibleX; 
    }

    public int getCibleY() { 
        return cibleY; 
    }

    public boolean isTermine() {
        return termine;
    }

    public String getDateDebut() { 
        return dateDebut;
    }
    
    public void setDateDebut(String dateDebut) {
        this.dateDebut = dateDebut;
    }

    public void setTermine(boolean termine) { 
        this.termine = termine; 
    }

    public String getStatut() {
        return this.statut;
    }

    public void setStatut(String statut) {
        this.statut = statut;
    }
}