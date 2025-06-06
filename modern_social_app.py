from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
import webbrowser
import urllib.parse

# Set window size
Window.size = (400, 700)

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<CustomButton@MDRaisedButton>:
    size_hint_x: 1
    md_bg_color: app.theme_cls.primary_color
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    font_size: "18sp"
    size_hint_y: None
    height: dp(50)
    elevation: 3

MDScreen:
    canvas:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        md_bg_color: 0, 0, 0, 1

        MDCard:
            orientation: 'vertical'
            padding: dp(15)
            spacing: dp(15)
            size_hint: None, None
            size: dp(320), dp(600)
            pos_hint: {'center_x': .5, 'center_y': .5}
            elevation: 3
            radius: [dp(20)]
            md_bg_color: app.theme_cls.primary_dark
            line_color: app.theme_cls.primary_color

            MDCard:
                size_hint: None, None
                size: dp(280), dp(280)
                pos_hint: {'center_x': .5}
                radius: [dp(20)]
                elevation: 2
                padding: dp(4)
                md_bg_color: app.theme_cls.primary_light
                line_color: app.theme_cls.primary_color

                MDLabel:
                    text: "Profile Photo\\n(Place RECENT.jpg here)"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.9, 0.9, 0.9, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}

            MDLabel:
                text: "Connect With Me"
                font_style: "H5"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                size_hint_y: None
                height: self.texture_size[1]
                padding_y: dp(20)

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(10)
                adaptive_height: True

                CustomButton:
                    text: "LinkedIn"
                    icon: "linkedin"
                    md_bg_color: get_color_from_hex("#0077B5")
                    on_release: app.open_link("https://www.linkedin.com/in/er-ayan-singha")

                CustomButton:
                    text: "Facebook"
                    icon: "facebook"
                    md_bg_color: get_color_from_hex("#4267B2")
                    on_release: app.open_link("https://www.facebook.com/er.ayan.singha")

                CustomButton:
                    text: "Email"
                    icon: "email"
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.send_email()

                CustomButton:
                    text: "YouTube"
                    icon: "youtube"
                    md_bg_color: get_color_from_hex("#FF0000")
                    on_release: app.open_link("https://www.youtube.com/")

                CustomButton:
                    text: "My Projects"
                    icon: "folder-account"
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.open_link("https://www.youtube.com/")
'''

class ModernSocialApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)
    
    def open_link(self, url):
        print(f"Opening link: {url}")
        webbrowser.open(url)

    def send_email(self):
        print("Sending email")
        recipient = "singhaayanray07@gmail.com"
        subject = urllib.parse.quote("Hello from the Modern Social App")
        body = urllib.parse.quote("Hi Ayan, I saw your profile and wanted to connect with you!")
        webbrowser.open(f"mailto:{recipient}?subject={subject}&body={body}")

if __name__ == '__main__':
    ModernSocialApp().run() 