in DataIngestor am parsa csv fie-ul si mi-am facut o lista de dictionare pentru fiecare coloana din tabel. in task_runner imi fac o lista de thread-uri pe care le pornesc si o coada de job-uri pentru job-urile care urmeaza sa vina de la server. De asemenea, folosesc lock si event pentru sincronizari. intr-un thread, practic am doar metoda run si in functie de job-ul pe care il extrage se ruleaza o functie(adica fiecare tip de job  are un id si parametrii specifici. metodele sunt urmatoarele:
join_all - metoda ce face join dintr-un thread pe celelalte
states_mean - se face o lista in care se calculeaza pentru fiecare stat un tuplu de suma totala si numarul de studii, iar apoi imparte in rezultat suma la numar
state_mean - metoda ce calculeaza doar pentru un singur stat, analog ca mai sus
best5 - metoda ce calculeaza primele 5, analog ca mai sus doar ca le ia pe primele
worst5 - metoda ce calculeaza primele 5, analog ca mai sus doar ca le ia pe ultimele(cum scrie si in enunt, depinde de cum e formulata intrebarea)
global_mean - metoda ce calculeaza global_mean, ia o variabila unde tine suma si un counter
diff_from_mean - se face media globala si media pentru fiecare stat ca mai sus si se face diferenta lor
state_diff_from_mean - metoda ce calculeaza analog ca mai sus doar ca pentru un stat
mean_by_category - metoda ce calculeaza media dupa categorie, functioneaza ca states_mean doar ca cheia din lista e si in functie de categorie.
state_mean_by_category - metoda ce calculeaza analog ca mai sus doar ca pentru un stat
Fiecare request este pus in coada folosind un lock, iar la cererea rezultatului se verifica daca exista o cheie cu id-ul job-ului intr-un dictionar de job-uri terminate. 
Pentru logging mi-am facut un logger in care am folosit ca handler RotatingFileHandler, nivel de info si ca format gmtime, la fiecare request faceam un log cu request-ul primit.
In unittesting am trimis niste request-uri, dupa care am dat graceful_shutdown si am verificat numarul de job-uri si starea job-urilor. Pentru a dovedi ca este corect implementat se poate rula
testul de 2 ori, astfel dovedindu-se ca noile request-uri nu mai sunt luate in consideratie si server-ul poate fi oprit.
Pentru a rula: python3 TestWebserver.py
