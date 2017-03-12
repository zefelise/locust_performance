
import grpc

from protos import quantumdataservice_pb2, quantumdataservice_pb2_grpc


class QuantuamDataClient(object):
    host = None
    channel = None
    stub = None

    def __init__(self, host):
        # super(QuantuamDataClient,self).__init__()
        self.host = host
        self.channel = grpc.insecure_channel(self.host)
        self.stub = quantumdataservice_pb2_grpc.QuantumDataServiceStub(
            self.channel)

    def add(self, x, y):
        return self.stub.add(quantumdataservice_pb2.TestRequest(input1=x, input2=y))

    def create(self):
        return self.stub.create(quantumdataservice_pb2.Empty())

    def read(self, data_id):
        return self.stub.read(quantumdataservice_pb2.ReadRequest(data_id=data_id))


def run():
    a = QuantuamDataClient("172.16.0.8:50001")
    add=a.add(1, 2)
    print(add.output)
    print(a.create().data_id)
    print(add.ByteSize())


if __name__ == '__main__':
    run()
