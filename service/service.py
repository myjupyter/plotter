import io
import json

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
                x=string_convert(request.x),
                y=string_convert(request.y),
                hue=string_convert(request.hue),
                order=list_convert(request.order),
                orient=orient_convert(request.orient),
                color=string_convert(request.color),
                palette=string_convert(request.palette),
                saturation=request.saturation,
        )
        b = io.BytesIO()
        plt.savefig(b, format=define_format(request.image_format))
        b.seek(0)
        return pb.plotter_pb2.BarPlotResponse(image=b.read()) 

    def CircleDiagram(self, request, context):
        data = pd.read_json(MessageToJson(request.dataframe))
        ax = plt.pie(
                data.iloc[0], 
                labels=data.columns,
                explode=list_convert(request.explode),
                radius=request.radius,  
                colors=list_convert(request.colors),
                shadow=request.shadow,
                wedgeprops=list_convert(json.loads(MessageToJson(
                    request.wedgeprops)))
        )
        b = io.BytesIO()
        plt.savefig(b, format=define_format(request.image_format))
        b.seek(0)
        return pb.plotter_pb2.BarPlotResponse(image=b.read())

def orient_convert(o):
    if int(o) == 0:
        return 'v'
    return 'h'

def define_format(f):
    if len(f) != 0:
        return f
    return 'png'

def dict_convert(d):
    if len(d) == 0:
        return None
    return d

def string_convert(s):
    if len(s) != 0:
        return s
    return None

def list_convert(l):
    if len(l) == 0:
        return None
    return list(l)
