# AI Logo Designer Pro 🎨🤖

A sleek, dark-themed desktop application built with Python and Tkinter that leverages Generative AI to design professional company logos in seconds.

By integrating Hugging Face's state-of-the-art **FLUX.1-schnell** image generation model, this app takes a simple company name and style preference, intelligently guesses the industry context, and generates a high-quality, text-free vector-style icon ready for branding.

![ai-logo-designer](https://github.com/raghubeer-singh/ai-logo-designer/blob/main/screenshot.png)

## ✨ Features

- **Generative AI Integration:** Uses the blazing-fast `FLUX.1-schnell` model via the Hugging Face Serverless Inference API.
- **Smart Context Engine:** Automatically guesses the company's industry (Tech, Fitness, Restaurant, Legal, etc.) based on keywords in the name to engineer the perfect hidden AI prompt.
- **Modern Dark UI:** A professional, easy-on-the-eyes graphical interface built with Python's native `tkinter`.
- **One-Click Copy:** Seamlessly copy generated logos directly to your Windows clipboard using background PowerShell execution.
- **Native Saving:** Save your favorite logos directly to your hard drive using native OS dialog boxes.
- **Secure Credential Management:** Uses `python-dotenv` to ensure your private API keys are never hardcoded into the source code.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI Framework:** Tkinter (Standard Library)
- **Image Processing:** Pillow (PIL)
- **AI/API Client:** `huggingface_hub`
- **Environment Management:** `python-dotenv`
- **Clipboard Interaction:** `subprocess` (PowerShell)

## 🚀 Getting Started

### Prerequisites

1. Python installed on your machine.
2. A free [Hugging Face](https://huggingface.co/) account.
3. A Hugging Face Access Token with **Fine-grained Inference permissions** enabled.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/raghubeer-singh/ai-logo-designer.git
   cd ai-logo-designer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   ```

3. **Install the required dependencies:**
   ```bash
   pip install huggingface-hub Pillow python-dotenv
   ```

4. **Set up your environment variables:**
   - Create a file named `.env` in the root directory.
   - Add your Hugging Face token to the file:
     ```
     HF_TOKEN=hf_your_actual_token_here
     ```

### Running the App

Execute the main Python script from your terminal:

```bash
python ai-logo-designer.py
```

## 🧠 How It Works (The Prompt Engineering)

Generative AI models struggle with rendering readable text. To bypass this, AI Logo Designer Pro utilizes a specialized prompt engineering pipeline.

1. The app parses the user's input (e.g., `"QuantumCode"`).
2. The logic engine detects keywords (`"Code"`) and assigns the industry `"Technology Startup"`.
3. It constructs a highly specific prompt asking for a `"vector logo, icon, symbol... no text"`.
4. The user receives a perfect, text-less graphic mark, allowing them to add their own clean typography later in software like Canva or Illustrator.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/raghubeer-singh/ai-logo-designer/issues).

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
