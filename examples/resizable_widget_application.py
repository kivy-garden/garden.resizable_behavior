from __future__ import print_function
from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import cm
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.graphics import *
from kivy.clock import Clock

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from behaviors.resize import ResizableBehavior

class ResizableLabel(ResizableBehavior, Label):
    def __init__(self, **kwargs):
        super(ResizableLabel, self).__init__(**kwargs)
        self.background = Rectangle(pos=self.pos, size=self.size)
        blue2 = InstructionGroup()
        blue2.add(Color(0.5, 0.5, 0.5, 1))
        blue2.add(self.background)
        self.canvas.before.add(blue2)
        self.bind(size=lambda obj, val: setattr(
            self.background, 'pos', self.pos))
        self.bind(size=self.on_size2)

    def on_size2(self, _, val):
        self.text_size = val
        self.background.size = val


class ResizableButton(ResizableBehavior, Button):
    pass


class ResizableSideBar(ResizableBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(ResizableSideBar, self).__init__(**kwargs)
        self.background = Rectangle(pos=self.pos, size=self.size)
        self.resizable_right = True

    def after_init(self):
        for x in range(1, 10):
            lbl = Label(size_hint=(1, None), height=(cm(1)), text='X '+str(x))
            self.add_widget(lbl)
        self.bind(size=lambda obj, val: setattr(
            self.background, 'size', self.size))
        self.bind(size=lambda obj, val: setattr(
            self.background, 'pos', self.pos))
        blue = InstructionGroup()
        blue.add(Color(0.6, 0.6, 0.7, 1))
        blue.add(self.background)
        self.canvas.before.add(blue)


class ResizableStackLayout(ResizableBehavior, StackLayout):
    bgcl = ListProperty([1, 1, 1, 1])
    def __init__(self, bgcl, **kwargs):
        super(ResizableStackLayout, self).__init__(**kwargs)
        self.bgcl = bgcl
        self.background = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=lambda obj, val: setattr(self.background, 'size', val))
        self.bind(pos=lambda obj, val: setattr(self.background, 'pos', val))
        blue = InstructionGroup()
        blue.add(Color(*self.bgcl))
        blue.add(self.background)
        self.canvas.before.add(blue)


class ResizableWidgetDemo(FloatLayout):
    def __init__(self, **kwargs):
        super(ResizableWidgetDemo, self).__init__(**kwargs)
        self.stack0 = StackLayout(size_hint=(1, 1))
        self.sidebar = ResizableSideBar(
            size_hint=(None, 1), width=cm(4.5), orientation='vertical')
        self.stack1 = StackLayout(
            size_hint=(None, 1), width=self.width-cm(4.5))
        self.stack2 = ResizableStackLayout(
            [0.7, 0.2, 0.2, 1], size_hint=(1, None),
            height=cm(5), resizable_down=True)
        self.stack3 = ResizableStackLayout(
            [0.2, 0.2, 0.7, 1], size_hint=(1, None))
        rbutton = ResizableButton(
            text='down, left resizable button \n in resizable stacklayout',
            resizable_right = True,
            resizable_down = True,
            size_hint=(None, None),
            size=(cm(6), cm(4)),
            on_release=lambda x: print('ON_RELASE()')
        )
        sidelabel = ResizableLabel(
            text='Reizable button \nin resizable sidebar',
            resizable_down = True,
            dont_move=True,
            size_hint=(1, None),
            height=cm(1),
        )
        r4sides = ResizableButton(
            text='4 sides resizable,\n floating button\n with size limit',
            resizable_right = True,
            resizable_left = True,
            resizable_up = True,
            resizable_down = True,
            size_hint=(None, None),
            min_resizable_width=cm(3),
            min_resizable_height=cm(3),
            max_resizable_width=cm(10),
            max_resizable_height=cm(10),
            resizable_border_offset = 14,
            size=(cm(6), cm(6)),
            on_release=lambda x: print('ON_RELASE()')
        )
        self.add_widget(self.stack0)
        self.stack0.add_widget(self.sidebar)
        self.stack0.add_widget(self.stack1)
        self.sidebar.add_widget(sidelabel)
        self.stack1.add_widget(self.stack2)
        self.stack1.add_widget(self.stack3)
        self.stack2.add_widget(rbutton)
        self.add_widget(r4sides)
        self.sidebar.after_init()
        self.sidebar.bind(size=lambda obj, val: setattr(
            self.stack1, 'width', self.width - val[0]))
        self.stack2.bind(size=lambda obj, val: setattr(
            self.stack3, 'height', self.height - val[1]))

class ResizableWidgetDemoApp(App):
    def build(self):
        return ResizableWidgetDemo()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    ResizableWidgetDemoApp().run()
