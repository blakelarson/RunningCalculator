# coding: utf-8

from objc_util import ObjCInstance, c, ObjCClass, ns, create_objc_class, NSObject
from ctypes import c_void_p
import ui
import arrow


# Data for four pickers
_data = [
    [str(x) for x in range(0,10)],
    [str(x) for x in range(0, 24)],
    [str(x) for x in range(0,60)],
    [str(x) for x in range(0,60)],
]

# ObjC classes
UIColor = ObjCClass('UIColor')
UIPickerView = ObjCClass('UIPickerView')
UIFont = ObjCClass('UIFont')
NSAttributedString = ObjCClass('NSAttributedString')


# Default attributes, no need to recreate them again and again
def _str_symbol(name):
    return ObjCInstance(c_void_p.in_dll(c, name))


_default_attributes = {
    _str_symbol('NSFontAttributeName'): UIFont.fontWithName_size_(ns('Courier'), 16),
    _str_symbol('NSForegroundColorAttributeName'): UIColor.blackColor(),
    _str_symbol('NSBackgroundColorAttributeName'): UIColor.whiteColor()
}


# Data source & delegate methods
def pickerView_attributedTitleForRow_forComponent_(self, cmd, picker_view, row, component):
    tag = ObjCInstance(picker_view).tag()
    return NSAttributedString.alloc().initWithString_attributes_(ns(_data[tag - 1][row]), ns(_default_attributes)).ptr


def pickerView_titleForRow_forComponent_(self, cmd, picker_view, row, component):
    tag = ObjCInstance(picker_view).tag()
    return ns(_data[tag - 1][row]).ptr


def pickerView_numberOfRowsInComponent_(self, cmd, picker_view, component):
    tag = ObjCInstance(picker_view).tag()
    return len(_data[tag - 1])


def numberOfComponentsInPickerView_(self, cmd, picker_view):
    return 1


def rowSize_forComponent_(self, cmd, picker_view, component):
    return 100


def pickerView_rowHeightForComponent_(self, cmd, picker_view, component):
    return 30


def pickerView_didSelectRow_inComponent_(self, cmd, picker_view, row, component):
    tag = ObjCInstance(picker_view).tag()
    print(f'Did select {_data[tag - 1][row]}')


methods = [
    numberOfComponentsInPickerView_, pickerView_numberOfRowsInComponent_,
    rowSize_forComponent_, pickerView_rowHeightForComponent_, pickerView_attributedTitleForRow_forComponent_,
    pickerView_didSelectRow_inComponent_
]

protocols = ['UIPickerViewDataSource', 'UIPickerViewDelegate']


UIPickerViewDataSourceAndDelegate = create_objc_class(
    'UIPickerViewDataSourceAndDelegate', NSObject, methods=methods, protocols=protocols
)


# UIPickerView wrapper which behaves like ui.View (in terms of init, layout, ...)
class UIPickerViewWrapper(ui.View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._picker_view = UIPickerView.alloc().initWithFrame_(ObjCInstance(self).bounds()).autorelease()
        ObjCInstance(self).addSubview_(self._picker_view)

    def layout(self):
        self._picker_view.frame = ObjCInstance(self).bounds()

    @property
    def tag(self):
        return self._picker_view.tag()

    @tag.setter
    def tag(self, x):
        self._picker_view.setTag_(x)

    @property
    def delegate(self):
        return self._picker_view.delegate()

    @delegate.setter
    def delegate(self, x):
        self._picker_view.setDelegate_(x)

    @property
    def data_source(self):
        return self._picker_view.dataSource()

    @data_source.setter
    def data_source(self, x):
        self._picker_view.setDataSource_(x)

class MyTimerTest(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_color = 'white'
        self.countdown_time = arrow.now().shift(days=+3, hours=+1, minutes=+3)
        self.make_view()
        self.update_interval = 1

    def make_view(self):
        
        self.delegate_and_datasource = UIPickerViewDataSourceAndDelegate.alloc().init().autorelease()
        
        x = 50
        dx = 100
        dy = 100
        for i in range(0,4):
          l = ui.Label(frame=(x,50,dx,dy))
          l.text = ['day','hour','min','sec'][i]
          l.alignment = ui.ALIGN_CENTER
          self.add_subview(l)
          pv = UIPickerViewWrapper(frame=[x, 100, dx, dy])
          pv.name = l.text
          pv.delegate = self.delegate_and_datasource
          pv.data_source = self.delegate_and_datasource
          pv._picker_view.userInteractionEnabled = False
          
          pv.tag = i + 1
          self.add_subview(pv)
          x = x + dx

    def update(self):
        #self.update_interval = 30 if self.update_interval == 1 else 1
        td = self.countdown_time - arrow.now()
        self.name = str(td)
        self.disp_counters(td)
        
    def disp_counters(self,td):
        days  = td.days
        secs  = td.seconds
        hours = int(secs/3600)
        secs  = secs - hours*3600
        mins  = int(secs/60)
        secs  = secs - mins*60
        self['day']._picker_view.selectRow_inComponent_animated_(days, 0, True)
        self['hour']._picker_view.selectRow_inComponent_animated_(hours, 0, True)
        self['min']._picker_view.selectRow_inComponent_animated_(mins, 0, True)
        self['sec']._picker_view.selectRow_inComponent_animated_(secs, 0, True)

if __name__ == '__main__':
    f = (0, 0, 500, 480)
    tt = MyTimerTest(frame=f)
    tt.present('sheet')
