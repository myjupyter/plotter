import io

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from google.protobuf.json_format import MessageToJson

import pb 

sns.set_style('whitegrid')

class Plotter(pb.plotter_pb2_grpc.PlotterServicer):
    def BarPlot(self, request, context):
        ax = sns.barplot(data=pd.read_json(
            MessageToJson(request.dataframe)),
                x=option_string(request.x),
                y=option_string(request.y),
                hue=option_string(request.hue),
                order=order_convert(request.order),
                orient=orient_convert(request.orient),
                color=option_string(request.color),
                palette=option_string(request.palette),
                saturation=request.saturation,
        )
        b = io.BytesIO()
        plt.savefig(b, format='png')
        b.seek(0)
        return pb.plotter_pb2.BarPlotResponse(
            image=b.read(),
        ) 

    def CircleDiagram(self, request, context):
        pass

def option_string(s):
    if len(s) == 0:
        return None
    return s

def orient_convert(o):
    if int(o) == 0:
        return 'v'
    return 'h'

def order_convert(o):
    if len(o) == 0:
        return None
    return list(o)
