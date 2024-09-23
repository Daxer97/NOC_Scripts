# SPARKLE_AUTOMATION
This folder contain scripts related to work automations

## SMF_SNMP_RISK

Link rischio SMF IP, ossia che sono composti da un solo link fisico per tratta, che se cade, ed il traffico non si riesce a distribuire senza saturare altri link creano le circostanze per fare uno SMF.

PS ci sono delle tratte che fanno 10 giga 1 Giga di traffico tra questi link e che tante volte fanno ammalapena  1 o 2 mega e che quindi non contano a patto che il traffico venga redistribuito senza problemi.
 
Particolare attenzione va agli Intralink tra sopra menzionati come per esempio CAS-CAS o TIR-TIR dove se si perde quel link bisognerà fare lo SMNP tabella BLUE per il router di gerarchia piu bassa, dato il link in questione è solo uno per una tratta interna. 
Nei link normali invece la raggiungibilità viene quasi sempre backuppata facendo un altro giro, dovendo porre attenzione alla possibilità di un presunto SMF IP in quel caso.
 
## Scraper

Il file presente definisce una parent class NetworkManagementTool dove child classes sono definite andando ad agire in modo spcfico con funzioni ad-hoc per il NMT do referernza

NetworkManagementTool()
  SCAINEMO()
  # Funzioni specifiche per SCAINEMO
  NETCRECKER()
  # Funzioni specifche per netcrecker

Questo design permette la creazione di un oggetto singlo che dinamicamente puo accedere a piu informazioni da molteplici collector (o monitoring/DB)
