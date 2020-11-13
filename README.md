# dash-segment

Repository for building a Image annotation Graphical User Interface using Dash.  This interface is starting from the segmentation example provided by plotly (makers of Dash). 


## Installation Instructions

After cloning this repository, open a terminal in the main folder and create a local conda environment (with pip installed) named 'envs' using the following command:

```conda create --prefix ./envs python=3.7```

Activate this new environment using the following command:

```conda activate ./envs```

Install the required modules in the environment using the ```requirements.txt``` file provided in the repository

```pip install -r requirements.txt```

Run the Dash app:

```python app.py```

Open a web browser on your machine and navigate to the following localhost URL:

	http://127.0.0.1:8050/

When you are done use "ctrl-c" to cancel the dash server and the following command to deactivate the conda environment:

```conda deactivate```

That should be it!

---

# Steps to get see working for development

1. git clone git@github.com:see-insight/see-segment.git
2. cp -r see-segment/see .
3. rm -rf see-segment





