"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class BadgerXBlock(XBlock):
    """
    This XBlock will play an MP3 file as an HTML5 badger element. 
    """

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the BadgerXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/badger.html")
        #print html.format
        html = html.replace("CSS", self.resource_string("static/css/badger.css"))
        frag = Fragment(html)
        #frag.add_css(self.resource_string("static/css/badger.css"))
        frag.add_javascript(self.resource_string("static/js/src/badger.js"))
        frag.initialize_js('BadgerXBlock')
        print self.xml_text_content()
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("BadgerXBlock",
             """<vertical_demo>
                  <badger> 
                    edX platform/edx.png : dialog/dialog.png
                    cleaner/cleaner.png 
                    mentor/mentor.png : sage/sage.png
                  </badger>
                </vertical_demo>
             """),
        ]

    
