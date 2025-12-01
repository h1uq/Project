## Anforderungen

### Aufgabenstellung

Eure Aufgabe ist es einen "Roboter" zu programmieren, der sich selbstständig durch ein Labyrinth bis zu einem Ausgang den Weg findet.

Hierzu muss der Roboter einen Algorithmus nutzen, d.h. er darf nicht um Zufallsverfahren Schritte machen und "hoffen", dass er irgendwann am Ziel ankommt. Der Roboter muss einzelne Schritte machen, und das Labyrinth wirklich erkunden, d.h. er hat keine interne Karte mit der er automatisch den richtigen Weg wählt, oder er ist auch keine Drohne, er kann nicht teleportieren usw. Also wie in der echten Welt: reinlaufen und erkunden.

Ihr dürft annehmen, dass es sich um ein echtes Labyrinth OHNE Kreise handelt, d.h. es gibt garantiert immer (mindestens) 1 Pfad vom Start bis zum Ziel, man kann aber nicht "im Kreis" laufen. Sackgassen hingegen gibt es natürlich schon.

Die Wahl des Algorithmus ist Euch überlassen, aber wenn man recherchiert kommt man schnell auf einen eigentlich ganz simplen Algorithmus (der sich in 4 Worte zusammenfassen lässt;-)
Das Programm soll pyGame nutzen: Man muss die einzelnen Schritte des Roboters sehen können. Man muss auch sehen können wie er seine Welt erkundet. Beispiel: es gibt Algorithmen, bei denen man immer an einer Seite überprüft, ob da eine Wand ist. Man sollte "irgendwie" sehen, dass der Roboter überprüft, ob dort eine Wand ist (also z.B. indem er sich dorthin dreht, oder durch eine Animation, usw)

Das Programm muss das Spielfeld aus einer Datei einlesen. Dabei gilt:

- 1 = Wand
- 0 = begehbarer Gang
- S = Start
- Z = Ziel

Auf Szejlas Wunsch hin: es müssen Soundeffekte dabei sein, bzw ein Soundtrack im Hintergrund spielen.

### Bewertungskriterien

Hier ist beispielhaft eine Liste von Dingen, die ich im Code anschaue:

- ist der Code ordentlich strukturiert (Funktionen, anstatt ein riesen Block)
- sind Kommentare drin?
- sinnvolle/selbsterklärende Variablennamen und Nutzung
- sinnvolle (wenn sinnvoll;-) Nutzung von Try-Except
- gute Nutzung von Datenstrukturen (Listen, Dictionaries, Tuples)
- "fortgeschrittene" Python Features wie List-Comprehension, das eingebaute "sorted", etc

### Bearbeitung

Die Aufgabe wird in 3er Gruppen bearbeitet. Maximal zwei 4er Gruppen sind erlaubt, wenn es mit 3er Gruppen nicht aufgeht. Die Gruppen finden sich selbst zusammen.

Die Benutzung von ChatGPT ist erlaubt, MUSS aber dokumentiert werden - das soll keine "Qual" oder "Überprüfung" sein, sondern gleich als Übung dienen, sich aktiv mit ChatGPT auseinander zu setzen und den Output kritisch zu hinterfragen, und gezielt zum Lernen zu nutzen. D.h. in der Ausarbeitung erwarte ich die (wichtigsten) Prompts, die Ihr genutzt habt, den Output, und Eure Bewertung des Outputs.

In der mündlichen Prüfung (Hauptteil der Prüfungsleistung) erwarte ich, dass Ihr Euren eigenen Code versteht - d.h. wenn ChatGPT Euch Code gibt, stellt sicher, dass Ihr den _komplett_ versteht - ich werde Fragen stellen!

### Abgabe

Erwartet werden:

- der Code: 1 Python file, und falls nötig, maximal EINE Input-Datei (falls Ihr z.B ein Spielfeld in einer Datei speichern wollt)
- Eine KURZE Ausarbeitung:
  - Dokumentation des/der benutzten Algorithmen für die KI, zusammen mit Begründung, WARUM genau dieser Algorithmus genutzt wurde
  - die wichtigsten Design-Entscheidungen (warum Ihr bestimmte Datenstrukturen genutzt habt, was implementiert wurde, und was nicht (und warum), etc)
  - die wichtigsten ChatGPT Prompts + Analyse (siehe oben)
- Ein kurzes (maximal 10 Minuten) Übersichtsvideo über den Spielablauf (kurz demonstrieren wie/ob es funktioniert, idealerweise für ein paar verschiedene Szenarien), und eine Übersicht über die "highlights" des Codes. Link zum Video bitte auf der ersten Seite der Ausarbeitung.
