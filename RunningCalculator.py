from datetime import timedelta
import json
from numpy import interp
import PickerView
import ui

class ChangeSubview( ui.View ):
	def __init__(self, num_pickers = 2, separator = ':', vals = [range(5,30), range(0,59)]):
		#
		# THE NEW STYLE
		# make a new class
		# Have all selectors pre-made in advance
		# Speed: Ones, Tenths, Hundreths
		# Pace: Minutes, Seconds
		# Time: Hours, Minutes, Seconds
		# 
		# These will basically be laid out on top of each other.
		# Then selectively hide & show those as necessary.
		
		#self.frame = [0,0,600,600]
		self.background_color = 'white'
		self.delegate_and_datasource = PickerView.UIPickerViewDataSourceAndDelegate.alloc().init().autorelease()
		self.num_pickers = num_pickers
		self.separator = separator
		x = 90
		dx = 50
		db = ui.ButtonItem(title='Done')
		db.action = self.change_set
		self.right_button_items = [db]
		l = ui.Label(frame=[x,0,40,40])
		l.alignment = ui.ALIGN_CENTER
		self.add_subview(l)
		for i in range(0, num_pickers):
			if(i!=0):
				ls = ui.Label(frame=[x-dx/2+2, 35,40,100], text=self.separator)
				ls.alignment = ui.ALIGN_CENTER
				self.add_subview(ls)
			pv = PickerView.UIPickerViewWrapper(frame=[x,30,40,100])
			pv.data_source = self.delegate_and_datasource
			pv.delegate = self.delegate_and_datasource
			pv.name = 'chg'+str(i)
			self.add_subview(pv)
			x = x + dx
			#print(PickerView._data)
		pv = dict()
		type_name = 'speed'
		print(type_name)
		pv[type_name+'_ones'] = PickerView.UIPickerViewWrapper(frame=[90,30,40,100])
		pv[type_name+'_ones'].data_source = self.delegate_and_datasource
		pv[type_name+'_ones'].delegate = self.delegate_and_datasource
		pv[type_name+'_ones'].name = type_name+'_ones'
		self.add_subview(pv[type_name+'_ones'])
		self[type_name+'_ones'].hidden = True
		speed_pvs = [ pv[type_name+'_ones'] ]
		pv[type_name+'_tenths'] = PickerView.UIPickerViewWrapper(frame=[140,30,40,100])
		pv[type_name+'_tenths'].data_source = self.delegate_and_datasource
		pv[type_name+'_tenths'].delegate = self.delegate_and_datasource
		pv[type_name+'_tenths'].name = type_name+'_tenths'
		self.add_subview(pv[type_name+'_tenths'])
		self[type_name+'_tenths'].hidden = True
		speed_pvs.append( pv[type_name+'_tenths'] )
		
	def change_set(self, sender):
		pass

