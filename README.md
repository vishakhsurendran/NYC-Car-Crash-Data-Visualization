# NYC Crash Analytics
A program which intakes current official car crash reports from New York City and generates visualizations with the intent of showcasing where improvements to infrastructure may need to be made. This is an improved version of my Collision-Data-Analysis project. Data provided by the City of New York. 

## Demo Images
![Graph Demo](/assets/graph_demo.png)

![Trend Demo](/assets/trend_demo.png)

![Map Demo](/assets/map_demo.png)

## How to run this program
```
git clone https://github.com/vishakhsurendran/NYC-Car-Crash-Data-Visualization.git
cd NYC-Car-Crash-Data-Visualization

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```
