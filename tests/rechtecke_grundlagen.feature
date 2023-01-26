# language: de
Funktionalität: Rechtecke erkennen
Vierecke die in die gegebenen Parameter fallen müssen als Rechtecke erkannt werden.
  Hierbei wird nur getestet, ob die Vierecke erkannt werden!
  In den Test- und Kontrollsets haben die Punkte folgendes Format:
    Punkt-Id,x-Position,y-Position,Rechteck-Id,Differenz-zu-perfektem-Rechteck,minimale-Seitenlänge-des-Rechtecks,maximale-Seitenlänge-des-Rechtecks

  Szenariogrundriss: In einer Punktwolke aus <Datei> werden Rechtecke mit verschiedenen Parametern gesucht
    Angenommen die Punkte aus dem Test- und Kontrollset "<Datei>" aus dem Ordner "basic_test-control_sets" wurden geladen
    Wenn nach den Rechtecken mit den Parametern in der Liste gesucht wird
      | Differenz | Minimum | Maximum |
      | 10        | 1.5     | 2.5     |
      | 10        | 1.5     | 3.5     |
      | 10        | 1.5     | 5.5     |
      | 10        | 1.5     | 7.5     |
      | 10        | 1.5     | 10.5    |
      | 10        | 1.5     | 11.5    |
      | 10        | 1.5     | 12.5    |
      | 10        | 2.5     | 3.5     |
      | 10        | 2.5     | 5.5     |
      | 10        | 2.5     | 7.5     |
      | 10        | 2.5     | 10.5    |
      | 10        | 2.5     | 11.5    |
      | 10        | 2.5     | 12.5    |
      | 10        | 5.5     | 7.5     |
      | 10        | 5.5     | 10.5    |
      | 10        | 5.5     | 11.5    |
      | 10        | 5.5     | 12.5    |
      | 15        | 1.5     | 2.5     |
      | 15        | 1.5     | 3.5     |
      | 15        | 1.5     | 5.5     |
      | 15        | 1.5     | 7.5     |
      | 15        | 1.5     | 10.5    |
      | 15        | 1.5     | 11.5    |
      | 15        | 1.5     | 12.5    |
      | 15        | 2.5     | 3.5     |
      | 15        | 2.5     | 5.5     |
      | 15        | 2.5     | 7.5     |
      | 15        | 2.5     | 10.5    |
      | 15        | 2.5     | 11.5    |
      | 15        | 2.5     | 12.5    |
      | 15        | 5.5     | 7.5     |
      | 15        | 5.5     | 10.5    |
      | 15        | 5.5     | 11.5    |
      | 15        | 5.5     | 12.5    |
      | 25        | 1.5     | 2.5     |
      | 25        | 1.5     | 3.5     |
      | 25        | 1.5     | 5.5     |
      | 25        | 1.5     | 7.5     |
      | 25        | 1.5     | 10.5    |
      | 25        | 1.5     | 11.5    |
      | 25        | 1.5     | 12.5    |
      | 25        | 2.5     | 3.5     |
      | 25        | 2.5     | 5.5     |
      | 25        | 2.5     | 7.5     |
      | 25        | 2.5     | 10.5    |
      | 25        | 2.5     | 11.5    |
      | 25        | 2.5     | 12.5    |
      | 25        | 5.5     | 7.5     |
      | 25        | 5.5     | 10.5    |
      | 25        | 5.5     | 11.5    |
      | 25        | 5.5     | 12.5    |

    Dann werden nur die Rechtecke gefunden die zu den Parametern in der Liste passen

    Beispiele:
      | Datei                           |
      | rectangle_1.csv                 |
      | rectangle_with_jitter_0.1_1.csv |
      | rectangle_with_jitter_0.1_2.csv |
      | rectangle_with_jitter_0.1_3.csv |
      | rectangle_with_jitter_0.1_4.csv |
      | rectangle_with_jitter_0.1_5.csv |
      | rectangle_with_jitter_0.2_1.csv |
      | rectangle_with_jitter_0.2_2.csv |
      | rectangle_with_jitter_0.2_3.csv |
      | rectangle_with_jitter_0.2_4.csv |
      | rectangle_with_jitter_0.2_5.csv |
      | rectangle_with_jitter_0.3_1.csv |
      | rectangle_with_jitter_0.3_2.csv |
      | rectangle_with_jitter_0.3_3.csv |
      | rectangle_with_jitter_0.3_4.csv |
      | rectangle_with_jitter_0.3_5.csv |
      | rectangle_with_jitter_0.4_1.csv |
      | rectangle_with_jitter_0.4_2.csv |
      | rectangle_with_jitter_0.4_3.csv |
      | rectangle_with_jitter_0.4_4.csv |
      | rectangle_with_jitter_0.4_5.csv |
      | rectangle_with_jitter_0.5_1.csv |
      | rectangle_with_jitter_0.5_2.csv |
      | rectangle_with_jitter_0.5_3.csv |
      | rectangle_with_jitter_0.5_4.csv |
      | rectangle_with_jitter_0.5_5.csv |
      | rectangle_with_jitter_0.6_1.csv |
      | rectangle_with_jitter_0.6_2.csv |
      | rectangle_with_jitter_0.6_3.csv |
      | rectangle_with_jitter_0.6_4.csv |
      | rectangle_with_jitter_0.6_5.csv |
      | rectangle_with_jitter_0.7_1.csv |
      | rectangle_with_jitter_0.7_2.csv |
      | rectangle_with_jitter_0.7_3.csv |
      | rectangle_with_jitter_0.7_4.csv |
      | rectangle_with_jitter_0.7_5.csv |
      | rectangle_with_jitter_0.8_1.csv |
      | rectangle_with_jitter_0.8_2.csv |
      | rectangle_with_jitter_0.8_3.csv |
      | rectangle_with_jitter_0.8_4.csv |
      | rectangle_with_jitter_0.8_5.csv |
      | rectangle_with_jitter_0.9_1.csv |
      | rectangle_with_jitter_0.9_2.csv |
      | rectangle_with_jitter_0.9_3.csv |
      | rectangle_with_jitter_0.9_4.csv |
      | rectangle_with_jitter_0.9_5.csv |
      | rombus_2_2_1.csv                |
      | rombus_2_2_2.csv                |
      | rombus_2_5_1.csv                |
      | rombus_2_5_2.csv                |
      | rombus_2_10_1.csv               |
      | rombus_2_10_2.csv               |
      | rombus_5_5_1.csv                |
      | rombus_5_5_2.csv                |
      | rombus_5_10_1.csv               |
      | rombus_5_10_2.csv               |
      | rombus_10_10_1.csv              |
      | rombus_10_10_2.csv              |
      | trapezoid_2_2_1.csv             |
      | trapezoid_2_2_2.csv             |
      | trapezoid_2_2_3.csv             |
      | trapezoid_2_2_4.csv             |
      | trapezoid_2_2_5.csv             |
      | trapezoid_2_2_6.csv             |
      | trapezoid_2_2_7.csv             |
      | trapezoid_2_2_8.csv             |
      | trapezoid_2_5_1.csv             |
      | trapezoid_2_5_2.csv             |
      | trapezoid_2_5_3.csv             |
      | trapezoid_2_5_4.csv             |
      | trapezoid_2_5_5.csv             |
      | trapezoid_2_5_6.csv             |
      | trapezoid_2_5_7.csv             |
      | trapezoid_2_5_8.csv             |
      | trapezoid_2_10_1.csv            |
      | trapezoid_2_10_2.csv            |
      | trapezoid_2_10_3.csv            |
      | trapezoid_2_10_4.csv            |
      | trapezoid_2_10_5.csv            |
      | trapezoid_2_10_6.csv            |
      | trapezoid_2_10_7.csv            |
      | trapezoid_2_10_8.csv            |
      | trapezoid_5_5_1.csv             |
      | trapezoid_5_5_2.csv             |
      | trapezoid_5_5_3.csv             |
      | trapezoid_5_5_4.csv             |
      | trapezoid_5_5_5.csv             |
      | trapezoid_5_5_6.csv             |
      | trapezoid_5_5_7.csv             |
      | trapezoid_5_5_8.csv             |
      | trapezoid_5_10_1.csv            |
      | trapezoid_5_10_2.csv            |
      | trapezoid_5_10_3.csv            |
      | trapezoid_5_10_4.csv            |
      | trapezoid_5_10_5.csv            |
      | trapezoid_5_10_6.csv            |
      | trapezoid_5_10_7.csv            |
      | trapezoid_5_10_8.csv            |
      | trapezoid_10_10_1.csv           |
      | trapezoid_10_10_2.csv           |
      | trapezoid_10_10_3.csv           |
      | trapezoid_10_10_4.csv           |
      | trapezoid_10_10_5.csv           |
      | trapezoid_10_10_6.csv           |
      | trapezoid_10_10_7.csv           |
      | trapezoid_10_10_8.csv           |