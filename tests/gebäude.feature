# language: de
Funktionalität: Gebäude erkennen
Gebäude werden aus Rechtecken gebildet.

  Szenario: Rechtecke bilden alle Gebäude
    Angenommen die Punkte und Rechtecke aus dem Testordner "rectangle_square_over_square_1-3" wurden geladen
    Wenn nach möglichen Gebäuden gesucht wird
    Dann werden alle möglichen Gebäude gefunden

  Szenario: Rechtecke bilden alle Gebäude (multicore)
    Angenommen die Punkte und Rechtecke aus dem Testordner "rectangle_square_over_square_1-3" wurden geladen
    Wenn nach möglichen Gebäuden mit mehreren Kernen gesucht wird
    Dann werden alle möglichen Gebäude gefunden

  Szenario: Rechtecke bilden Gebäude ohne Löcher
    Angenommen die Punkte und Rechtecke aus dem Testordner "building_without_hole_1-1.5" wurden geladen
    Wenn nach möglichen Gebäuden gesucht wird
    Dann werden alle möglichen Gebäude gefunden

  Szenario: Rechtecke bilden Gebäude ohne Löcher (multicore)
    Angenommen die Punkte und Rechtecke aus dem Testordner "building_without_hole_1-1.5" wurden geladen
    Wenn nach möglichen Gebäuden mit mehreren Kernen gesucht wird
    Dann werden alle möglichen Gebäude gefunden