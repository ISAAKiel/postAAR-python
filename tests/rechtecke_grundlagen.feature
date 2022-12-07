# language: de
Funktionalität: Rechtecke erkennen
Vierecke die in die gegebenen Parameter fallen müssen als Rechtecke erkannt werden.
  Hierbei wird nur getestet, ob die Vierecke erkannt werden!
  In den Test- und Kontrollsets haben die Punkte folgendes Format:
    Punkt-Id,x-Position,y-Position,Rechteck-Id,Differenz-zu-perfektem-Rechteck,minimale-Seitenlänge-des-Rechtecks,maximale-Seitenlänge-des-Rechtecks

  Szenariogrundriss: In einer Punktwolke aus <Datei> werden Rechtecke mit den Parametern <Differenz>, <Minimum> und <Maximum> gesucht
    Angenommen die Punkte aus dem Test- und Kontrollset "<Datei>" wurden geladen
    Und die erwarteten Rechtecke sollen eine maximale Differenz von "<Differenz>" Prozent haben
    Und die erwarteten Rechtecke sollen eine Seitenlänge zwischen "<Minimum>" und "<Maximum>" haben
    Wenn nach den Rechtecken gesucht wird
    Dann werden nur die Rechtecke gefunden die zu den Werten passen

    Beispiele:
      | Datei                                    | Differenz | Minimum | Maximum |
      | test_shape_rectangle.csv                 | 10        | 4.5     | 6.5     |
      | test_shape_rectangle.csv                 | 10        | 9.5     | 10.5    |
      | test_shape_rectangle.csv                 | 10        | 1.5     | 6.5     |
      | test_shape_rectangle.csv                 | 10        | 1.5     | 10.5    |
      | test_shape_rectangle.csv                 | 10        | 1.0     | 1.5     |
      | test_shape_rectangle.csv                 | 10        | 5.5     | 10.5    |
      | test_shape_rectangle_with_jitter_0.1.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.2.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.3.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.4.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.5.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.6.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.7.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.8.csv | 10        | 1.5     | 2.5     |
      | test_shape_rectangle_with_jitter_0.9.csv | 10        | 1.5     | 2.5     |
      | test_shape_rombus_2_2.csv                | 10        | 1.5     | 2.5     |
      | test_shape_rombus_2_5.csv                | 10        | 1.5     | 2.5     |
      | test_shape_rombus_2_10.csv               | 10        | 1.5     | 2.5     |
      | test_shape_rombus_5_5.csv                | 10        | 1.5     | 2.5     |
      | test_shape_rombus_5_10.csv               | 10        | 1.5     | 2.5     |
      | test_shape_rombus_10_10.csv              | 10        | 1.5     | 2.5     |
      | test_shape_trapezoid_2_2.csv             | 11        | 1.5     | 2.5     |
      | test_shape_trapezoid_2_5.csv             | 10        | 1.5     | 2.5     |
      | test_shape_trapezoid_2_10.csv            | 10        | 1.5     | 2.5     |
      | test_shape_trapezoid_5_5.csv             | 10        | 1.5     | 2.5     |
      | test_shape_trapezoid_5_10.csv            | 10        | 1.5     | 2.5     |
      | test_shape_trapezoid_10_10.csv           | 10        | 1.5     | 2.5     |