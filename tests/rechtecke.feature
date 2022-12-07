# language: de
Funktionalität: Rechtecke erkennen
Vierecke die in die gegebenen Parameter fallen müssen als Rechtecke erkannt werden.

  Szenario:  In einer Punktwolke werden Rechtecke gesucht
    Angenommen die Punkte aus dem Test- und Kontrollset "test_shape_rectangle.csv" wurden geladen
    Und die erwarteten Rechtecke sollen eine maximale Differenz von "10" Prozent haben
    Und die erwarteten Rechtecke sollen eine Seitenlänge zwischen "1.5" und "2.5" haben
    Wenn nach den Rechtecken gesucht wird
    Dann werden nur die Rechtecke gefunden die zu den Werten passen

