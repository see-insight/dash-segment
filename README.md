# dash-segment

Repository for building a Image annotation Graphical User Interface using Dash.  This interface is starting from the segmentation example provided by plotly (makers of Dash). 


## Installation Instructions

After cloning this repository, open a terminal in the main folder and create a local conda environment (with pip installed) named 'envs' using the following command:

```conda create --prefix ./envs pip```

Activate this new environment using the following command:

```conda activate ./envs```

Install the required modules in the environment using the ```requirements.txt``` file provided in the repository

```pip install -r requirements.txt```

Run the Dash app:

```python app.py```

Open a web browser on your machine and navigate to the following localhost URL:

	http://127.0.0.1:8050/

