[![Tests](https://github.com/ISAAKiel/postAAR-python/actions/workflows/tests.yml/badge.svg)](https://github.com/ISAAKiel/postAAR-python/actions/workflows/tests.yml)
[![license](https://img.shields.io/badge/license-GPL%203-B50B82.svg)](https://www.r-project.org/Licenses/GPL-3)

# postAAR-python

This is a QGIS plugin for finding rectangular structures in a point layer. It is intended for archaeological excavations to find possible houses in a field of postholes. You can set the minimum and maximum distance between the posts and a degree of skewness by the area difference to the corresponding minimum rotated rectangle. For further explanations see Jupyter Notebook [how_it_works.ipynb](how_it_works.ipynb). To know the degree of skew, you can [run a R shiny app](./help/readme.md).

If you install the plugin from a zip file, please rename the folder of the plugin to postAAR.

Windows: c:\Users\\\<user\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\postAAR

MacOS: /\<user>/Library/Application\Support/QGIS/QGIS3/profiles/default/python/plugins/postAAR 
