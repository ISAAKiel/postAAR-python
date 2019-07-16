    
    def check_dialog_input(self):
        # Input values have to be checked
        postlayer = self.dlg.cmb_layer_selected.currentLayer()
        postid = self.dlg.cmb_postid.currentField()
        maximum_length_of_side = unicode(self.dlg.maximum_length_of_side.text())
        minimum_length_of_side = unicode(self.dlg.minimum_length_of_side.text())
        max_diff_side = unicode(self.dlg.maximal_length_difference.text())
        results_shape = unicode(self.dlg.save_outfile.filePath())

        # Layer selected?

        # CRS is not geografic?
        if postlayer.crs().isGeographic() == True:
            msg = "-  Layer " + postlayer.name() + " is not projected. Please choose an projected reference system. \n"

        # geometry type is point?
        if postlayer.geometryType() != 0:
            msg = msg + "-  Layer " + postlayer.name() + " is not a point geometry. Please choose an point geometry.\n"

        # ID field selected?
        if self.cmb_postid.currentField() == "":
            msg = msg + "-  please select a ID field \n" 

        if int(self.maximum_length_of_side.text()) < int(self.minimum_length_of_side.text()):
            msg = msg + "-  maximal length must be greater or equal to minimal length \n"
            # QMessageBox.information(self, 'postAAR dialog', "please select suitable max and min values")
            # return
        if self.save_outfile.filePath() == "":
            msg = msg + "-  please select a file for the results"
            # return
        QMessageBox.information(self, 'postAAR dialog', msg)
        return FALSE
