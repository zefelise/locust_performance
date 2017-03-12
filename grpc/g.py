import grpc
import time

from quantuamdataclient import QuantuamDataClient
from locust import Locust, events, task, TaskSet
from locust.exception import CatchResponseError


class GrpcResponse(object):
    grpc_response = None
    total_time = None
    name = None
    exception = None

    def __init__(self, name, total_time, response=None, exception=None):
        self.total_time = total_time
        self.name = name
        self.grpc_response = response
        self.exception = exception

    def fail(self, exception=None):
        if isinstance(exception, str):
            exception = CatchResponseError(exception)
        events.request_failure.fire(
            request_type="grpc", name=self.name, response_time=self.total_time, exception=exception)

    def success(self):
        events.request_success.fire(request_type="grpc", name=self.name,
                                    response_time=self.total_time,
                                    response_length=self.grpc_response.ByteSize())


class GrpcClient(QuantuamDataClient):

    def __init__(self, host):
        super(GrpcClient, self).__init__(host)

    def __getattribute__(self, name):
        func = QuantuamDataClient.__getattribute__(self, name)
        if not callable(func):
            return func

        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(
                    request_type="grpc", name=name, response_time=total_time, exception=e)
            else:
                total_time = int((time.time() - start_time) * 1000)
                return GrpcResponse(name, total_time, result)

        return wrapper


class GrpcLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an XML-RPC client
    that can be used to make XML-RPC requests that will be tracked in Locust's statistics.
    """

    def __init__(self, *args, **kwargs):
        super(GrpcLocust, self).__init__(*args, **kwargs)
        assert self.host is not None
        self.client = GrpcClient(self.host)


class GrpcUserBehaviour(TaskSet):
    @task(1)
    def add(self):

        response = self.client.add(1, 2)
        print(response.grpc_response)
        if response.grpc_response.output == 3:
            response.success()
        else:
            response.fail("add result not correct")


class ApiUser(GrpcLocust):

    min_wait = 100
    max_wait = 1000
    task_set = GrpcUserBehaviour


def main():
    client = GrpcClient("172.16.0.8:50001")
    res = client.add(1, 2)


if __name__ == '__main__':
    main()
