# NOC_Scritps
This folder contain scripts related to work automations

*Disclamers*

La presente cartella contiene scripts utilizzati per la convalida delle abilità di scrittura in Python applicate su infrastrutture di reti internet e management reali.
Gli script sono stati utilizzati prettamente per uso personale all'interno del NOC per il raggoungimento delle task che risultavano ripetititve raggruppandole in singole funzioni.

## SMF_SNMP_RISK (Manipolazione Struttura dati JSON)

Link rischio SMF IP, ossia che sono composti da un solo link fisico per tratta, che se cade, ed il traffico non si riesce a distribuire senza saturare altri link creano le circostanze per fare uno SMF.

PS ci sono delle tratte che fanno 10 giga 1 Giga di traffico tra questi link e che tante volte fanno ammalapena  1 o 2 mega e che quindi non contano a patto che il traffico venga redistribuito senza problemi.
 
Particolare attenzione va agli Intralink tra sopra menzionati come per esempio CAS-CAS o TIR-TIR dove se si perde quel link bisognerà fare lo SMNP tabella BLUE per il router di gerarchia piu bassa, dato il link in questione è solo uno per una tratta interna. 
Nei link normali invece la raggiungibilità viene quasi sempre backuppata facendo un altro giro, dovendo porre attenzione alla possibilità di un presunto SMF IP in quel caso.
 
## Scraper (Object-Oriented Programming)

Il file presente definisce una parent class NetworkManagementTool dove child classes sono definite andando ad agire in modo spcfico con funzioni ad-hoc per il NMT/DB di referernza

```python
NetworkManagementTool()
  SCAINEMO()
      # Funzioni specifiche per SCAINEMO
  NETCRECKER()
      # Funzioni specifche per netcrecker
```
Questo design permette la creazione di un oggetto singlo che dinamicamente puo accedere a piu informazioni da molteplici collector (o monitoring/DB)
