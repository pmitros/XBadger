"""TO-DO: Write a description of what this XBlock is."""

import math

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

learning_map = [
    {'title':"Getting started", 'row':0, 'element':1, 'status':'active'},
    {'title':"Constructive learning" , 'row':1, 'element':1, 'status':'inactive', 
     'children' : [
            {'title':'Intro'}, 
            {'title':'Examplar'}, 
            {'title':'Discuss'}, 
            {'title':'Make'},
            {'title':'Review'}]},
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

def html_line(x1, y1, x2, y2):
    ''' HTML+CSS needed to draw a line from x1,y1 to x2,y2 relative to
    the current position in the HTML. 
    '''
    html = '<div style="position:absolute"><div style="position:relative; top:{top}px; left:{left}px; transform:rotate({angle}deg);-webkit-transform:rotate({angle}deg);-ms-transform:rotate({angle}deg);"><div style="height:3px; background:#000; width:{width}px;"></div></div></div>'
    rad = math.atan2(y2-y1, x2-x1)
    angle = rad/math.pi*180.
    width = math.sqrt((x2-x1)**2+(y2-y1)**2)
    top = (y1+y2)/2.
    center = (x1+x2)/2.
    left = center - width /2
    return html.format(angle=angle, top=top, left=left, width=width)

child_layout = '''
      <div style="position:absolute; width:1024px;"><div style="position:relative; top:{top}px; left:{left}px; overflow:visible; width:1024px;">{title}</div></div>
      <!--div style="position:absolute"><div style="position:relative; top:5px; left:100px; transform:rotate(-30deg);-webkit-transform:rotate(-30deg);-ms-transform:rotate(-30deg);"><div style="height:3px; background:#000; width:20px;"></div></div></div>
      <div style="position:absolute"><div style="position:relative; top:0px; left:117px; transform:rotate(0deg);-webkit-transform:rotate(0deg);-ms-transform:rotate(0deg);"><div style="height:3px; background:#000; width:20px;"></div></div></div-->
'''

def layout_item(item):
    if not item: 
        item = {}

    for key, value in [('title',''),('status','invisible'), ('children',[])]:
        if key not in item:
            item[key] = value

    children = ""
    yoffset = 0
    for child in item['children']:
        children = children + child_layout.format(left=140,top = -7+yoffset, **child)
        yoffset = yoffset+20

    div = '<div class="'+item['status']+'-hex">'+children+'<div style="text-align:center">' + item['title'] + '</div></div>'
    return div

def layout_line(line):
    new_item_html = '<div class="hex-row">'
    for item in line: 
        new_item_html = new_item_html + layout_item(item)
    new_item_html = new_item_html + '</div>'
    return new_item_html

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
        layout_html = ""
        for line in transform_layout(learning_map):
            new_item_html = layout_line(line)
            layout_html = layout_html + new_item_html
        html = html.replace("CSS", self.resource_string("static/css/badger.css"))
        html = html.replace("LAYOUT", layout_html)

        

        # circle = ""
        # for x in range(0,101,10):
        #     circle = circle + html_line(x, 0, 100-x, 100)

        # circle = circle + html_line(50, -50, 50, 150)

        circle = "" #html_line(0,0,0,100) + html_line(0,100,100,200) + html_line(100,200,200,200) + html_line(200,200,300,100) + html_line(300,100,300,0)

        html = html.replace('CIRCLE', circle)

        frag = Fragment(html)
        #frag.add_css(self.resource_string("static/css/badger.css"))
        frag.add_javascript(self.resource_string("static/js/src/badger.js"))
        frag.initialize_js('BadgerXBlock')
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
