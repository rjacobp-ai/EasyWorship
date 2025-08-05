from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.utils import platform
import requests
from bs4 import BeautifulSoup
import re

class EasyWorshipApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical' if platform == 'android' else 'horizontal'
        self.padding = 5
        self.spacing = 5
        
        # Set background color
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.versions = [
            ("KJV", "King James Version"),
            ("ESV", "English Standard Version"),
            ("NIV", "New International Version"),
            ("NLT", "New Living Translation"),
            ("NASB", "New American Standard Bible"),
            ("NKJV", "New King James Version"),
            ("AMP", "Amplified Bible"),
            ("MSG", "The Message"),
            ("CSB", "Christian Standard Bible"),
            ("RSV", "Revised Standard Version"),
            ("APSD-CEB", "Bisaya Bible Version")
        ]
        
        self.selected_version = "KJV"
        self.build_ui()
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def build_ui(self):
        if platform == 'android':
            self.build_mobile_ui()
        else:
            self.build_desktop_ui()
    
    def build_mobile_ui(self):
        # Mobile-optimized layout
        main_scroll = ScrollView()
        main_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        main_content.bind(minimum_height=main_content.setter('height'))
        
        # Scripture Search Section
        scripture_section = BoxLayout(orientation='vertical', size_hint_y=None, height=140, spacing=5)
        
        scripture_title = Label(text='Scripture Search', font_size=18, bold=True, 
                               size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1))
        scripture_section.add_widget(scripture_title)
        
        self.scripture_input = TextInput(
            text='John 3:16', 
            multiline=False, 
            size_hint_y=None, 
            height=50,
            font_size=16
        )
        scripture_section.add_widget(self.scripture_input)
        
        search_btn = Button(
            text='Search Scripture', 
            size_hint_y=None, 
            height=50,
            background_color=(0.2, 0.5, 0.8, 1),
            font_size=16
        )
        search_btn.bind(on_press=self.show_scripture)
        scripture_section.add_widget(search_btn)
        
        main_content.add_widget(scripture_section)
        
        # Bible Versions Section
        version_section = BoxLayout(orientation='vertical', size_hint_y=None, height=300, spacing=5)
        
        version_title = Label(text='Bible Versions', font_size=18, bold=True, 
                             size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1))
        version_section.add_widget(version_title)
        
        version_scroll = ScrollView(size_hint_y=None, height=250)
        version_grid = GridLayout(cols=3, size_hint_y=None, spacing=5)
        version_grid.bind(minimum_height=version_grid.setter('height'))
        
        self.version_buttons = []
        for abbr, full_name in self.versions:
            btn = ToggleButton(
                text=abbr, 
                size_hint_y=None, 
                height=50, 
                group='version',
                font_size=14,
                background_color=(0.8, 0.8, 0.8, 1) if abbr != "KJV" else (0.3, 0.6, 0.9, 1)
            )
            if abbr == "KJV":
                btn.state = 'down'
            btn.bind(on_press=lambda x, v=abbr: self.select_version(v))
            self.version_buttons.append(btn)
            version_grid.add_widget(btn)
        
        version_scroll.add_widget(version_grid)
        version_section.add_widget(version_scroll)
        main_content.add_widget(version_section)
        
        # Navigation Section
        nav_section = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        
        nav_title = Label(text='Navigation', font_size=18, bold=True, 
                         size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1))
        nav_section.add_widget(nav_title)
        
        nav_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        prev_btn = Button(
            text='< Previous',
            background_color=(0.6, 0.3, 0.3, 1),
            font_size=16
        )
        prev_btn.bind(on_press=lambda x: self.change_verse(-1))
        nav_buttons.add_widget(prev_btn)
        
        next_btn = Button(
            text='Next >',
            background_color=(0.3, 0.6, 0.3, 1),
            font_size=16
        )
        next_btn.bind(on_press=lambda x: self.change_verse(1))
        nav_buttons.add_widget(next_btn)
        
        nav_section.add_widget(nav_buttons)
        main_content.add_widget(nav_section)
        
        # Display Area
        display_section = BoxLayout(orientation='vertical', size_hint_y=None, height=400, spacing=5)
        
        display_title = Label(text='Scripture Display', font_size=18, bold=True, 
                             size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1))
        display_section.add_widget(display_title)
        
        display_scroll = ScrollView(size_hint_y=None, height=350)
        self.display_label = Label(
            text='Welcome to Easy Worship App\n\nSelect a scripture and tap Search.', 
            text_size=(None, None), 
            size_hint_y=None,
            valign='top',
            font_size=16,
            color=(0.1, 0.1, 0.1, 1)
        )
        self.display_label.bind(texture_size=self.display_label.setter('size'))
        display_scroll.add_widget(self.display_label)
        display_section.add_widget(display_scroll)
        
        main_content.add_widget(display_section)
        
        # Project Button
        project_btn = Button(
            text='Project to Screen',
            size_hint_y=None, 
            height=60,
            background_color=(0.7, 0.2, 0.7, 1),
            font_size=18
        )
        project_btn.bind(on_press=self.project_text)
        main_content.add_widget(project_btn)
        
        # Lyrics Section
        lyrics_section = BoxLayout(orientation='vertical', size_hint_y=None, height=250, spacing=5)
        
        lyrics_title = Label(text='Worship Lyrics', font_size=18, bold=True, 
                           size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1))
        lyrics_section.add_widget(lyrics_title)
        
        self.lyrics_input = TextInput(
            multiline=True, 
            size_hint_y=None, 
            height=150,
            hint_text='Enter worship lyrics here...',
            font_size=16
        )
        lyrics_section.add_widget(self.lyrics_input)
        
        lyrics_btn = Button(
            text='Show Lyrics', 
            size_hint_y=None, 
            height=60,
            background_color=(0.8, 0.6, 0.2, 1),
            font_size=16
        )
        lyrics_btn.bind(on_press=self.show_lyrics)
        lyrics_section.add_widget(lyrics_btn)
        
        main_content.add_widget(lyrics_section)
        
        main_scroll.add_widget(main_content)
        self.add_widget(main_scroll)
    
    def build_desktop_ui(self):
        # Left Panel (Controls)
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.35, padding=10, spacing=10)
        with left_panel.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            left_panel.rect = Rectangle(size=left_panel.size, pos=left_panel.pos)
        left_panel.bind(size=self._update_panel_rect, pos=self._update_panel_rect)
        
        # Scripture Search Section
        scripture_section = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        
        scripture_title = Label(text='Scripture Search', font_size=16, bold=True, 
                               size_hint_y=None, height=30, color=(0.2, 0.2, 0.2, 1))
        scripture_section.add_widget(scripture_title)
        
        self.scripture_input = TextInput(
            text='John 3:16', 
            multiline=False, 
            size_hint_y=None, 
            height=40,
            font_size=14,
            background_color=(1, 1, 1, 1)
        )
        scripture_section.add_widget(self.scripture_input)
        
        search_btn = Button(
            text='Search Scripture', 
            size_hint_y=None, 
            height=40,
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        search_btn.bind(on_press=self.show_scripture)
        scripture_section.add_widget(search_btn)
        
        left_panel.add_widget(scripture_section)
        
        # Bible Version Section
        version_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=5)
        
        version_title = Label(text='Bible Versions', font_size=16, bold=True, 
                             size_hint_y=None, height=30, color=(0.2, 0.2, 0.2, 1))
        version_section.add_widget(version_title)
        
        version_scroll = ScrollView(size_hint_y=None, height=160)
        version_grid = GridLayout(cols=2, size_hint_y=None, spacing=3)
        version_grid.bind(minimum_height=version_grid.setter('height'))
        
        self.version_buttons = []
        for abbr, full_name in self.versions:
            btn = ToggleButton(
                text=abbr, 
                size_hint_y=None, 
                height=35, 
                group='version',
                font_size=12,
                background_color=(0.8, 0.8, 0.8, 1) if abbr != "KJV" else (0.3, 0.6, 0.9, 1)
            )
            if abbr == "KJV":
                btn.state = 'down'
            btn.bind(on_press=lambda x, v=abbr: self.select_version(v))
            self.version_buttons.append(btn)
            version_grid.add_widget(btn)
        
        version_scroll.add_widget(version_grid)
        version_section.add_widget(version_scroll)
        left_panel.add_widget(version_section)
        
        # Navigation Section
        nav_section = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        
        nav_title = Label(text='Navigation', font_size=16, bold=True, 
                         size_hint_y=None, height=30, color=(0.2, 0.2, 0.2, 1))
        nav_section.add_widget(nav_title)
        
        nav_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        
        prev_btn = Button(
            text='< Prev', 
            background_color=(0.6, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        prev_btn.bind(on_press=lambda x: self.change_verse(-1))
        nav_buttons.add_widget(prev_btn)
        
        next_btn = Button(
            text='Next >', 
            background_color=(0.3, 0.6, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        next_btn.bind(on_press=lambda x: self.change_verse(1))
        nav_buttons.add_widget(next_btn)
        
        nav_section.add_widget(nav_buttons)
        
        # Project button
        project_btn = Button(
            text='Project to Screen', 
            size_hint_y=None, 
            height=40,
            background_color=(0.7, 0.2, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        project_btn.bind(on_press=self.project_text)
        nav_section.add_widget(project_btn)
        
        left_panel.add_widget(nav_section)
        
        # Lyrics Section
        lyrics_section = BoxLayout(orientation='vertical', spacing=5)
        
        lyrics_title = Label(text='Worship Lyrics', font_size=16, bold=True, 
                           size_hint_y=None, height=30, color=(0.2, 0.2, 0.2, 1))
        lyrics_section.add_widget(lyrics_title)
        
        self.lyrics_input = TextInput(
            multiline=True, 
            size_hint_y=None, 
            height=150,
            hint_text='Enter worship lyrics here...',
            background_color=(1, 1, 1, 1)
        )
        lyrics_section.add_widget(self.lyrics_input)
        
        lyrics_btn = Button(
            text='Show Lyrics', 
            size_hint_y=None, 
            height=40,
            background_color=(0.8, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        lyrics_btn.bind(on_press=self.show_lyrics)
        lyrics_section.add_widget(lyrics_btn)
        
        left_panel.add_widget(lyrics_section)
        
        self.add_widget(left_panel)
        
        # Right Panel (Display Area)
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.65, padding=10, spacing=10)
        with right_panel.canvas.before:
            Color(1, 1, 1, 1)  # White background
            right_panel.rect = Rectangle(size=right_panel.size, pos=right_panel.pos)
        right_panel.bind(size=self._update_panel_rect, pos=self._update_panel_rect)
        
        # Display title
        display_title = Label(
            text='Scripture Display', 
            font_size=18, 
            bold=True, 
            size_hint_y=None, 
            height=40,
            color=(0.2, 0.2, 0.2, 1)
        )
        right_panel.add_widget(display_title)
        
        # Main display area
        display_scroll = ScrollView()
        self.display_label = Label(
            text='[size=20][b]Welcome to Easy Worship App[/b][/size]\n\n[size=14]Select a scripture reference and click "Search Scripture" to begin.[/size]', 
            text_size=(None, None), 
            size_hint_y=None,
            valign='top',
            markup=True,
            font_size=16,
            color=(0.1, 0.1, 0.1, 1)
        )
        self.display_label.bind(texture_size=self.display_label.setter('size'))
        
        # Set initial text_size for the welcome message
        def set_initial_text_size(*args):
            right_panel_width = (self.width * 0.65) - 40
            self.display_label.text_size = (right_panel_width, None)
        
        # Bind to size changes and set initial size
        self.bind(size=set_initial_text_size)
        self.bind(on_kv_post=set_initial_text_size)  # Set after widget is fully created
        
        display_scroll.add_widget(self.display_label)
        right_panel.add_widget(display_scroll)
        
        # Status bar
        status_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        with status_bar.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            status_bar.rect = Rectangle(size=status_bar.size, pos=status_bar.pos)
        status_bar.bind(size=self._update_panel_rect, pos=self._update_panel_rect)
        
        self.status_label = Label(
            text='Ready', 
            font_size=12, 
            color=(0.3, 0.3, 0.3, 1)
        )
        status_bar.add_widget(self.status_label)
        right_panel.add_widget(status_bar)
        
        self.add_widget(right_panel)

    def _update_panel_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    # Copy all your existing methods here (select_version, get_verse, show_scripture, etc.)
    def select_version(self, version):
        self.selected_version = version
        
        for btn in self.version_buttons:
            if btn.text == version:
                btn.background_color = (0.3, 0.6, 0.9, 1)
            else:
                btn.background_color = (0.8, 0.8, 0.8, 1)
        
        if hasattr(self, 'display_label') and 'Welcome' not in self.display_label.text:
            self.show_scripture(None)
    
    def get_verse(self, passage, version):
        try:
            url = f"https://www.biblegateway.com/passage/?search={passage}&version={version}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                content_div = soup.find("div", class_="passage-text")
                if content_div:
                    for tag in content_div.find_all(["sup", "a"]):
                        tag.decompose()
                    verses = content_div.get_text(separator=" ", strip=True)
                    verses = re.sub(r'\s+', ' ', verses).strip()
                    return verses
            return "Could not retrieve verse."
        except:
            return "Error retrieving verse."
    
    def show_scripture(self, instance):
        ref = self.scripture_input.text
        verse = self.get_verse(ref, self.selected_version)
        full_name = next((name for code, name in self.versions if code == self.selected_version), self.selected_version)
        
        if platform == 'android':
            formatted_text = f"{ref} ({self.selected_version})\n\n{verse}"
            # Set text_size for mobile
            def update_mobile_text_size(*args):
                self.display_label.text_size = (self.width - 40, None)
            self.bind(width=update_mobile_text_size)
            update_mobile_text_size()
        else:
            formatted_text = f"[size=22][b]{ref}[/b][/size]\n[size=14]({self.selected_version} - {full_name})[/size]\n\n[size=18]{verse}[/size]"
            # Set text_size for desktop - use right panel width
            def update_desktop_text_size(*args):
                # Calculate the right panel width (65% of total width minus padding)
                right_panel_width = (self.width * 0.65) - 40
                self.display_label.text_size = (right_panel_width, None)
            self.bind(width=update_desktop_text_size)
            update_desktop_text_size()
        
        self.display_label.text = formatted_text

    def show_lyrics(self, instance):
        lyrics = self.lyrics_input.text
        if platform == 'android':
            self.display_label.text = f"Worship Lyrics\n\n{lyrics}"
            # Set text_size for mobile
            def update_mobile_text_size(*args):
                self.display_label.text_size = (self.width - 40, None)
            self.bind(width=update_mobile_text_size)
            update_mobile_text_size()
        else:
            self.display_label.text = f"[size=24][b]Worship Lyrics[/b][/size]\n\n[size=18]{lyrics}[/size]"
            # Set text_size for desktop - use right panel width
            def update_desktop_text_size(*args):
                # Calculate the right panel width (65% of total width minus padding)
                right_panel_width = (self.width * 0.65) - 40
                self.display_label.text_size = (right_panel_width, None)
            self.bind(width=update_desktop_text_size)
            update_desktop_text_size()

    def change_verse(self, delta):
        ref = self.scripture_input.text
        match = re.match(r"([A-Za-z ]+)\s+(\d+):(\d+)", ref)
        if match:
            book = match.group(1)
            chapter = int(match.group(2))
            verse = int(match.group(3)) + delta
            if verse < 1:
                verse = 1
            new_ref = f"{book} {chapter}:{verse}"
            self.scripture_input.text = new_ref
            self.show_scripture(None)
    
    def project_text(self, instance):
        try:
            from kivy.uix.popup import Popup
            from kivy.graphics import Color, Rectangle
            from kivy.clock import Clock
            
            # Get the text to display first
            display_text = self.display_label.text
            clean_text = re.sub(r'\[/?[^\]]*\]', '', display_text)
            
            # Create a simple popup with ScrollView for long text
            content = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Set black background
            with content.canvas.before:
                Color(0, 0, 0, 1)
                content.rect = Rectangle(size=content.size, pos=content.pos)
            content.bind(size=lambda inst, val: setattr(content.rect, 'size', inst.size))
            content.bind(pos=lambda inst, val: setattr(content.rect, 'pos', inst.pos))
            
            # Add ScrollView for text that might be too long
            scroll = ScrollView()
            
            # Create the label with smaller initial font size
            project_label = Label(
                text=clean_text,
                font_size=32,  # Start smaller - was 72
                text_size=(600, None),  # Fixed width that works well
                size_hint_y=None,  # Allow manual height
                valign='top',  # Start from top
                halign='center',
                color=(1, 1, 1, 1)
            )
            
            # Bind texture size to label size for proper scrolling
            project_label.bind(texture_size=project_label.setter('size'))
            
            scroll.add_widget(project_label)
            content.add_widget(scroll)
            
            # Control buttons
            button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
            
            smaller_btn = Button(text='A-', size_hint_x=0.25, background_color=(0.2, 0.5, 0.8, 1))
            larger_btn = Button(text='A+', size_hint_x=0.25, background_color=(0.2, 0.5, 0.8, 1))
            bg_toggle_btn = Button(text='Toggle BG', size_hint_x=0.25, background_color=(0.5, 0.5, 0.5, 1))
            close_btn = Button(text='Close', size_hint_x=0.25, background_color=(0.8, 0.2, 0.2, 1))
            
            button_layout.add_widget(smaller_btn)
            button_layout.add_widget(larger_btn)
            button_layout.add_widget(bg_toggle_btn)
            button_layout.add_widget(close_btn)
            
            content.add_widget(button_layout)
            
            popup = Popup(
                title='Scripture Projection',
                content=content,
                size_hint=(0.95, 0.95),
                auto_dismiss=False
            )
            
            # Function to update text size based on popup width
            def update_text_size(*args):
                if hasattr(popup, 'width') and popup.width > 0:
                    project_label.text_size = (popup.width - 100, None)
                    project_label.texture_update()
            
            # Button functions with text size update
            def make_smaller(*args):
                if project_label.font_size > 16:
                    project_label.font_size -= 4  # Smaller increments
                    update_text_size()
            
            def make_larger(*args):
                if project_label.font_size < 80:
                    project_label.font_size += 4  # Smaller increments
                    update_text_size()
            
            bg_is_black = [True]
            def toggle_background(*args):
                with content.canvas.before:
                    content.canvas.before.clear()
                    if bg_is_black[0]:
                        Color(1, 1, 1, 1)  # White
                        project_label.color = (0, 0, 0, 1)  # Black text
                        bg_is_black[0] = False
                    else:
                        Color(0, 0, 0, 1)  # Black
                        project_label.color = (1, 1, 1, 1)  # White text
                        bg_is_black[0] = True
                    content.rect = Rectangle(size=content.size, pos=content.pos)
            content.bind(size=lambda inst, val: setattr(content.rect, 'size', inst.size))
            content.bind(pos=lambda inst, val: setattr(content.rect, 'pos', inst.pos))
            
            # Bind buttons
            smaller_btn.bind(on_press=make_smaller)
            larger_btn.bind(on_press=make_larger)
            bg_toggle_btn.bind(on_press=toggle_background)
            close_btn.bind(on_press=popup.dismiss)
            
            # Bind popup width changes
            popup.bind(width=update_text_size)
            
            # Update status
            if hasattr(self, 'status_label'):
                self.status_label.text = 'Text projected - Use A+/A- to resize'
                popup.bind(on_dismiss=lambda x: setattr(self.status_label, 'text', 'Projection closed'))
            
            popup.open()
            
            # Force text size update after popup opens
            Clock.schedule_once(lambda dt: update_text_size(), 0.1)
            
        except Exception as e:
            print(f"Error in project_text: {e}")
            if hasattr(self, 'status_label'):
                self.status_label.text = f'Projection error: {str(e)}'

class EasyWorshipAppApp(App):
    def build(self):
        return EasyWorshipApp()

if __name__ == '__main__':
    EasyWorshipAppApp().run()