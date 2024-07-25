
# Real Estate Chatbot 🏡

## Project Overview 🌟
This Real Estate Chatbot application is built using Streamlit. The chatbot interacts with two datasets containing real estate data, allowing users to inquire about properties in various locations, sectors, and room counts. The chatbot uses the OpenAI GPT-3.5 model to provide intelligent responses based on user queries.

## Features 🚀
- **Load and Display Data:** Load and display land and residential real estate data.
- **Property Filtering:** Filter properties based on location, number of rooms, and sector.
- **Chatbot Interaction:** Interact with a chatbot to ask questions about available properties.

## Installation 🔧
Follow these steps to set up the project:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key:**
   - Create a `.env` file in the root directory of your project.
   - Add your OpenAI API key to the `.env` file:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key_here

     ```

## Usage 📘
Run the Streamlit app:

```bash
streamlit run app.py
```

Open your web browser and go to [http://localhost:8501](http://localhost:8501) to interact with the Real Estate Chatbot.

## File Structure 📁
- `app.py`: Main application script.
- `requirements.txt`: List of Python dependencies.
- `.env`: Environment file containing the OpenAI API key (not included in the repository).

## Example 📝
### Loaded Data
The application loads and displays real estate data for both land and residential sectors.

### Property Filter
Users can filter properties based on location, number of rooms, and sector.

### Chatbot Interaction
Users can interact with a chatbot to ask questions about available properties. The chatbot uses the OpenAI GPT-3.5 model to generate responses.

## Dependencies 📦
- `streamlit==1.15.0`
- `pandas==1.3.3`
- `openai==1.5.0`
- `python-dotenv==0.19.2`
- `streamlit-chat==0.1.1`

---

Happy property hunting! 🏘️