class ChangePopup( ui.View ):
	def __init__(self):
		self.background_color = 'white'
		self.delegate_and_datasource = PickerView.UIPickerViewDataSourceAndDelegate.alloc().init().autorelease()
		db = ui.ButtonItem(title='Done')
		db.action = self.change_set
		self.right_button_items = [db]
		
		x = 90
		y = 30
		dx = 50
		dy = 0
		w = 40
		h = 100
		pv_names = [	'speed_ones', 'speed_tenths', 'speed_hundreths', 
									'pace_hours', 'pace_minutes', 'pace_seconds',
									'time_hours', 'time_minutes', 'time_seconds' ]
		pv_range = [	range(1,16), 	range(0,10),	range(0,10),
									range(0,2),		range(0,60),	range(0,60),
									range(0,10),	range(0,60),	range(0,60) ]
		PickerView._data = [list(map(str,x)) for x in pv_range]
		for type in range(0,3):
			f = [x, y, w, h]
			for place in range(0,3):
				i = 3*place + type 
				print('name[{}]: {}'.format(i, pv_names[i]) )
				pv = PickerView.UIPickerViewWrapper(frame=f)
				pv.data_source = self.delegate_and_datasource
				pv.delegate = self.delegate_and_datasource
				pv.name = pv_names[i]
				self.add_subview(pv)
				pv.hidden = True
				pv.tag = i
			x = x + dx
			
	def change_set(self, sender):
		pass
				
	def chg_controls(self, arr):
		self['speed_ones'].hidden = arr[0]
		self['speed_tenths'].hidden = arr[1]
		self['speed_hundreths'].hidden = arr[2]
		self['pace_hours'].hidden = arr[3]
		self['pace_minutes'].hidden = arr[4]
		self['pace_seconds'].hidden = arr[5]
		self['time_hours'].hidden = arr[6]
		self['time_minutes'].hidden = arr[7]
		self['time_seconds'].hidden = arr[8]
	
	def show_speed_controls(self):
		self.chg_controls( [False, False, False, 
												True, True, True,
												True, True, True])
		
	def show_pace_controls(self):
		self.chg_controls( [True, True, True, 
												False, False, False,
												True, True, True])
		
		
	def show_time_controls(self):
		self.chg_controls( [True, True, True, 
												True, True, True,
												False, False, False])
		
	def set_speed(self, mph):
		pass
		
	def set_pace(self, sec_per_mile):
		pass
		
	def set_time(self, seconds):
		pass
		
	def get_result(self):
		new_min = self.sv['chg1']._picker_view.selectedRowInComponent(0)
		return [5.0, 5.0]
		
	def get_speed(self):
		return 8.2
		
	def get_pace(self):
		return 480.0
		
	def get_time(self):
		return 900.0
	
