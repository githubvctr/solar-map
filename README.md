Interactive solar map showing installed PV capacities by Dutch municipality (based on publicly available data) on streamlit with interactive features such as:
- Filter municipalities below a selected installed capacity (MW)
- View total capacity (MW) of selected municipalities


Some more ideas of interactive features are under intense category 5 brain storm. See for yourself: 
1. Displaying 10-min radiation averages from KNMI station data  
2. Spatially averaged radiation heatmaps based on KNMI points  
3. Overlaying real-time production vs. installed capacity using Energiopwek data  
4. Click-based selection of areas to estimate current output from covered capacity


## How to Run the Project Locally

1. Install Poetry (if not already installed):
   ```bash
   pip install poetry
2. Clone the respo and navigate into the project folder:
    ```bash
    git clone https://github.com/githubvctr/solar-map.git
    cd solar-map
3. Install all dependencies (to import all the librairies used to make this project run):
    ```bash
    poetry install --no-root
4. Activate the virtual environment:
    ```bash
    poetry shell
5. Run the project through streamlit:
    ```bash
    streamlit run streamlit_app/app.py
7. To generate a summary of all scripts and functions in the project (helpful for LLMs likeContinue or Copilot):
    ```bash
    make summary
7. Use it!