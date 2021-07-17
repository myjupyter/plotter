#!/usr/bin/env python3

import grpc
from grpc_reflection.v1alpha import reflection
from concurrent import futures

import matplotlib

import pb
import service

def main():
    # to turn off GUI windows
    matplotlib.use('agg')

    server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10))

    pb.plotter_pb2_grpc.add_PlotterServicer_to_server(
        service.Plotter(), server)

    SERVICE_NAMES = (
        pb.plotter_pb2.DESCRIPTOR.services_by_name['Plotter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    p = service.Plotter()

if __name__ == '__main__':
    main()