class RunningView( ui.View ):
	def __init__(self):
		self.background_color = 'white'
		self.load_data()
		x = 50
		dx = 75
		self.delegate_and_datasource = PickerView.UIPickerViewDataSourceAndDelegate.alloc().init().autorelease()
		PickerView._data =  [
			[str(x) for x in range(1, 15)],	# speed in mph
			[str(x) for x in range(0, 99)], # hundreths
			[str(x) for x in range(0, 59)], # minutes
			[str(x) for x in range(0, 10)]  # hours
		]
		text_y = 30
		dy = 30
		x_l = 10
		x_s = 120
		x_p = 180
		x_t = 250
		
		w_l = 110
		w_s = 60
		w_p = 60
		w_t = 70
		h_font = ('<system-bold>', 16)
		hl = ui.Label(frame=(x_l, 0, w_l, dy))
		hl.text = "Distance"
		hl.font = h_font
		self.add_subview(hl)
		hs = ui.Label(frame=(x_s, 0, w_s, dy))
		hs.text = "Speed"
		hs.font = h_font
		hs.alignment = ui.ALIGN_CENTER
		self.add_subview(hs)
		hp = ui.Label(frame=(x_p, 0, w_p, dy))
		hp.text = "Pace"
		hp.font = h_font
		hp.alignment = ui.ALIGN_CENTER
		self.add_subview(hp)
		ht = ui.Label(frame=(x_t, 0, w_t, dy))
		ht.text = "Time"
		ht.font = h_font
		ht.alignment = ui.ALIGN_CENTER
		self.add_subview(ht)
		for r in self.j['run']:
			l = ui.Label(frame=(x_l, text_y, w_l, dy))
			l.name = r+'_name'
			l.text = r
			s = ui.Button(frame=(x_s, text_y, w_s, dy))
			s.name = r+'_speed'
			s.action = self.button_pressed
			p = ui.Button(frame=(x_p, text_y, w_p, dy))
			p.name = r+'_pace'
			p.action = self.button_pressed
			t = ui.Button(frame=(x_t, text_y, w_t, dy))
			t.name = r+'_time'
			t.action = self.button_pressed
			self.add_subview(l)
			self.add_subview(p)
			self.add_subview(s)
			self.add_subview(t)
		
			text_y = text_y + dy
		self.sv = ui.View()
		self.sv.background_color = 'white'
		#ranges = [ range(1,15), range(0,99)]
		#self.v_chg_speed = ChangeSubview(separator='.')
		#self.v_chg_speed['chg0'].tag = 1
		#self.v_chg_pace = ChangeSubview()
		#ranges = [ range(0,9), range(0,59), range(0,59)]
		#self.v_chg_time = ChangeSubview(num_pickers=3, vals=ranges)
		
		self.chg_view = ChangePopup()
		
	def draw(self):
		#r_font = self['5k_name'].font
		#print(r_font)
		r_font = ('<system>', 17)
		b_font = ('<system-bold>', 17)
		for rn in self.j['run']:
			row = self.get_row_text(rn)
			self[rn+'_pace'].title = row['pace']
			self[rn+'_speed'].title = row['speed']
			self[rn+'_time'].title = row['time']
			if (rn == self.set_run_name):
				self[rn+'_name'].font = b_font
				self[rn+'_name'].text_color = 'red'
				self[rn+'_pace'].font = b_font
				self[rn+'_speed'].font = b_font
				self[rn+'_time'].font = b_font
			else:
				self[rn+'_name'].font = r_font
				self[rn+'_name'].text_color = 'black'
				self[rn+'_pace'].font = r_font
				self[rn+'_speed'].font = r_font
				self[rn+'_time'].font = r_font
			
		
	def load_data(self):
		filename = 'runs.json'
		json_data = open(filename)
		self.j = json.load(json_data)	
		json_data.close()
		self.set_run_name = self.j['set_run_name']
		self.set_run_speed = self.j['set_run_speed']
		#self.set_5k_speed = 1.0
		self.set_5k()
				
	def set_5k(self):
		if (self.set_run_name != '5k'):
			#print(self.j['run'][self.set_run_name]['run_mph'])
			#print(self.j['run'][self.set_run_name]['5k_mph'])
			#print(self.set_run_speed)
			[m, b] = self.j['run'][self.set_run_name]['polyfit']
			self.set_5k_speed = (self.set_run_speed - b) / m
			#self.set_5k_speed = interp( self.set_run_speed, self.j['run'][self.set_run_name]['run_mph'], self.j['run'][self.set_run_name]['5k_mph'] )
			#print('e5k '+ str(self.set_5k_speed))
		else:
			self.set_5k_speed = self.set_run_speed
			print('5k speed alreafy set to: '+ str(self.set_5k_speed))
			
	def get_row_text(self, run_name):
		row = dict()
		[m, b] = self.j['run'][run_name]['polyfit']
		speed = m*self.set_5k_speed + b
		#speed = interp( self.set_5k_speed, self.j['run'][run_name]['5k_mph'], self.j['run'][run_name]['run_mph'] )
		#print('speed: ', speed)
		#print('speed: {0:%3.1f}'.format(speed))
		pace = 3600.0/speed
		row['name']=run_name
		(mins, secs) = divmod(pace, 60)
		row['pace']='{0:d}:{1:02d}'.format(int(mins),int(secs))
		#print(row['pace'])
		row['speed'] = str(round(speed,2))
		if( 'miles' in self.j['run'][run_name] ):
			distance = self.j['run'][run_name]['miles']
			secs = distance * pace
			row['time']=str( timedelta( seconds = round(secs) ))
		else:
			row['time'] = ''
		return row
				
	def button_pressed(self, sender):
		print(sender.name)
		rn = sender.name.split('_', 1)[0]
		action = sender.name.split('_', 1)[1]
		print('action: '+action)
		db = ui.ButtonItem(title='Done')
		db.action = self.change_set
		self.sv.right_button_items = [db]
		
		if (action == 'pace'):
			print('pace pressed')
			start_pace = self[sender.name].title.split(':')
			start_min = int(start_pace[0])
			start_sec = int(start_pace[1])
			print('start_min: {}'.format(start_min))
			self.sv.name = rn + ' pace'
			l_min = ui.Label(frame=[90,0,40,30], text='min')
			l_min.alignment = ui.ALIGN_CENTER
			self.sv.add_subview(l_min)
			pv_min = PickerView.UIPickerViewWrapper(frame=[90,30,40,100])
			pv_min.data_source = self.delegate_and_datasource
			pv_min.delegate = self.delegate_and_datasource
			pv_min.name = 'pv_min'
			self.sv.add_subview(pv_min)
			sep = ui.Label(frame=[135,55,10,50], text=':')
			self.sv.add_subview(sep)
			l_sec = ui.Label(frame=[140,0,40,30], text='sec')
			l_sec.alignment = ui.ALIGN_CENTER
			self.sv.add_subview(l_sec)
			pv_sec = PickerView.UIPickerViewWrapper(frame=[140,30,40,100])
			pv_sec.data_source = self.delegate_and_datasource
			pv_sec.delegate = self.delegate_and_datasource
			pv_sec.name = 'pv_sec'
			self.sv.add_subview(pv_sec)
			print('start_sec: {}'.format(start_sec))
			pv_min._picker_view.selectRow_inComponent_animated_(start_min, 0, False)
			pv_sec._picker_view.selectRow_inComponent_animated_(start_sec, 0, False)
			self.sv.present()
			
		elif (action == 'speed'):
			print('speed pressed')
			#self.v_chg_speed.name = rn + ' speed'
			speed = float(self[rn+'_speed'].title)
			ones = round(speed)
			tenths = round(10*(speed-ones))
			#self.v_chg_speed['chg0']._picker_view.selectRow_inComponent_animated_(ones, 0, False)
			#self.v_chg_speed['chg1']._picker_view.selectRow_inComponent_animated_(tenths, 0, False)
			
			#self.v_chg_speed.present()
			self.chg_view.show_speed_controls()
			self.chg_view.present()
			
		elif (action == 'time'):
			print('time pressed')
			self.sv.name = rn + ' time'
			self.chg_view.show_time_controls()
			self.chg_view.present()
			#self.v_chg_time.present()
		else:
			 print('who knows?')
			 return
		
		
	def change_set(self, sender):
		print('need to find which to set')
		print('this item set: '+self.sv.name)
		#print(self.sv['pv_sec'].name)
		#jprint(dir(self.sv['pv_sec']._picker_view))
		new_min = self.sv['pv_min']._picker_view.selectedRowInComponent(0)
		new_sec = self.sv['pv_sec']._picker_view.selectedRowInComponent(0)
		print('{}:{:02d}'.format(new_min,new_sec))
		self.set_run_name = self.sv.name.rsplit(' ',1)[0]
		self.set_run_speed = 3600 / (60*new_min+new_sec)
		self.set_5k()
		self.sv.close()
		self.v_chg_speed.close()
		self.set_needs_display()
