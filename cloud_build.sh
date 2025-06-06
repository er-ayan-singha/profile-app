#!/bin/bash

# Create project directory
mkdir modern_profile_app
cd modern_profile_app

# Create main.py
cat > main.py << 'EOL'
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy_garden.mapview import MapView, MapMarker
import webbrowser
import urllib.parse

# Set window size to match phone screen dimensions
Window.size = (360, 640)  # Common phone resolution
Window.left = 100  # Position window on screen
Window.top = 100

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Window kivy.core.window.Window
#:import MapView kivy_garden.mapview.MapView
#:import MapMarker kivy_garden.mapview.MapMarker

<SocialStatCard>:
    orientation: 'vertical'
    padding: dp(12)
    spacing: dp(8)
    size_hint: None, None
    size: dp(140), dp(100)  # Made wider and taller
    radius: [dp(20)]
    elevation: 2
    md_bg_color: get_color_from_hex("#1F1F1F")
    line_color: get_color_from_hex("#673AB7")  # Deep Purple
    ripple_behavior: True  # Add this line
    
    MDIcon:
        icon: root.icon
        halign: "center"
        font_size: dp(36)  # Bigger icon
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#673AB7")  # Deep Purple
    
    MDLabel:
        text: root.count
        halign: "center"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_style: "Body1"  # Bigger text
        bold: True

<GlassmorphicCard@MDCard>:
    md_bg_color: get_color_from_hex("#1F1F1F")
    radius: [dp(25)]
    elevation: 1
    line_color: get_color_from_hex("#673AB7")

<LocationCard>:
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(10)
    md_bg_color: get_color_from_hex("#1F1F1F")
    radius: [dp(25)]
    elevation: 1
    line_color: get_color_from_hex("#673AB7")
    size_hint_y: None
    height: dp(300)
    
    MDLabel:
        text: "My Location"
        halign: "center"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#673AB7")
        font_style: "H6"
        bold: True
        adaptive_height: True
        padding: [0, dp(5)]
    
    MapView:
        id: mapview
        lat: 22.5726453  # Exact latitude
        lon: 88.3638924  # Exact longitude
        zoom: 17      # Closer zoom for better detail
        min_zoom: 8   # Regional view
        max_zoom: 18  # Detailed view
        size_hint_y: None
        height: dp(230)
        double_tap_zoom: True
        on_map_relocated: root.update_marker()
        
        MDIconButton:
            icon: "plus"
            pos_hint: {"right": 0.98, "top": 0.98}
            on_release: mapview.zoom += 1 if mapview.zoom < mapview.max_zoom else 0
            md_bg_color: get_color_from_hex("#673AB7")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        
        MDIconButton:
            icon: "minus"
            pos_hint: {"right": 0.98, "top": 0.88}
            on_release: mapview.zoom -= 1 if mapview.zoom > mapview.min_zoom else 0
            md_bg_color: get_color_from_hex("#673AB7")
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

