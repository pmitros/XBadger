"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

learning_map = [
    {'title':"Getting started", 'row':0, 'element':1, 'status':'active'},
    {'title':"Constructive learning" , 'row':1, 'element':1, 'status':'inactive', 
     'children' : [
            {'title':'Constructive learning: Intro'}, 
            {'title':'Constructive learning: Examplar'}, 
            {'title':'Constructive learning: Discuss'}, 
            {'title':'Constructive learning: Make'},
            {'title':'Constructive learning: Review'}]},
    {'title':"OERs" , 'row':2, 'element':1, 'status':'inactive'}, 
    {'title':"Blended Learning" , 'row':2, 'element':2, 'status':'inactive'},
    {'title':"Peer review", 'row':5, 'element':1, 'status':'active'},
    ]

#learning_map = [{'title':"Getting started", 'row':0, 'element':0, 'status':'active'}]

def transform_layout(learning_map):
    ''' Convert a learning_map into a hex grid of items
    '''
    rows = max([l['element'] for l in learning_map])+1
    cols = max([l['row'] for l in learning_map])+1
    layout = [[None]*rows for a in [None]*cols]
    for item in learning_map:
        layout[item['row']][item['element']] = item
    return layout

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
        layout_html = ""
        for line in transform_layout(learning_map):
            layout_html = layout_html + '<div class="hex-row">'
            for item in line: 
                if not item: 
                    item = {'title':'','status':'invisible'}
                div = '<div class="'+item['status']+'-hex"><div style="text-align:center">' + item['title'] + '</div></div>'
                layout_html = layout_html + div
            layout_html = layout_html + '</div>'
        print layout_html
        html = html.replace("CSS", self.resource_string("static/css/badger.css"))
        html = html.replace("LAYOUT", layout_html)
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

    
