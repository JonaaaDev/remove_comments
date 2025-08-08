#JonathanGIZ
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import tokenize
import io

class ModernCommentRemoverApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Python Comment Remover")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkLabel(
            self.root, 
            text="Python Comment Remover", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, pady=15)
        
        button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        
        self.input_text = ctk.CTkTextbox(
            button_frame, 
            wrap="word", 
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_width=2,
            border_color="#3a7ebf"
        )
        self.input_text.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        
        self.output_text = ctk.CTkTextbox(
            button_frame, 
            wrap="word", 
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_width=2,
            border_color="#3a7ebf"
        )
        self.output_text.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
        
        input_label = ctk.CTkLabel(button_frame, text="Input Code", font=ctk.CTkFont(size=16, weight="bold"))
        input_label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        
        output_label = ctk.CTkLabel(button_frame, text="Cleaned Code", font=ctk.CTkFont(size=16, weight="bold"))
        output_label.grid(row=1, column=1, sticky="w", padx=(10, 0))
        
        control_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        control_frame.grid(row=2, column=0, pady=10)
        
        button_style = {
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 8,
            "height": 40,
            "width": 150
        }
        
        self.load_btn = ctk.CTkButton(
            control_frame, 
            text="Load File", 
            command=self.load_file,
            **button_style
        )
        self.load_btn.grid(row=0, column=0, padx=10)
        
        self.process_btn = ctk.CTkButton(
            control_frame, 
            text="Remove Comments", 
            command=self.remove_comments,
            **button_style,
            fg_color="#1a6fff",
            hover_color="#1450cc"
        )
        self.process_btn.grid(row=0, column=1, padx=10)
        
        self.save_btn = ctk.CTkButton(
            control_frame, 
            text="Save Output", 
            command=self.save_file,
            **button_style
        )
        self.save_btn.grid(row=0, column=2, padx=10)
        
        self.clear_btn = ctk.CTkButton(
            control_frame, 
            text="Clear All", 
            command=self.clear_text,
            **button_style,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        self.clear_btn.grid(row=0, column=3, padx=10)
        
        self.status_label = ctk.CTkLabel(
            self.root, 
            text="Ready to process Python files", 
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=3, column=0, pady=5)
        
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", content)
                    self.status_label.configure(text=f"Loaded: {file_path}")
            except Exception as e:
                self.status_label.configure(text=f"Error loading file: {str(e)}")
    
    def remove_comments(self):
        input_code = self.input_text.get("1.0", "end")
        if not input_code.strip():
            self.status_label.configure(text="No input code to process")
            return
            
        try:
            tokens = tokenize.tokenize(io.BytesIO(input_code.encode('utf-8')).readline)
            output_tokens = []
            for token in tokens:
                if token.type != tokenize.COMMENT:
                    output_tokens.append(token)
            output_code = tokenize.untokenize(output_tokens).decode('utf-8')
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", output_code)
            self.status_label.configure(text="Comments removed successfully")
        except Exception as e:
            self.status_label.configure(text=f"Error processing code: {str(e)}")
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Cleaned Code",
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.output_text.get("1.0", "end"))
                self.status_label.configure(text=f"Saved to: {file_path}")
            except Exception as e:
                self.status_label.configure(text=f"Error saving file: {str(e)}")
    
    def clear_text(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.status_label.configure(text="Ready to process Python files")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernCommentRemoverApp()
    app.run()
