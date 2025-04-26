import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
from bs4 import BeautifulSoup
import time

class HackerJSONGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("LANAVYN JSON Generator")
        self.root.configure(bg='black')
        
        # Set hacker font (Courier is commonly available)
        self.font = ('Courier', 12)
        
        # Create intro animation
        self.create_intro()
        
        # After intro, setup main interface
        self.root.after(3000, self.setup_ui)
    
    def create_intro(self):
        self.intro_frame = tk.Frame(self.root, bg='black')
        self.intro_frame.pack(expand=True, fill='both')
        
        self.intro_label = tk.Label(
            self.intro_frame, 
            text="", 
            fg='#00ff00', 
            bg='black', 
            font=('Courier', 14, 'bold')
        )
        self.intro_label.pack(expand=True)
        
        intro_text = "LANAVYN\n/owner Rakha\n\nInitializing JSON Generator..."
        self.animate_text(self.intro_label, intro_text, 0)
    
    def animate_text(self, label, text, index):
        if index < len(text):
            current = label.cget("text") + text[index]
            label.config(text=current)
            self.root.after(50, lambda: self.animate_text(label, text, index + 1))
        else:
            time.sleep(1)
    
    def setup_ui(self):
        # Clear intro
        self.intro_frame.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Input label and text area
        input_label = tk.Label(
            main_frame, 
            text="/jso [html or text to convert to JSON]", 
            fg='#00ff00', 
            bg='black', 
            font=self.font,
            anchor='w'
        )
        input_label.pack(fill='x')
        
        self.input_text = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            fg='#00ff00',
            bg='black',
            insertbackground='#00ff00',
            font=self.font,
            wrap=tk.WORD
        )
        self.input_text.pack(expand=True, fill='both', pady=(0, 10))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(fill='x')
        
        generate_btn = tk.Button(
            button_frame,
            text="Generate JSON",
            command=self.generate_json,
            fg='black',
            bg='#00ff00',
            font=self.font,
            relief='flat',
            bd=0
        )
        generate_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_input,
            fg='black',
            bg='#00ff00',
            font=self.font,
            relief='flat',
            bd=0
        )
        clear_btn.pack(side='left')
        
        # Output label and text area
        output_label = tk.Label(
            main_frame, 
            text="JSON Output:", 
            fg='#00ff00', 
            bg='black', 
            font=self.font,
            anchor='w'
        )
        output_label.pack(fill='x')
        
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            fg='#00ff00',
            bg='black',
            font=self.font,
            wrap=tk.WORD,
            state='disabled'
        )
        self.output_text.pack(expand=True, fill='both')
        
        # Status bar
        self.status = tk.Label(
            main_frame,
            text="Ready",
            fg='#00ff00',
            bg='black',
            font=self.font,
            anchor='w'
        )
        self.status.pack(fill='x')
        
        # Bind Enter key to generate JSON
        self.root.bind('<Return>', lambda event: self.generate_json())
    
    def generate_json(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        
        if not input_data:
            self.update_status("Error: No input provided")
            messagebox.showerror("Error", "Please enter some text or HTML to convert to JSON")
            return
        
        try:
            # Try to parse as HTML
            soup = BeautifulSoup(input_data, 'html.parser')
            
            # If it's HTML, create a JSON structure
            if len(soup.find_all()) > 0:
                result = {
                    "html": str(soup),
                    "text": soup.get_text(),
                    "tags": [tag.name for tag in soup.find_all()],
                    "links": [a.get('href') for a in soup.find_all('a') if a.get('href')]
                }
                json_data = json.dumps(result, indent=2)
            else:
                # If not HTML, treat as plain text
                result = {
                    "input": input_data,
                    "length": len(input_data),
                    "words": input_data.split(),
                    "lines": input_data.split('\n')
                }
                json_data = json.dumps(result, indent=2)
            
            # Display the JSON
            self.output_text.config(state='normal')
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, json_data)
            self.output_text.config(state='disabled')
            
            self.update_status("JSON generated successfully")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate JSON: {str(e)}")
    
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state='disabled')
        self.update_status("Cleared input and output")
    
    def update_status(self, message):
        self.status.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    
    # Make window resizable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    app = HackerJSONGenerator(root)
    root.mainloop()
