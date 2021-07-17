

proto-gen:
	python -m grpc_tools.protoc \
		-Iproto/plotter/v1 \
		--proto_path=proto\
		-Iproto/google/protobuf \
	   	--python_out=pb/ \
		--grpc_python_out=pb/ \
		plotter.proto
