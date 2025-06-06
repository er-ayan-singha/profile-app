from kivymd.app import MDApp
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from datetime import datetime
from plyer import notification
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')

class AlarmListItem(OneLineIconListItem):
    def __init__(self, alarm_time, **kwargs):
        super().__init__(**kwargs)
        self.alarm_time = alarm_time
        self.text = f"Alarm: {alarm_time}"

class ModernTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.background_color = (0, 0, 0, 0)  # Transparent background

class ModernAlarmClock(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alarms = []
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        
        # Set window size for mobile-like display
        Window.size = (400, 700)
        
    def build(self):
        # Main layout
        self.tabs = ModernTabbedPanel()
        
        # Clock Tab
        clock_tab = TabbedPanelItem(text='Clock')
        clock_content = MDBoxLayout(orientation='vertical', spacing=10, padding=15)
        
        # Date display
        self.date_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6"
        )
        clock_content.add_widget(self.date_label)
        
        # Time display
        self.time_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Primary",
            font_style="H3"
        )
        clock_content.add_widget(self.time_label)
        
        # Weather display
        self.weather_card = MDCard(
            orientation="vertical",
            padding=15,
            spacing=10,
            size_hint=(1, None),
            height=dp(100)
        )
        self.weather_label = MDLabel(
            text="Loading weather...",
            halign="center"
        )
        self.weather_card.add_widget(self.weather_label)
        clock_content.add_widget(self.weather_card)
        
        clock_tab.add_widget(clock_content)
        self.tabs.add_widget(clock_tab)
        
        # Alarms Tab
        alarms_tab = TabbedPanelItem(text='Alarms')
        alarms_content = MDBoxLayout(orientation='vertical', spacing=10, padding=15)
        
        # Time input for new alarm
        time_input = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))
        self.hour_input = MDRaisedButton(text="00")
        self.minute_input = MDRaisedButton(text="00")
        time_input.add_widget(self.hour_input)
        time_input.add_widget(MDLabel(text=":", halign="center", size_hint_x=None, width=dp(20)))
        time_input.add_widget(self.minute_input)
        
        # Add alarm button
        add_alarm_btn = MDRaisedButton(
            text="Add Alarm",
            on_release=self.add_alarm
        )
        time_input.add_widget(add_alarm_btn)
        alarms_content.add_widget(time_input)
        
        # Alarms list
        scroll = ScrollView()
        self.alarm_list = MDList()
        scroll.add_widget(self.alarm_list)
        alarms_content.add_widget(scroll)
        
        alarms_tab.add_widget(alarms_content)
        self.tabs.add_widget(alarms_tab)
        
        # Stopwatch Tab
        stopwatch_tab = TabbedPanelItem(text='Stopwatch')
        stopwatch_content = MDBoxLayout(orientation='vertical', spacing=10, padding=15)
        
        # Stopwatch display
        self.stopwatch_label = MDLabel(
            text="00:00:00",
            halign="center",
            theme_text_color="Primary",
            font_style="H3"
        )
        stopwatch_content.add_widget(self.stopwatch_label)
        
        # Stopwatch controls
        controls = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))
        self.start_stop_btn = MDRaisedButton(
            text="Start",
            on_release=self.toggle_stopwatch
        )
        self.reset_btn = MDRaisedButton(
            text="Reset",
            on_release=self.reset_stopwatch
        )
        controls.add_widget(self.start_stop_btn)
        controls.add_widget(self.reset_btn)
        stopwatch_content.add_widget(controls)
        
        stopwatch_tab.add_widget(stopwatch_content)
        self.tabs.add_widget(stopwatch_tab)
        
        # Start clock updates
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_stopwatch, 0.1)
        
        # Update weather every 30 minutes
        Clock.schedule_interval(self.update_weather, 1800)
        self.update_weather(0)
        
        return self.tabs
    
    def update_time(self, dt):
        now = datetime.now()
        self.time_label.text = now.strftime("%H:%M:%S")
        self.date_label.text = now.strftime("%A, %B %d, %Y")
        
        # Check alarms
        current_time = now.strftime("%H:%M")
        for alarm in self.alarms:
            if alarm.alarm_time == current_time and not hasattr(alarm, 'triggered'):
                self.trigger_alarm(alarm)
                alarm.triggered = True
    
    def update_stopwatch(self, dt):
        if self.stopwatch_running:
            self.stopwatch_time += dt
            minutes, seconds = divmod(int(self.stopwatch_time), 60)
            hours, minutes = divmod(minutes, 60)
            self.stopwatch_label.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def toggle_stopwatch(self, instance):
        self.stopwatch_running = not self.stopwatch_running
        self.start_stop_btn.text = "Stop" if self.stopwatch_running else "Start"
    
    def reset_stopwatch(self, instance):
        self.stopwatch_time = 0
        self.stopwatch_label.text = "00:00:00"
        self.stopwatch_running = False
        self.start_stop_btn.text = "Start"
    
    def update_weather(self, dt):
        try:
            # Using London as default location - you can modify this to use GPS or user input
            url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                condition = data['weather'][0]['description']
                self.weather_label.text = f"Temperature: {temp}°C\n{condition.capitalize()}"
            else:
                self.weather_label.text = "Weather data unavailable"
        except Exception as e:
            self.weather_label.text = "Weather data unavailable"
    
    def add_alarm(self, instance):
        alarm_time = f"{self.hour_input.text}:{self.minute_input.text}"
        alarm_item = AlarmListItem(alarm_time)
        self.alarm_list.add_widget(alarm_item)
        self.alarms.append(alarm_item)
    
    def trigger_alarm(self, alarm_item):
        notification.notify(
            title='Alarm!',
            message=f'Alarm time: {alarm_item.alarm_time}',
            app_icon=None,
            timeout=10,
        )

if __name__ == '__main__':
    ModernAlarmClock().run() 