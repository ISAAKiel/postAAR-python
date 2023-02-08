# language: de
Funktionalität: Rechtecke erkennen
Vierecke die in die gegebenen Parameter fallen müssen als Rechtecke erkannt werden.

  Szenario:  In einer Punktwolke werden Rechtecke gesucht
    Angenommen die Punkte und erwarteten Rechtecke aus dem Testordner "rectangle_square_over_square_1-3" wurden geladen
    Und die erwarteten Rechtecke sollen eine maximale Differenz von "1" Prozent haben
    Und die erwarteten Rechtecke sollen eine Seitenlänge zwischen "0.9" und "3.1" haben
    Wenn nach den Rechtecken gesucht wird
    Dann werden nur die Rechtecke gefunden die zu den Parametern passen

  Szenario:  In einer Punktwolke werden Rechtecke gesucht (multicore)
    Angenommen die Punkte und erwarteten Rechtecke aus dem Testordner "rectangle_square_over_square_1-3" wurden geladen
    Und die erwarteten Rechtecke sollen eine maximale Differenz von "1" Prozent haben
    Und die erwarteten Rechtecke sollen eine Seitenlänge zwischen "0.9" und "3.1" haben
    Wenn nach den Rechtecken mit mehreren Kernen gesucht wird
    Dann werden nur die Rechtecke gefunden die zu den Parametern passen

