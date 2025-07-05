# 🚀 AI Code Generator

This project is an AI-powered code generator that leverages the Google Gemini API to generate code snippets, full files, and associated metadata based on natural language prompts. It features a Flask backend for API interactions and a user-friendly HTML/JavaScript frontend.

## ✨ Features

* **Natural Language to Code:** Generate code from plain English descriptions.
* **Multi-file Generation:** Supports generating multiple distinct code files for complex requests (e.g., frontend and backend components).
* **Detailed Code Metadata:** For each generated solution, get insights into:
    * Primary language(s)
    * Approximate lines of code
    * Time and Space complexity
    * Purpose and Goal
    * Required dependencies
    * File extensions
    * Input/Output examples
    * Usage instructions
    * Number of functions/classes
    * Error handling details
    * Assumptions
    * Adherence to best practices
    * Target environment
* **Intuitive Web Interface:** A clean and responsive chat-like interface built with HTML and Tailwind CSS.
* **Code Download:** Easily save generated code files directly from the browser.

## 🛠️ Technologies Used

**Backend:**
* **Python:** The core language for the backend logic.
* **Flask:** A lightweight web framework for building the API.
* **Flask-CORS:** Enables Cross-Origin Resource Sharing for seamless frontend-backend communication.
* **Google Generative AI SDK:** Interfaces with the Gemini API for code generation.

**Frontend:**
* **HTML5:** Structure of the web application.
* **CSS3 (Tailwind CSS):** For modern and responsive styling.
* **JavaScript (ES6+):** Handles dynamic content, user interactions, and API calls.

## 🚦 Getting Started

Follow these steps to set up and run the AI Code Generator on your local machine.

### Prerequisites

* Python 3.8+
* Node.js (optional, for frontend development tools like Tailwind CLI, but not strictly required for running the provided `index.html` as Tailwind is linked via CDN)
* A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/godzaryan/ai-code-generator.git
    cd ai-code-generator
    ```

2.  **Set up the Backend:**
    * Create a virtual environment (recommended):
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```
    * Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```
    * **Configure your Gemini API Key:**
        Open `main.py` and replace `"YOUR_GEMINI_API_KEY"` with your actual API key:
        ```python
        API_KEY = "YOUR_GEMINI_API_KEY" # Replace this with your actual key
        ```
        **Security Note:** For production deployments, it's highly recommended to load the API key from environment variables (e.g., using a `.env` file and `python-dotenv`) rather than hardcoding it directly in the script.

### Running the Application

1.  **Start the Backend Server:**
    From the root directory of the project, run the Flask application:
    ```bash
    python main.py
    ```
    The backend will start on `http://127.0.0.1:8080`. You should see a message like `Backend is running. Open index.html in your browser.` in your console.

2.  **Open the Frontend:**
    Navigate to the `index.html` file in your web browser. You can usually do this by right-clicking `index.html` and selecting "Open with" -> your preferred browser, or by dragging the file into your browser.

    The application will now be running, and you can start generating code!

## 💡 Usage

1.  Type your code request in the input box at the bottom of the page (e.g., "Generate a simple Python function to reverse a string" or "Create an HTML page with a button and a JavaScript function that shows an alert when clicked").
2.  Click the "Generate Code" button or press Enter.
3.  The generated code will appear in the chat area. If multiple files are generated, they will appear as separate blocks.
4.  Click on any generated code block to view its detailed metadata (purpose, complexity, dependencies, etc.) in the "Code Details" section on the right.
5.  Use the "Save Code" button below each code block to download the file to your local machine.

## 📁 Project Structure

```

.
├── main.py             \# Flask backend application
├── index.html          \# Frontend HTML and JavaScript
├── requirements.txt    \# Python dependencies
└── README.md           \# Project README file

```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## 📄 License

This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file (if you plan to add one) for more details.

## 📞 Support / Contact

If you have any questions or need further assistance, please open an issue on this repository.

---

**Happy Coding!** 🚀
