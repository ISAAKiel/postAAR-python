# postAARectangle

postAARectangle is a small R Shiny app that complements the QGIS plugin [postAAR-python](https://github.com/ISAAKiel/postAAR-python). It serves exclusively to visualise the skewness of quadrilaterals on the basis of the area deviation from the corresponding minimum rotated rectangle. Thus, the parameter used in postAAR for the quality of the quadrilaterals to be found can be quickly captured visually.

To load the app into RStudio, please execute the following commands:

```
if (!require('shiny')) install.packages('shiny')
shiny::runGitHub(repo="postAARectangle", username="ISAAKiel", ref = "main")
```

postAARectangle ist eine kleine R Shiny App in Ergänzung zu dem QGIS plugin [postAAR-python](https://github.com/ISAAKiel/postAAR-python). Sie dient ausschließlich zur Visualisierung der Schiefe von Vierecken anhand der Flächenabweichung zum kleinsten umschließenden Rechteck. Damit kann der in postAAR verwendete Paramter für die Güte der zu findenden Vierecke schnell visuell erfasst werden.

Um die App in RStudio zu laden führen Sie bitte folgende Befehle aus:

```
if (!require('shiny')) install.packages('shiny')
shiny::runGitHub(repo="postAARectangle", username="ISAAKiel", ref = "main")
```