# coding:utf-8
import linecache
import os

from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.lang.builder import Builder
from kivy.core.window import Window

Window.size = (1080, 720)

h2StartMkup = "[size=25][b]" # 改ページ処理したい


'''
f = open("alice.txt", "r", encoding="UTF-8")
data = [v for v in f.readlines()]
f.close()

page = 0
'''

class Book(EventDispatcher):
    page = NumericProperty()
    maxPage = 0
    

    def __init__(self, page):
        #self.page=0
        self.columnsize = 20
        with open("alice.txt", "r", encoding="UTF-8") as f:
            self.data = [v for v in f.readlines()]
        self.maxPage = len(self.data) / self.columnsize
        print("maxPage:", self.maxPage)

    
    def lpageShow(self):
        #print("l" + str(self.page))
        tmp = ""
        for i in range(self.columnsize):
            nextColumn = i + self.columnsize*(self.page)
            if nextColumn < len(self.data):
                tmp += self.data[nextColumn]
            else:
                break
        return tmp
    
    def rpageShow(self):
        #print("r" + str(self.page))
        tmp = ""
        for i in range(self.columnsize):
            nextColumn = i + self.columnsize*(self.page+1)
            if nextColumn < len(self.data):
                tmp += self.data[nextColumn]
            else:
                tmp += "fin."
                break
        return tmp
    

class MainScreen(FloatLayout):

    def cb_lTextBtn(self, book, rTextBtn, slider, lPageLabel, rPageLabel, lTextBtn):
        if book.page > 0:
            setattr(book, 'page', book.page-2)
            self.turnpage(book, lTextBtn, rTextBtn, lPageLabel, rPageLabel, slider)


    def cb_rTextBtn(self, book, lTextBtn, slider, lPageLabel, rPageLabel, rTextBtn):
        if book.page < book.maxPage - 1:
            setattr(book, 'page', book.page+2)
            self.turnpage(book, lTextBtn, rTextBtn, lPageLabel, rPageLabel, slider)

    def turnpage(self, book, lTextBtn, rTextBtn, lPageLabel, rPageLabel, slider):
        setattr(lTextBtn, 'text', book.lpageShow())
        setattr(rTextBtn, 'text', book.rpageShow())
        setattr(slider, 'value', book.page)
        setattr(lPageLabel, 'text', str(book.page))
        setattr(rPageLabel, 'text', str(book.page+1))       

    def cb_bookmarkBtn(self, book, button):
        file = 'bookmark.txt'
        if os.path.exists(file):
            os.remove(file)
        with open(file, "w", encoding="UTF-8") as f:
            print(book.page, file=f)
    
    def cb_openBtn(self, book, lTextBtn, rTextBtn, lPageLabel, rPageLabel, slider, button):
        file = 'bookmark.txt'
        if os.path.exists(file):
            with open(file, "r", encoding="UTF-8") as f:
                book.page = int(f.readline())
            self.turnpage(book, lTextBtn, rTextBtn, lPageLabel, rPageLabel, slider)
        

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        '''
        #Button(text="hello")
        #self.add_widget(btn)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        #txt = open("alice.txt", "r", encoding="UTF-8")
        #for line in txt.read():
        btn = Button(text=lines[0], size_hint_y=None, height=40)
        layout.add_widget(btn)
        scr = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.add_widget(scr)
        lbl = Label(text=lines)
        scr.add_widget(lbl)
        
        #txt.close()  
        '''
        fontsize = 20
        columnsize = 20

        book = Book(page=0)

        rootLayout = Factory.BoxLayout(orientation = 'vertical')
        pageLayout = Factory.BoxLayout(orientation='horizontal')
        floatLayout = Factory.FloatLayout()

        #左ページ
        lTextBtn = Factory.Button(text=book.lpageShow(), font_size=fontsize, markup=True,
                                    background_color=[0,.25,.25,1])

        lPageLabel = Label(text="0", font_size=fontsize, size_hint=(.1, .1), pos_hint={'x':.2, 'y':.1})
        floatLayout.add_widget(lPageLabel)

        '''
        lTextBtn.fbind('on_press', self.cb_lTextBtn, book, rTextBtn, slider)
        pageLayout.add_widget(lTextBtn)
        '''

        #右ページ
        rTextBtn = Factory.Button(text=book.rpageShow(), font_size=fontsize, markup=True,
                                    background_color=[0,.25,.25,1])

        rPageLabel = Label(text="1", font_size=fontsize, size_hint=(.1, .1), pos_hint={'x':.7, 'y':.1})
        floatLayout.add_widget(rPageLabel)
        

        '''
        rTextBtn.fbind('on_press', self.cb_rTextBtn, book, lTextBtn, slider)
        pageLayout.add_widget(rTextBtn)
        rootLayout.add_widget(pageLayout)
        '''

        #スライダー
        slider = Factory.Slider(value=1, min=0, max=book.maxPage, step=2, size_hint_y=.1)
        #slider.bind(value=lambda slider, value: setattr(book, 'page', int(int(value)/2)))
        slider.bind(value=lambda slider, value: setattr(book, 'page', int(value)))
        slider.bind(value=lambda slider, value: setattr(lTextBtn, 'text', book.lpageShow()))
        slider.bind(value=lambda slider, value: setattr(rTextBtn, 'text', book.rpageShow()))
        slider.bind(value=lambda slider, value: setattr(lPageLabel, 'text', str(book.page)))
        slider.bind(value=lambda slider, value: setattr(rPageLabel, 'text', str(book.page+1)))

        #ブックマークボタン
        bookmarkBtn = Factory.Button(text="*", size_hint=(.05, .05), pos_hint={'x':.05, 'y':.9})
        bookmarkBtn.fbind('on_press', self.cb_bookmarkBtn, book)
        floatLayout.add_widget(bookmarkBtn)

        #ブックマークを開くボタン
        openBtn = Factory.Button(text="R", size_hint=(.05, .05), pos_hint={'x':.11, 'y':.9})
        openBtn.fbind('on_press', self.cb_openBtn, book, lTextBtn, rTextBtn, lPageLabel, rPageLabel, slider)
        floatLayout.add_widget(openBtn)



        lTextBtn.fbind('on_press', self.cb_lTextBtn, book, rTextBtn, slider, lPageLabel, rPageLabel)
        pageLayout.add_widget(lTextBtn)
        rTextBtn.fbind('on_press', self.cb_rTextBtn, book, lTextBtn, slider, lPageLabel, rPageLabel)
        pageLayout.add_widget(rTextBtn)
        rootLayout.add_widget(pageLayout)
        
        rootLayout.add_widget(slider)
        self.add_widget(rootLayout)
        self.add_widget(floatLayout)


class MainApp(App):
    def build(self):
        MS = MainScreen()
        return MS

if __name__ == "__main__":
    MainApp().run()