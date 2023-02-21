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
      | rectangle_1.csv |
      | rectangle_2.csv |
      | rectangle_3.csv |
      | rectangle_with_jitter_0.1_1.csv |
      | rectangle_with_jitter_0.1_10.csv |
      | rectangle_with_jitter_0.1_11.csv |
      | rectangle_with_jitter_0.1_12.csv |
      | rectangle_with_jitter_0.1_13.csv |
      | rectangle_with_jitter_0.1_14.csv |
      | rectangle_with_jitter_0.1_15.csv |
      | rectangle_with_jitter_0.1_2.csv |
      | rectangle_with_jitter_0.1_3.csv |
      | rectangle_with_jitter_0.1_4.csv |
      | rectangle_with_jitter_0.1_5.csv |
      | rectangle_with_jitter_0.1_6.csv |
      | rectangle_with_jitter_0.1_7.csv |
      | rectangle_with_jitter_0.1_8.csv |
      | rectangle_with_jitter_0.1_9.csv |
      | rectangle_with_jitter_0.2_1.csv |
      | rectangle_with_jitter_0.2_10.csv |
      | rectangle_with_jitter_0.2_11.csv |
      | rectangle_with_jitter_0.2_12.csv |
      | rectangle_with_jitter_0.2_13.csv |
      | rectangle_with_jitter_0.2_14.csv |
      | rectangle_with_jitter_0.2_15.csv |
      | rectangle_with_jitter_0.2_2.csv |
      | rectangle_with_jitter_0.2_3.csv |
      | rectangle_with_jitter_0.2_4.csv |
      | rectangle_with_jitter_0.2_5.csv |
      | rectangle_with_jitter_0.2_6.csv |
      | rectangle_with_jitter_0.2_7.csv |
      | rectangle_with_jitter_0.2_8.csv |
      | rectangle_with_jitter_0.2_9.csv |
      | rectangle_with_jitter_0.3_1.csv |
      | rectangle_with_jitter_0.3_10.csv |
      | rectangle_with_jitter_0.3_11.csv |
      | rectangle_with_jitter_0.3_12.csv |
      | rectangle_with_jitter_0.3_13.csv |
      | rectangle_with_jitter_0.3_14.csv |
      | rectangle_with_jitter_0.3_15.csv |
      | rectangle_with_jitter_0.3_2.csv |
      | rectangle_with_jitter_0.3_3.csv |
      | rectangle_with_jitter_0.3_4.csv |
      | rectangle_with_jitter_0.3_5.csv |
      | rectangle_with_jitter_0.3_6.csv |
      | rectangle_with_jitter_0.3_7.csv |
      | rectangle_with_jitter_0.3_8.csv |
      | rectangle_with_jitter_0.3_9.csv |
      | rectangle_with_jitter_0.4_1.csv |
      | rectangle_with_jitter_0.4_10.csv |
      | rectangle_with_jitter_0.4_11.csv |
      | rectangle_with_jitter_0.4_12.csv |
      | rectangle_with_jitter_0.4_13.csv |
      | rectangle_with_jitter_0.4_14.csv |
      | rectangle_with_jitter_0.4_15.csv |
      | rectangle_with_jitter_0.4_2.csv |
      | rectangle_with_jitter_0.4_3.csv |
      | rectangle_with_jitter_0.4_4.csv |
      | rectangle_with_jitter_0.4_5.csv |
      | rectangle_with_jitter_0.4_6.csv |
      | rectangle_with_jitter_0.4_7.csv |
      | rectangle_with_jitter_0.4_8.csv |
      | rectangle_with_jitter_0.4_9.csv |
      | rectangle_with_jitter_0.5_1.csv |
      | rectangle_with_jitter_0.5_10.csv |
      | rectangle_with_jitter_0.5_11.csv |
      | rectangle_with_jitter_0.5_12.csv |
      | rectangle_with_jitter_0.5_13.csv |
      | rectangle_with_jitter_0.5_14.csv |
      | rectangle_with_jitter_0.5_15.csv |
      | rectangle_with_jitter_0.5_2.csv |
      | rectangle_with_jitter_0.5_3.csv |
      | rectangle_with_jitter_0.5_4.csv |
      | rectangle_with_jitter_0.5_5.csv |
      | rectangle_with_jitter_0.5_6.csv |
      | rectangle_with_jitter_0.5_7.csv |
      | rectangle_with_jitter_0.5_8.csv |
      | rectangle_with_jitter_0.5_9.csv |
      | rectangle_with_jitter_0.6_1.csv |
      | rectangle_with_jitter_0.6_10.csv |
      | rectangle_with_jitter_0.6_11.csv |
      | rectangle_with_jitter_0.6_12.csv |
      | rectangle_with_jitter_0.6_13.csv |
      | rectangle_with_jitter_0.6_14.csv |
      | rectangle_with_jitter_0.6_15.csv |
      | rectangle_with_jitter_0.6_2.csv |
      | rectangle_with_jitter_0.6_3.csv |
      | rectangle_with_jitter_0.6_4.csv |
      | rectangle_with_jitter_0.6_5.csv |
      | rectangle_with_jitter_0.6_6.csv |
      | rectangle_with_jitter_0.6_7.csv |
      | rectangle_with_jitter_0.6_8.csv |
      | rectangle_with_jitter_0.6_9.csv |
      | rectangle_with_jitter_0.7_1.csv |
      | rectangle_with_jitter_0.7_10.csv |
      | rectangle_with_jitter_0.7_11.csv |
      | rectangle_with_jitter_0.7_12.csv |
      | rectangle_with_jitter_0.7_13.csv |
      | rectangle_with_jitter_0.7_14.csv |
      | rectangle_with_jitter_0.7_15.csv |
      | rectangle_with_jitter_0.7_2.csv |
      | rectangle_with_jitter_0.7_3.csv |
      | rectangle_with_jitter_0.7_4.csv |
      | rectangle_with_jitter_0.7_5.csv |
      | rectangle_with_jitter_0.7_6.csv |
      | rectangle_with_jitter_0.7_7.csv |
      | rectangle_with_jitter_0.7_8.csv |
      | rectangle_with_jitter_0.7_9.csv |
      | rectangle_with_jitter_0.8_1.csv |
      | rectangle_with_jitter_0.8_10.csv |
      | rectangle_with_jitter_0.8_11.csv |
      | rectangle_with_jitter_0.8_12.csv |
      | rectangle_with_jitter_0.8_13.csv |
      | rectangle_with_jitter_0.8_14.csv |
      | rectangle_with_jitter_0.8_15.csv |
      | rectangle_with_jitter_0.8_2.csv |
      | rectangle_with_jitter_0.8_3.csv |
      | rectangle_with_jitter_0.8_4.csv |
      | rectangle_with_jitter_0.8_5.csv |
      | rectangle_with_jitter_0.8_6.csv |
      | rectangle_with_jitter_0.8_7.csv |
      | rectangle_with_jitter_0.8_8.csv |
      | rectangle_with_jitter_0.8_9.csv |
      | rectangle_with_jitter_0.9_1.csv |
      | rectangle_with_jitter_0.9_10.csv |
      | rectangle_with_jitter_0.9_11.csv |
      | rectangle_with_jitter_0.9_12.csv |
      | rectangle_with_jitter_0.9_13.csv |
      | rectangle_with_jitter_0.9_14.csv |
      | rectangle_with_jitter_0.9_15.csv |
      | rectangle_with_jitter_0.9_2.csv |
      | rectangle_with_jitter_0.9_3.csv |
      | rectangle_with_jitter_0.9_4.csv |
      | rectangle_with_jitter_0.9_5.csv |
      | rectangle_with_jitter_0.9_6.csv |
      | rectangle_with_jitter_0.9_7.csv |
      | rectangle_with_jitter_0.9_8.csv |
      | rectangle_with_jitter_0.9_9.csv |
      | rombus_10_10_1.csv |
      | rombus_10_10_2.csv |
      | rombus_10_10_3.csv |
      | rombus_10_10_4.csv |
      | rombus_10_10_5.csv |
      | rombus_2_10_1.csv |
      | rombus_2_10_2.csv |
      | rombus_2_10_3.csv |
      | rombus_2_10_4.csv |
      | rombus_2_10_5.csv |
      | rombus_2_2_1.csv |
      | rombus_2_2_2.csv |
      | rombus_2_2_3.csv |
      | rombus_2_2_4.csv |
      | rombus_2_2_5.csv |
      | rombus_2_5_1.csv |
      | rombus_2_5_2.csv |
      | rombus_2_5_3.csv |
      | rombus_2_5_4.csv |
      | rombus_2_5_5.csv |
      | rombus_5_10_1.csv |
      | rombus_5_10_2.csv |
      | rombus_5_10_3.csv |
      | rombus_5_10_4.csv |
      | rombus_5_10_5.csv |
      | rombus_5_5_1.csv |
      | rombus_5_5_2.csv |
      | rombus_5_5_3.csv |
      | rombus_5_5_4.csv |
      | rombus_5_5_5.csv |
      | trapezoid_10_10_1.csv |
      | trapezoid_10_10_10.csv |
      | trapezoid_10_10_11.csv |
      | trapezoid_10_10_12.csv |
      | trapezoid_10_10_13.csv |
      | trapezoid_10_10_14.csv |
      | trapezoid_10_10_15.csv |
      | trapezoid_10_10_16.csv |
      | trapezoid_10_10_17.csv |
      | trapezoid_10_10_18.csv |
      | trapezoid_10_10_19.csv |
      | trapezoid_10_10_2.csv |
      | trapezoid_10_10_20.csv |
      | trapezoid_10_10_21.csv |
      | trapezoid_10_10_22.csv |
      | trapezoid_10_10_23.csv |
      | trapezoid_10_10_24.csv |
      | trapezoid_10_10_25.csv |
      | trapezoid_10_10_26.csv |
      | trapezoid_10_10_27.csv |
      | trapezoid_10_10_3.csv |
      | trapezoid_10_10_4.csv |
      | trapezoid_10_10_5.csv |
      | trapezoid_10_10_6.csv |
      | trapezoid_10_10_7.csv |
      | trapezoid_10_10_8.csv |
      | trapezoid_10_10_9.csv |
      | trapezoid_2_10_1.csv |
      | trapezoid_2_10_10.csv |
      | trapezoid_2_10_11.csv |
      | trapezoid_2_10_12.csv |
      | trapezoid_2_10_13.csv |
      | trapezoid_2_10_14.csv |
      | trapezoid_2_10_15.csv |
      | trapezoid_2_10_16.csv |
      | trapezoid_2_10_17.csv |
      | trapezoid_2_10_18.csv |
      | trapezoid_2_10_19.csv |
      | trapezoid_2_10_2.csv |
      | trapezoid_2_10_20.csv |
      | trapezoid_2_10_21.csv |
      | trapezoid_2_10_22.csv |
      | trapezoid_2_10_23.csv |
      | trapezoid_2_10_24.csv |
      | trapezoid_2_10_25.csv |
      | trapezoid_2_10_26.csv |
      | trapezoid_2_10_27.csv |
      | trapezoid_2_10_3.csv |
      | trapezoid_2_10_4.csv |
      | trapezoid_2_10_5.csv |
      | trapezoid_2_10_6.csv |
      | trapezoid_2_10_7.csv |
      | trapezoid_2_10_8.csv |
      | trapezoid_2_10_9.csv |
      | trapezoid_2_2_1.csv |
      | trapezoid_2_2_10.csv |
      | trapezoid_2_2_11.csv |
      | trapezoid_2_2_12.csv |
      | trapezoid_2_2_13.csv |
      | trapezoid_2_2_14.csv |
      | trapezoid_2_2_15.csv |
      | trapezoid_2_2_16.csv |
      | trapezoid_2_2_17.csv |
      | trapezoid_2_2_18.csv |
      | trapezoid_2_2_19.csv |
      | trapezoid_2_2_2.csv |
      | trapezoid_2_2_20.csv |
      | trapezoid_2_2_21.csv |
      | trapezoid_2_2_22.csv |
      | trapezoid_2_2_23.csv |
      | trapezoid_2_2_24.csv |
      | trapezoid_2_2_25.csv |
      | trapezoid_2_2_26.csv |
      | trapezoid_2_2_27.csv |
      | trapezoid_2_2_3.csv |
      | trapezoid_2_2_4.csv |
      | trapezoid_2_2_5.csv |
      | trapezoid_2_2_6.csv |
      | trapezoid_2_2_7.csv |
      | trapezoid_2_2_8.csv |
      | trapezoid_2_2_9.csv |
      | trapezoid_2_5_1.csv |
      | trapezoid_2_5_10.csv |
      | trapezoid_2_5_11.csv |
      | trapezoid_2_5_12.csv |
      | trapezoid_2_5_13.csv |
      | trapezoid_2_5_14.csv |
      | trapezoid_2_5_15.csv |
      | trapezoid_2_5_16.csv |
      | trapezoid_2_5_17.csv |
      | trapezoid_2_5_18.csv |
      | trapezoid_2_5_19.csv |
      | trapezoid_2_5_2.csv |
      | trapezoid_2_5_20.csv |
      | trapezoid_2_5_21.csv |
      | trapezoid_2_5_22.csv |
      | trapezoid_2_5_23.csv |
      | trapezoid_2_5_24.csv |
      | trapezoid_2_5_25.csv |
      | trapezoid_2_5_26.csv |
      | trapezoid_2_5_27.csv |
      | trapezoid_2_5_3.csv |
      | trapezoid_2_5_4.csv |
      | trapezoid_2_5_5.csv |
      | trapezoid_2_5_6.csv |
      | trapezoid_2_5_7.csv |
      | trapezoid_2_5_8.csv |
      | trapezoid_2_5_9.csv |
      | trapezoid_5_10_1.csv |
      | trapezoid_5_10_10.csv |
      | trapezoid_5_10_11.csv |
      | trapezoid_5_10_12.csv |
      | trapezoid_5_10_13.csv |
      | trapezoid_5_10_14.csv |
      | trapezoid_5_10_15.csv |
      | trapezoid_5_10_16.csv |
      | trapezoid_5_10_17.csv |
      | trapezoid_5_10_18.csv |
      | trapezoid_5_10_19.csv |
      | trapezoid_5_10_2.csv |
      | trapezoid_5_10_20.csv |
      | trapezoid_5_10_21.csv |
      | trapezoid_5_10_22.csv |
      | trapezoid_5_10_23.csv |
      | trapezoid_5_10_24.csv |
      | trapezoid_5_10_25.csv |
      | trapezoid_5_10_26.csv |
      | trapezoid_5_10_27.csv |
      | trapezoid_5_10_3.csv |
      | trapezoid_5_10_4.csv |
      | trapezoid_5_10_5.csv |
      | trapezoid_5_10_6.csv |
      | trapezoid_5_10_7.csv |
      | trapezoid_5_10_8.csv |
      | trapezoid_5_10_9.csv |
      | trapezoid_5_5_1.csv |
      | trapezoid_5_5_10.csv |
      | trapezoid_5_5_11.csv |
      | trapezoid_5_5_12.csv |
      | trapezoid_5_5_13.csv |
      | trapezoid_5_5_14.csv |
      | trapezoid_5_5_15.csv |
      | trapezoid_5_5_16.csv |
      | trapezoid_5_5_17.csv |
      | trapezoid_5_5_18.csv |
      | trapezoid_5_5_19.csv |
      | trapezoid_5_5_2.csv |
      | trapezoid_5_5_20.csv |
      | trapezoid_5_5_21.csv |
      | trapezoid_5_5_22.csv |
      | trapezoid_5_5_23.csv |
      | trapezoid_5_5_24.csv |
      | trapezoid_5_5_25.csv |
      | trapezoid_5_5_26.csv |
      | trapezoid_5_5_27.csv |
      | trapezoid_5_5_3.csv |
      | trapezoid_5_5_4.csv |
      | trapezoid_5_5_5.csv |
      | trapezoid_5_5_6.csv |
      | trapezoid_5_5_7.csv |
      | trapezoid_5_5_8.csv |
      | trapezoid_5_5_9.csv |