MDScreen:
    canvas.before:
        Color:
            rgba: get_color_from_hex("#000000")
        Rectangle:
            pos: self.pos
            size: self.size
        
        # Subtle gradient overlay
        Color:
            rgba: get_color_from_hex("#673AB7") + [0.05]  # Very subtle purple tint
        Rectangle:
            pos: self.pos[0], 0
            size: self.size[0], self.size[1] * 0.3
    
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(15)
            padding: dp(15)
            adaptive_height: True  # Important for scrolling
            
            # Profile Card
            GlassmorphicCard:
                orientation: 'vertical'
                padding: dp(15)
                spacing: dp(10)
                size_hint_y: None
                height: dp(400)  # Profile card height
                
                # Avatar Card
                MDCard:
                    size_hint: None, None
                    size: dp(80), dp(80)
                    pos_hint: {"center_x": .5}
                    radius: [dp(40)]
                    md_bg_color: get_color_from_hex("#673AB7")
                    padding: dp(3)
                    elevation: 4
                    
                    AsyncImage:
                        source: "avatar_placeholder.png"
                        size_hint: 1, 1
                        pos_hint: {"center_x": .5, "center_y": .5}
                        radius: [dp(37)]
                
                # Name and Username
                MDLabel:
                    text: "Ayan Singha"
                    halign: "center"
                    font_style: "H6"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                
                MDLabel:
                    text: "@er-ayan-singha"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#673AB7")
                    font_style: "Body1"
                
                # Social Stats - First Row
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(15)
                    adaptive_height: True
                    pos_hint: {"center_x": .5}
                    padding: [0, dp(10)]
                    
                    SocialStatCard:
                        icon: "facebook"
                        count: "Facebook"
                        on_release: app.open_facebook()
                    
                    SocialStatCard:
                        icon: "github"
                        count: "GitHub"
                        on_release: app.open_github()
                
                # Social Stats - Second Row
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(15)
                    adaptive_height: True
                    pos_hint: {"center_x": .5}
                    padding: [0, dp(10)]
                    
                    SocialStatCard:
                        icon: "email"
                        count: "Email Me"
                        on_release: app.send_email()
                    
                    SocialStatCard:
                        icon: "linkedin"
                        count: "LinkedIn"
                        on_release: app.open_linkedin()
            
            # Location Card
            LocationCard:
                id: location_card
                pos_hint: {"center_x": .5}
                
            # Add some space at the bottom for better scrolling
            Widget:
                size_hint_y: None
                height: dp(20)
'''

class SocialStatCard(MDCard, RoundedRectangularElevationBehavior):
    icon = StringProperty()
    count = StringProperty()
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(elevation=4, d=0.2).start(self)
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(elevation=2, d=0.2).start(self)
        return super().on_touch_up(touch)

class LocationCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marker = None
    
    def on_kv_post(self, base_widget):
        # Add marker after MapView is initialized
        mapview = self.ids.mapview
        self.marker = MapMarker(lat=mapview.lat, lon=mapview.lon)
        mapview.add_marker(self.marker)
    
    def update_marker(self, *args):
        if self.marker:
            mapview = self.ids.mapview
            self.marker.lat = mapview.lat
            self.marker.lon = mapview.lon

class ModernSocialApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)
    
    def open_facebook(self):
        webbrowser.open("https://www.facebook.com/er.ayan.singha")
    
    def open_github(self):
        webbrowser.open("https://github.com/er-ayan-singha")
    
    def send_email(self):
        recipient = "singhaayanray07@gmail.com"
        subject = urllib.parse.quote("Hello from your Profile App")
        body = urllib.parse.quote("Hi Ayan,\n\nI'd like to connect with you!")
        webbrowser.open(f"mailto:{recipient}?subject={subject}&body={body}")
    
    def open_linkedin(self):
        webbrowser.open("https://www.linkedin.com/in/er-ayan-singha")

if __name__ == '__main__':
    ModernSocialApp().run()
EOL

# Create buildozer.spec
cat > buildozer.spec << 'EOL'
[app]
title = Modern Social Profile
package.name = modernsocialprofile
package.domain = org.ayan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = assets/*,images/*
version = 0.1
requirements = python3,kivy==2.0.0,kivymd==1.0.2,kivy_garden.mapview,pillow,requests,urllib3,certifi
orientation = portrait
fullscreen = 0
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.skip_update = False
android.accept_sdk_license = True
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

[buildozer]
log_level = 2
warn_on_root = 1
EOL

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip build-essential git python3 python3-dev
sudo apt-get install -y libssl-dev
sudo apt-get install -y libffi-dev
sudo apt-get install -y libltdl-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y openjdk-11-jdk
sudo apt-get install -y autoconf
sudo apt-get install -y libtool
sudo apt-get install -y pkg-config
sudo apt-get install -y zip unzip

# Install buildozer
pip3 install --user --upgrade buildozer

# Build the APK
buildozer android debug

echo "Build complete! Your APK should be in the ./bin directory" 