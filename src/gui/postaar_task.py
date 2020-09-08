from qgis.core import (Qgis, QgsApplication, QgsMessageLog, QgsTask, QgsField, QgsPointXY, QgsFeature, QgsGeometry)
from PyQt5.QtCore import (QVariant)

from src.algorithm import helper as hlp
from src.algorithm import algorithm as alg

class postAARTask(QgsTask):
    def __init__(self, iface, postlayer, postid, maximum_length_of_side, minimum_length_of_side, max_area_diff, buildings, multicore, number_of_cores):
        self.name = 'postAAR ' + postlayer.name() + ' (' + ("_".join(str(i) for i in [maximum_length_of_side, minimum_length_of_side, max_area_diff])) + ')'
        super().__init__(self.name, QgsTask.AllFlags)

        self.iface = iface

        self.postlayer = postlayer
        self.postid = postid
        self.maximum_length_of_side = maximum_length_of_side
        self.minimum_length_of_side = minimum_length_of_side
        self.max_area_diff = max_area_diff

        self.buildings = buildings

        self.multicore = multicore
        self.number_of_cores = number_of_cores

        self.exception = None
        self.found_rects = []

        QgsMessageLog.logMessage('Preparing data', self.name, Qgis.Info)
        self.postslist = []
        for f in postlayer.getFeatures():
            pid = f[postid]
            x = f.geometry().asPoint().x()
            y = f.geometry().asPoint().y()
            self.postslist.append([pid, x, y])

    def run(self):
        QgsMessageLog.logMessage('Started', self.name, Qgis.Info)
        self.setProgress(0)
        if self.multicore:
            return self.runMulticore()
        else:
            return self.runSinglecore()

    def runMulticore(self):
        return True

    def runSinglecore(self):
        try:
            QgsMessageLog.logMessage('Building windows', self.name, Qgis.Info)
            windows = hlp.buildWindows(self.postslist, self.maximum_length_of_side)
            self.setProgress(30)

            QgsMessageLog.logMessage('Finding rectangles', self.name, Qgis.Info)
            self.found_rects = alg.find_rects(windows, self.postslist, self.maximum_length_of_side, self.minimum_length_of_side, self.max_area_diff, number_of_computercores=1)
            QgsMessageLog.logMessage('Found ' + str(len(self.found_rects)) + ' rectangles', self.name, Qgis.Info)
            self.setProgress(60)

            id = 0
            for rect in self.found_rects:
                rect.setId(id)
                id += 1

            if True or self.buildings:
                print('Finding buildings', end='', flush=True)
                QgsMessageLog.logMessage('Finding buildings', self.name, Qgis.Info)
                self.buildings = alg.findBuildings(self.found_rects, self.postslist, number_of_computercores=1)
                QgsMessageLog.logMessage('Found ' + str(len(self.buildings)) + ' buildings', self.name, Qgis.Info)
            self.setProgress(90)

            return True
        except Exception as e:
            self.exception = e
            return False

    def finished(self, result):
        if self.exception:
            QgsMessageLog.logMessage('Task Exception: {exception}'.format(exception=self.exception), self.name, Qgis.Critical)
            raise self.exception
        else:
            if len(self.found_rects) > 0:
                QgsMessageLog.logMessage('Creating rectangle layer', self.name, Qgis.Info)
                results_layer = self.iface.addVectorLayer("Polygon?crs=" + self.postlayer.crs().authid(), self.postlayer.name() + "_found_rectangles " + self.name, "memory")

                # add basic attributes
                pr = results_layer.dataProvider()
                pr.addAttributes([QgsField("rect_ID", QVariant.String), QgsField("PostIDs", QVariant.String)])
                results_layer.updateFields()

                # add the rectangles by a point list build first
                for rectangle in self.found_rects:
                    # build geometry
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(self.postslist[point][1], self.postslist[point][2]) for point in rectangle.corners]]))
                    feature.setAttributes([str(rectangle.id), (", ".join(str(self.postslist[point][0]) for point in rectangle.corners))])
                    pr.addFeatures([feature])
            else:
                return

            if len(self.buildings) > 0:
                QgsMessageLog.logMessage('Creating building layer', self.name, Qgis.Info)
                # Creat results layer in memory
                results_layer = self.iface.addVectorLayer("Polygon?crs=" + self.postlayer.crs().authid(), self.postlayer.name() + "_found_buildings " + self.name, "memory")

                # add basic attributes
                pr = results_layer.dataProvider()
                pr.addAttributes([QgsField("postIds", QVariant.String),
                                  QgsField("rectangleIds", QVariant.String),
                                  QgsField("rectangle_count", QVariant.Int)])
                results_layer.updateFields()

                # get the pointlist of the rectangle for the geom and collect data
                for building in self.buildings:
                    # Geometrie
                    building_geometry = None
                    postIds = []
                    for room in building.rooms:
                        if not building_geometry:
                            building_geometry = QgsGeometry.fromPolygonXY([[QgsPointXY(self.postslist[point][1], self.postslist[point][2]) for point in room.corners]])
                        else:
                            building_geometry.combine(QgsGeometry.fromPolygonXY([[QgsPointXY(self.postslist[point][1], self.postslist[point][2]) for point in room.corners]]))
                        for post in room.corners:
                            postIds.append(post)

                    print(building_geometry)
                    feature = QgsFeature()
                    feature.setGeometry(building_geometry)
                    feature.setAttributes([(", ".join(str(id) for id in postIds)), (", ".join(str(room.id) for room in building.rooms)), str(len(building.rooms))])
                    pr.addFeatures([feature])

            QgsMessageLog.logMessage('Task  completed', self.name, Qgis.Info)

    def cancel(self):
        QgsMessageLog.logMessage( 'Task was cancelled', self.name, Qgis.Info)
        super().cancel()

    def start(self):
        self.manager = QgsApplication.taskManager()
        self.manager.addTask(self)
        QgsMessageLog.logMessage('Starting Task', 'postAAR', Qgis.Info)

    def __repr__(self):
        return  'Task ' + str(self.postlayer) + ', ' + str(self.postlayer_crs) + ', ' + str(self.postid) + ', ' + str(self.maximum_length_of_side) + ', ' + str(self.minimum_length_of_side) + ', ' + str(self.max_area_diff)