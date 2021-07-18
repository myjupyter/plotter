'''
An implementation of Plotter service
See proto dir
'''
import io
import json

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from google.protobuf.json_format import MessageToJson

import pb

sns.set_style('whitegrid')

class Plotter(pb.plotter_pb2_grpc.PlotterServicer):
    '''
    Plotter service
    '''
    def BarPlot(self, request, context):
        sns.barplot(data=pd.read_json(
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
        byte_repr = io.BytesIO()
        plt.savefig(byte_repr, format=define_format(request.image_format))
        byte_repr.seek(0)
        return pb.plotter_pb2.BarPlotResponse(image=byte_repr.read())

    def CircleDiagram(self, request, context):
        data = pd.read_json(MessageToJson(request.dataframe))
        plt.pie(
                data.iloc[0],
                labels=data.columns,
                explode=list_convert(request.explode),
                radius=request.radius,
                colors=list_convert(request.colors),
                shadow=request.shadow,
                wedgeprops=list_convert(json.loads(MessageToJson(
                    request.wedgeprops)))
        )
        byte_repr = io.BytesIO()
        plt.savefig(byte_repr, format=define_format(request.image_format))
        byte_repr.seek(0)
        return pb.plotter_pb2.BarPlotResponse(image=byte_repr.read())

def orient_convert(orient):
    '''
    orient converts orient enum to string
    '''
    if int(orient) == 0:
        return 'v'
    return 'h'

def define_format(form):
    '''
    define_format
    '''
    if len(form) != 0:
        return form
    return 'png'

def dict_convert(dictionary):
    '''
    dict_convert
    '''
    if len(dictionary) == 0:
        return None
    return dictionary

def string_convert(string):
    '''
    string_convert
    '''
    if len(string) != 0:
        return string
    return None

def list_convert(elements):
    '''
    list_convert
    '''
    if len(elements) == 0:
        return None
    return list(elements)
