function afficherSucces() {
    var notif = document.getElementById('notification');
    notif.style.display = 'block';
   
    document.getElementById('form-robot').reset();
    document.getElementById('form-semaphore').reset();
    document.getElementById('form-shape').reset();
    document.getElementById('form-config').reset();

    setTimeout(function() {
        notif.style.display = 'none';
    }, 5000);
}