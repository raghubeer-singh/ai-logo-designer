import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from huggingface_hub import InferenceClient
import io
import os
import subprocess
import tempfile
from dotenv import load_dotenv
import traceback

# ==========================================
# 1. Setup & Configuration
# ==========================================
# Load the environment variables from the .env file
load_dotenv()

# Fetch the token securely
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "black-forest-labs/FLUX.1-schnell"

# --- Dark Theme Color Palette ---
BG_MAIN = "#2b2b2b"       # Dark gray for main window
BG_ENTRY = "#3c3c3c"      # Slightly lighter gray for input boxes
BG_CANVAS = "#1e1e1e"     # Deepest gray for the image area
TEXT_WHITE = "#ffffff"    # Pure white for text
TEXT_MUTED = "#aaaaaa"    # Muted gray for placeholder text/status
ACCENT_BLUE = "#4da6ff"   # Light blue for status messages
ACCENT_GREEN = "#66cc66"  # Light green for success messages
ACCENT_RED = "#ff6666"    # Light red for error messages

class LogoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Logo Designer Pro")
        self.root.geometry("500x750")
        self.root.configure(bg=BG_MAIN, padx=20, pady=20)

        self.current_image = None

        if not HF_TOKEN:
            messagebox.showerror(
                "Missing Token", 
                "Could not find HF_TOKEN. Make sure you have a .env file in the same folder as this script!"
            )
            self.root.destroy()
            return

        try:
            self.client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to connect to AI: {e}")

        # --- UI Elements (Dark Themed) ---
        tk.Label(root, text="Company Name:", font=("Arial", 12, "bold"), bg=BG_MAIN, fg=TEXT_WHITE).pack(pady=5)
        
        # insertbackground changes the blinking cursor color to white
        self.name_entry = tk.Entry(root, font=("Arial", 12), width=30, bg=BG_ENTRY, fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat")
        self.name_entry.pack(pady=5, ipady=3)

        tk.Label(root, text="Style (e.g. Minimalist, Modern, Retro):", font=("Arial", 10), bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=5)
        
        self.style_entry = tk.Entry(root, font=("Arial", 12), width=30, bg=BG_ENTRY, fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat")
        self.style_entry.pack(pady=5, ipady=3)

        self.generate_btn = tk.Button(root, text="Generate Logo", command=self.start_generation, 
                                     bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white",
                                     font=("Arial", 12, "bold"), height=2, relief="flat")
        self.generate_btn.pack(pady=20, fill="x")

        self.status_label = tk.Label(root, text="Ready", bg=BG_MAIN, fg=TEXT_MUTED)
        self.status_label.pack()

        # Image Display Area
        self.canvas = tk.Label(root, text="Logo will appear here", bg=BG_CANVAS, fg=TEXT_MUTED, width=40, height=15)
        self.canvas.pack(pady=10)

        self.action_frame = tk.Frame(root, bg=BG_MAIN)
        self.action_frame.pack(pady=10, fill="x")

        # disabledforeground="#f0f0f0" ensures the text is bright off-white even when the button can't be clicked
        self.copy_btn = tk.Button(self.action_frame, text="Copy Image", command=self.copy_image, 
                                  bg="#2196F3", fg="white", disabledforeground="#f0f0f0",
                                  activebackground="#1e88e5", activeforeground="white",
                                  font=("Arial", 12, "bold"), height=2, relief="flat", state="disabled")
        self.copy_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.save_btn = tk.Button(self.action_frame, text="Save Image As...", command=self.save_image, 
                                  bg="#FF9800", fg="white", disabledforeground="#f0f0f0",
                                  activebackground="#f57c00", activeforeground="white",
                                  font=("Arial", 12, "bold"), height=2, relief="flat", state="disabled")
        self.save_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

    # ==========================================
    # 2. Logic: Generation
    # ==========================================
    def guess_industry(self, name):
        name = name.lower()
        if any(k in name for k in ['tech', 'code', 'data', 'cyber']): return "Technology Startup"
        if any(k in name for k in ['fit', 'gym', 'health', 'iron']): return "Fitness Brand"
        if any(k in name for k in ['cafe', 'food', 'eat', 'brew']): return "Restaurant"
        if any(k in name for k in ['law', 'legal', 'firm']): return "Law Firm"
        return "Professional Business"

    def start_generation(self):
        name = self.name_entry.get().strip()
        style = self.style_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Please enter a Company Name before generating!")
            return

        self.status_label.config(text="Generating... please wait (this takes a few seconds)...", fg=ACCENT_BLUE)
        self.generate_btn.config(state="disabled")
        self.copy_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.root.update()

        try:
            industry = self.guess_industry(name)
            
            prompt = f"professional vector logo, icon, symbol for a company named '{name}', industry: {industry}, {style}, flat design, high contrast, white background, clean lines, centered, no text"
            
            self.current_image = self.client.text_to_image(
                prompt,
                negative_prompt="text, words, letters, signatures, watermark, blurry, realistic, photo, complex background",
                guidance_scale=8.5
            )

            self.display_image(self.current_image)
            
            self.status_label.config(text="Generation Successful!", fg=ACCENT_GREEN)
            
            self.copy_btn.config(state="normal")
            self.save_btn.config(state="normal")

        except Exception as e:
            self.status_label.config(text="Error occurred", fg=ACCENT_RED)
            crash_report = traceback.format_exc()
            print(f"\n=== FULL CRASH REPORT ===\n{crash_report}\n=========================\n")
            messagebox.showerror("API Error", "Check your VS Code terminal for the full red text!")
        
        finally:
            self.generate_btn.config(state="normal")

    def display_image(self, img):
        display_img = img.copy()
        display_img.thumbnail((300, 300))
        self.photo = ImageTk.PhotoImage(display_img)
        
        self.canvas.config(image=self.photo, text="", width=300, height=300)

    # ==========================================
    # 3. Save & Copy Features
    # ==========================================
    def save_image(self):
        if not self.current_image:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")],
            title="Save Logo As"
        )

        if file_path:
            self.current_image.save(file_path)
            messagebox.showinfo("Saved", f"Logo successfully saved to:\n{file_path}")

    def copy_image(self):
        if not self.current_image:
            return
            
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            self.current_image.save(temp_file.name)
            temp_file.close()

            cmd = f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{temp_file.name}'))\""
            subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            os.remove(temp_file.name)
            
            self.status_label.config(text="Image Copied to Clipboard!", fg=ACCENT_GREEN)
            
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy image to clipboard:\n{e}")

# ==========================================
# 4. Main Loop
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = LogoApp(root)
    root.mainloop()