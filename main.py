import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from google import genai

class YouTubeCommenterApp(App):
    def build(self):
        self.title = "Gemini AI YouTube Persona Commenter"
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        layout.add_widget(Label(text="Gemini YouTube Commenter", font_size='22sp', bold=True))
        
        layout.add_widget(Label(text="Gemini API Key:", size_hint_y=None, height=25))
        self.api_key_input = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.api_key_input)
        
        layout.add_widget(Label(text="YouTube Video URL:", size_hint_y=None, height=25))
        self.url_input = TextInput(hint_text="https://www.youtube.com/watch?v=...", multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.url_input)
        
        layout.add_widget(Label(text="Select Comment Persona:", size_hint_y=None, height=25))
        self.persona_spinner = Spinner(
            text='Friendly Viewer',
            values=('Friendly Viewer', 'Tech Expert', 'Funny & Sarcastic', 'Supportive Fan', 'Critical Reviewer', 'Short & Hype'),
            size_hint_y=None, height=40
        )
        layout.add_widget(self.persona_spinner)

        layout.add_widget(Label(text="Select Comment Language:", size_hint_y=None, height=25))
        self.lang_spinner = Spinner(
            text='English',
            values=('English', 'Malayalam', 'Manglish', 'Hindi', 'Tamil', 'Telugu', 'Spanish', 'Auto-Detect Video Language'),
            size_hint_y=None, height=40
        )
        layout.add_widget(self.lang_spinner)
        
        self.post_btn = Button(text="Generate Comment", background_color=(0.1, 0.6, 0.8, 1), size_hint_y=None, height=50)
        self.post_btn.bind(on_press=self.process_comment)
        layout.add_widget(self.post_btn)
        
        self.status_label = Label(text="Status: Ready", color=(0.8, 0.8, 0.8, 1))
        layout.add_widget(self.status_label)
        
        return layout

    def process_comment(self, instance):
        api_key = self.api_key_input.text.strip()
        video_url = self.url_input.text.strip()
        persona = self.persona_spinner.text
        language = self.lang_spinner.text
        
        if not api_key or not video_url:
            self.status_label.text = "Error: Please fill in API Key and Video URL!"
            return
            
        self.status_label.text = "Generating comment via Gemini AI..."
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"Write a natural 1-2 sentence YouTube comment for video: {video_url}. Persona: {persona}. Language: {language}."
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            self.status_label.text = f"Generated Comment ({language}):\n{response.text.strip()}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

if __name__ == "__main__":
    YouTubeCommenterApp().run()
