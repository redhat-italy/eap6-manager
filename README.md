Eap 6 manager
=================

script per gestion semplificata di EAP6

Funzioni implementate:

* start/stop server group
* start/stop istanza
* deploy
* creazione di un server group
* creazione di un istanza
* creazione e copia nel domain controller di un domain.xml partendo da template (crea un profilo duplicando full*ha, si possono aggiungere profili a piacere)
* set Jvm opts su una server group
* set jvm opts su una istanza
* check connessione datasource configurato
* check statistiche datasource con polling sulla CLI
* check statistiche thread con polling sulla CLI
* check statistiche connettore http con polling sulla CLI
* check multicast send/receive con jgroups
* check istanza jboss attive sulla macchina con indicazione utente/pid/nome server
* storage log files

Per estendere implementare BaseCommand e aggiungere la funzione a Main.py

```python
class StartInstanceCommand(BaseCommand)
	def execute(self, jbossHome, controller, user, password):
	#code here
```