'''
		for r in run_list:
			l = ui.Label(frame=(x1, text_y, 140, dy))
			l.text = r.get_name()
			p = ui.Button(frame=(x2, text_y, w2, dy))
			p.title = r.get_pace_text()
			p.action = r.button_pressed
			s = ui.Button(frame=(x3, text_y, w3, dy))
			s.title = r.get_speed_text()
			s.action = r.button_pressed
			t = ui.Button(frame=(x4, text_y, w4, dy))
			t.title = r.get_time_text()
			t.action = r.button_pressed
		
			if (r.get_name() == r.set_run):
				l.font = h_font
				l.text_color = 'red'
				p.font = h_font
#				p.text_color = 'red'
				s.font = h_font
#				s.text_color = 'red'
				t.font = h_font
#				t.text_color = 'red'
			
			self.add_subview(l)
			self.add_subview(p)
			self.add_subview(s)
			self.add_subview(t)
		
			text_y = text_y + dy
'''
	
if __name__ == '__main__':
	v = RunningView()
	v.present()


'''		l5 = ui.Label(frame=(x1, text_y, 140, dy))
		l5.text = "5k"
		self.add_subview(l5)
		p5 = ui.Button(frame=(x2, text_y, w2, dy))
		p5.name = '5k_pace'
		p5.title = '8:08'
		self.add_subview(p5)
		s5 = ui.Button(frame=(x3, text_y, w3, dy))
		s5.name = '5k_speed'
		s5.title = '7.2'
		self.add_subview(s5)
		t5 = ui.Button(frame=(x4, text_y, w4, dy))
		t5.name = '5k_time'
		t5.title = "21:00"
		self.add_subview(t5)
		text_y = text_y + dy
'''
		
