unibo courses downloader
============================

`./main.py panopto cookies.json [folderID]`

TUTORIAL PANOPTO
-----
*   assicurati di essere iscritto al "virtuale" del corso del quale vuoi scaricare le registrazioni.
*   (da, per esempio, il "virtuale" del corso) apri il link nella tab corrente di una registrazione qualsiasi che vuoi scaricare.
*   esporta i cookie in formato json usando questa [estensione open-source](https://github.com/kairi003/Get-cookies.txt-Locally).
*   nella tab corrente del browser, clicca l'icona della cartella in alto a sx (accanto ad essa c'e' il nome del corso).
*   dalla barra degli indirizzi, estrai il valore del campo "folderID" (e.g. se https://unibo.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID="8cea2670-08a2-4f20-a11d-afb200e2910f" => "8cea2670-08a2-4f20-a11d-afb200e2910f" ).
*   hai tutti gli ingredienti per poter eseguire il programma ;)
 
`./main.py virtuale cookies.json [folderID]`

TUTORIAL VIRTUALE
-----
*   assicurati di essere iscritto al "virtuale" del corso dal quale vuoi scaricare le slide.
*   (da, per esempio, il "virtuale" del corso) esporta i cookie in formato json usando questa [estensione open-source](https://github.com/kairi003/Get-cookies.txt-Locally).
*   dalla barra degli indirizzi, estrai il valore del campo "id" (e.g. se https://virtuale.unibo.it/course/view.php?id=39625 => "39625" ).
*   hai tutti gli ingredienti per poter eseguire il programma ;)
