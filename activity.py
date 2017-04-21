from gettext import gettext as _

import gtk
import pygame
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
import gobject
import sugargame.canvas
import PJ

class PeterActivity(activity.Activity):
    def __init__(self, handle):
        super(PeterActivity, self).__init__(handle)

        # Build the activity toolbar.
        toolbox = activity.ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.keep.props.visible = False
        activity_toolbar.share.props.visible = False

        toolbox.show()
        self.set_toolbox(toolbox)

        # Create the game instance.
        self.game = PJ.PJ()

        # Build the Pygame canvas.
        self._pygamecanvas = \
            sugargame.canvas.PygameCanvas(self)
        # Note that set_canvas implicitly calls
        # read_file when resuming from the Journal.
        self.set_canvas(self._pygamecanvas)

        # Start the game running.
        self._pygamecanvas.run_pygame(self.game.run)

    def read_file(self, file_path):
        try:
            f = open(file_path, "r")
        except:
            return #****
        try:
            self.game.success=int(f.readline())
        except:
            pass
        f.close()

    def write_file(self, file_path):
        f = open(file_path, 'wb')
        try:
            f.write(str(self.game.success)+'\n')
        finally:
            f.close()
