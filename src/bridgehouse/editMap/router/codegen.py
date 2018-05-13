import os
import sys
import grpc_tools.protoc as proto

protoFiles = [x for x in os.listdir() if x.endswith(".proto")]

for p in protoFiles:
    proto.main("--proto_path=./ --python_out=./ --grpc_python_out=./ {}".format(p).split())

