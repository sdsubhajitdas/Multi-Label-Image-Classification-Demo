from flask import Flask
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = "09167a185e72cd1619eb65beb0b623cb"

DEBUG_MODE = False
MODEL_PATH = os.path.join(app.root_path,'static', 'model', 'demo_model.h5')
CLASSES = "Aeroplane,Bicycle,Bird,Boat,Bottle,Bus,Car,Cat,Chair,Cow,Diningtable,Dog,Horse,Motorbike,Person,Pottedplant,Sheep,Sofa,Train,Tvmonitor".split(",")

from demo import routes