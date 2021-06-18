"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import remi.gui as gui
from remi import start, App
from threading import Timer


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def idle(self):
        self.counter.set_text('Running Time: ' + str(self.count))

    def main(self):
        # the margin 0px auto centers the main container
        verticalContainer = gui.Container(width=540, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        horizontalContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='0px', style={'display': 'block', 'overflow': 'auto'})
        
        subContainerLeft = gui.Container(width=320, style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        self.img = gui.Image('/res:logo.png', height=100, margin='10px')
        self.img.onclick.do(self.on_img_clicked)

        self.table = gui.Table.new_from_list([('Day', 'Grain Level'),
                                   ('DATEVALUE', 'SOME VALUE'),
                                   ('DATEVALUE', 'SOME VALUE'),
                                   ('DATEVALUE', 'SOME VALUE'),
                                   ('DATEVALUE', 'SOME VALUE'),
                                   ('DATEVALUE', 'SOME VALUE')], width=300, height=200, margin='10px')

        self.table.on_table_row_click.do(self.on_table_row_click)

        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Container(style={'width': '220px', 'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        self.count = 0
        self.counter = gui.Label('', width=200, height=30, margin='10px')

        self.lbl = gui.Label('EXAMPLE LABEL!', width=200, height=30, margin='10px')

        self.bt = gui.Button('EXAMPLE BUTTON', width=200, height=30, margin='10px')
        # setting the listener for the onclick event of the button
        self.bt.onclick.do(self.on_button_pressed)

        self.link = gui.Link("http://localhost:8081", "EXAMPLE LINK", width=200, height=30, margin='10px')
        
        # appending a widget to another, the first argument is a string key
        subContainerRight.append([self.counter, self.lbl, self.bt, self.link])
        # use a defined key as we replace this widget later
        self.subContainerRight = subContainerRight

        subContainerLeft.append([self.img, self.table])

        horizontalContainer.append([subContainerLeft, subContainerRight])

        verticalContainer.append([horizontalContainer])

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = False 

        # kick of regular display of counter
        self.display_counter()

        # returning the root widget
        return verticalContainer

    def display_counter(self):
        self.count += 1
        if not self.stop_flag:
            Timer(1, self.display_counter).start()

    # listener function
    def on_img_clicked(self, widget):
        self.lbl.set_text('Image clicked!')

    def on_table_row_click(self, table, row, item):
        self.lbl.set_text('Table Item clicked: ' + item.get_text())

    def on_button_pressed(self, widget):
        self.lbl.set_text('EXAMPLE BUTTON ')
        self.bt.set_text('Hi!')

    def on_close(self):
        """ Overloading App.on_close event to stop the Timer.
        """
        self.stop_flag = True
        super(MyApp, self).on_close()


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)
