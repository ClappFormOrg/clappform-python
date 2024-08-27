from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

import grpc

from .proto.clappform.client.v1 import (
    actionflow_pb2_grpc,
    collection_pb2_grpc,
    query_pb2_grpc,
)
from .proto.clappform.data.v1 import (
    aggregate_pb2_grpc,
    delete_pb2_grpc,
    insert_pb2_grpc,
    update_pb2_grpc,
)
from .utils import default_options

if TYPE_CHECKING:
    from typing import Callable, Iterator, Optional

    from .proto.clappform.client.v1 import (
        actionflow_pb2,
        collection_pb2,
        query_pb2,
    )
    from .proto.clappform.data.v1 import (
        aggregate_pb2,
        delete_pb2,
        insert_pb2,
        update_pb2,
    )
    from .proto.clappform.v1 import commons_pb2
    from .typedefs import GrpcChannelOptions, GrpcMetadata, RpcCallOptions

# Metadata
__version__ = "5.0.0-alpha9"
__author__ = "Clappform B.V."
__email__ = "info@clappform.com"
__license__ = "MIT"
__doc__ = "Clappform Python API wrapper"


class GrpcBase:
    """
    Base class for gRPC connections.

    :param target: The target server address.
    :type target: str
    :param token: The authentication token.
    :type token: str
    :param location: The client location (subdomain).
    :type location: str
    :param credentials_fn: A callable that returns gRPC channel credentials,
                           defaults to :py:obj:`grpc.ssl_channel_credentials`.
    :type credentials_fn: Optional[Callable[[], grpc.ChannelCredentials]],
                          optional
    :param options_fn: A callable that returns gRPC channel options,
                       defaults to :func:`clappform.utils.default_options`.
    :type options_fn: Optional[Callable[
                          [],
                          :py:data:`~clappform.typedefs.GrpcChannelOptions`]
                      ], optional
    :param compression_fn: A callable that returns gRPC compression options,
                           defaults to None.
    :type compression_fn: Optional[Callable[
                              [],
                              grpc.Compression
                          ]], optional

    :ivar channel: The gRPC channel.
    :vartype channel: grpc.Channel
    :ivar metadata: The metadata for gRPC calls.
    :vartype metadata: :py:data:`~clappform.typedefs.GrpcMetadata`
    """

    def __init__(
        self,
        target: str,
        token: str,
        location: str,
        credentials_fn: Optional[
            Callable[[], grpc.ChannelCredentials]
        ] = grpc.ssl_channel_credentials,
        options_fn: Optional[
            Callable[[], GrpcChannelOptions]
        ] = default_options,
        compression_fn: Optional[Callable[[], grpc.Compression]] = None,
    ) -> None:
        """
        Initializes the GrpcBase class.

        :param target: The target server address.
        :type target: str
        :param token: The authentication token.
        :type token: str
        :param location: The client location (subdomain).
        :type location: str
        :param credentials_fn: A callable that returns gRPC channel
                               credentials, defaults to
                               :py:obj:`grpc.ssl_channel_credentials`.
        :type credentials_fn: Optional[Callable[
                                  [],
                                  grpc.ChannelCredentials
                              ]], optional
        :param options_fn: A callable that returns gRPC channel options,
                           defaults to :func:`clappform.utils.default_options`.
        :type options_fn: Optional[Callable[
                              [],
                              :py:data:`~clappform.typedefs.GrpcChannelOptions`
                          ]], optional
        :param compression_fn: A callable that returns gRPC compression
                               options, defaults to None.
        :type compression_fn: Optional[Callable[
                                  [],
                                  grpc.Compression
                              ]], optional
        """
        credentials = credentials_fn and credentials_fn()
        options = options_fn and options_fn()
        compression = compression_fn and compression_fn()

        if credentials is None:  # We assume we want an insecure connection.
            self.channel = grpc.insecure_channel(target, options, compression)
        else:
            self.channel = grpc.secure_channel(
                target, credentials, options, compression
            )
        self.metadata: GrpcMetadata = (
            ("location", location),
            ("x-api-key", token),
            ("deadline", "3600s"),
        )

    def _metadata(self, metadata: GrpcMetadata) -> GrpcMetadata:
        """
        Combines the class metadata with additional metadata.

        :param metadata: Additional metadata to be included.
        :return: Combined metadata.
        :rtype: :py:data:`~clappform.typedefs.GrpcMetadata`
        """
        return tuple(chain(self.metadata, metadata))

    def _default_kwargs(
        self,
        timeout: Optional[float] = None,
        metadata: Optional[GrpcMetadata] = None,
        credentials: Optional[grpc.CallCredentials] = None,
        wait_for_ready: Optional[bool] = None,
        compression: Optional[grpc.Compression] = None,
    ) -> RpcCallOptions:
        """
        Creates the default keyword arguments for gRPC calls.

        :param timeout: Timeout for the gRPC call.
        :param metadata: Additional metadata for the gRPC call.
        :param credentials: Call credentials for the gRPC call.
        :param wait_for_ready: Whether to wait for the channel to be ready.
        :param compression: Compression options for the gRPC call.
        :return: Dictionary of gRPC call options.
        :rtype: :py:data:`~clappform.typedefs.RpcCallOptions`
        """
        return {
            "timeout": timeout,
            "metadata": self._metadata(metadata or ()),
            "credentials": credentials,
            "wait_for_ready": wait_for_ready,
            "compression": compression,
        }


class Data(GrpcBase):
    """
    Data class for interacting with gRPC services.

    Inherits from :class:`~clappform.GrpcBase`.

    :param token: The authentication token.
    :type token: str
    :param location: The client location (subdomain).
    :type location: str
    :param target: The target server address, defaults to
                   "data.clappform.com:50051".
    :type target: str, optional
    :param credentials_fn: A callable that returns gRPC channel credentials,
                           defaults to :py:obj:`grpc.ssl_channel_credentials`.
    :type credentials_fn: Optional[Callable[
                              [],
                              grpc.ChannelCredentials
                          ]], optional
    :param options_fn: A callable that returns gRPC channel options,
                       defaults to :func:`clappform.utils.default_options`.
    :type options_fn: Optional[Callable[
                          [],
                          :py:data:`~clappform.typedefs.GrpcChannelOptions`
                      ]], optional
    :param compression_fn: A callable that returns gRPC compression options,
                           defaults to None.
    :type compression_fn: Optional[Callable[
                              [],
                              grpc.Compression
                          ]], optional

    :ivar aggregate_stub: Stub for aggregate management.
    :vartype aggregate_stub: aggregate_pb2_grpc.AggregateManagementStub
    :ivar insert_stub: Stub for insert management.
    :vartype insert_stub: insert_pb2_grpc.InsertManagementStub
    :ivar delete_stub: Stub for delete management.
    :vartype delete_stub: delete_pb2_grpc.DeleteManagementStub
    :ivar update_stub: Stub for update management.
    :vartype update_stub: update_pb2_grpc.UpdateManagementStub
    """

    def __init__(
        self,
        token: str,
        location: str,
        target: str = "data.clappform.com:50051",
        credentials_fn: Optional[
            Callable[[], grpc.ChannelCredentials]
        ] = grpc.ssl_channel_credentials,
        options_fn: Optional[
            Callable[[], GrpcChannelOptions]
        ] = default_options,
        compression_fn: Optional[Callable[[], grpc.Compression]] = None,
    ) -> None:
        """
        Initializes the Data class.

        :param token: The authentication token.
        :type token: str
        :param location: The client location (subdomain).
        :type location: str
        :param target: The target server address, defaults to
                       "data.clappform.com:50051".
        :type target: str, optional
        :param credentials_fn: A callable that returns gRPC channel
                               credentials, defaults to
                               :py:obj:`grpc.ssl_channel_credentials`.
        :type credentials_fn: Optional[Callable[
                                  [],
                                  grpc.ChannelCredentials
                              ]], optional
        :param options_fn: A callable that returns gRPC channel options,
                           defaults to :func:`clappform.utils.default_options`.
        :type options_fn: Optional[Callable[
                              [],
                              :py:data:`~clappform.typedefs.GrpcChannelOptions`
                          ]], optional
        :param compression_fn: A callable that returns gRPC compression
                               options, defaults to None.
        :type compression_fn: Optional[Callable[
                                  [],
                                  grpc.Compression
                              ]], optional
        """
        super().__init__(
            target,
            token,
            location,
            credentials_fn=credentials_fn,
            options_fn=options_fn,
            compression_fn=compression_fn,
        )
        self.aggregate_stub = aggregate_pb2_grpc.AggregateManagementStub(
            self.channel
        )
        self.insert_stub = insert_pb2_grpc.InsertManagementStub(self.channel)
        self.delete_stub = delete_pb2_grpc.DeleteManagementStub(self.channel)
        self.update_stub = update_pb2_grpc.UpdateManagementStub(self.channel)

    def aggregate(
        self, request: aggregate_pb2.AggregateStreamRequest
    ) -> Iterator[aggregate_pb2.AggregateResponse]:
        """
        Sends an aggregate request to the gRPC service and yields responses.

        :param request: The aggregate request to be sent.
        :type request: :class:`~clappform.proto.clappform.data.v1.\
aggregate_pb2.AggregateStreamRequest`
        :return: An iterator over aggregate responses.
        :rtype: Iterator[:class:`~clappform.proto.clappform.data.v1.\
aggregate_pb2.AggregateResponse`]

        :raises grpc.RpcError: If an RPC error occurs

        This method sends an aggregate request to the gRPC service via the
        `AggregateStream` method of the `AggregateManagementStub`. The
        responses from the service are yielded one by one.

        Example usage:

        .. code-block:: python

            from clappform.proto.clappform.data.v1 import aggregate_pb2

            # Create an instance of the Data class
            data_instance = Data(token="your_token", location="your_location")

            # Create an AggregateStreamRequest
            request = aggregate_pb2.AggregateStreamRequest(
                # Fill in the request details
            )

            # Iterate over the responses
            for response in data_instance.aggregate(request):
                print(response)

        .. note::
            Ensure that the `clappform.proto.clappform.data.v1.aggregate_pb2`
            module is imported and available in your code to use the
            `AggregateStreamRequest` and `AggregateResponse` classes.
        """
        yield from self.aggregate_stub.AggregateStream(
            request, **self._default_kwargs()
        )

    def insert_many(
        self, request_iterator: Iterator[insert_pb2.InsertRequest]
    ) -> Iterator[insert_pb2.InsertResponse]:
        """
        Sends multiple insert requests to the gRPC service and yields
        responses.

        :param request_iterator: An iterator over insert requests.
        :type request_iterator: Iterator[:class:`~clappform.proto.clappform.\
data.v1.insert_pb2.InsertRequest`]
        :return: An iterator over insert responses.
        :rtype: Iterator[:class:`~clappform.proto.clappform.data.v1.\
insert_pb2.InsertResponse`]

        :raises grpc.RpcError: If an RPC error occurs

        This method sends multiple insert requests to the gRPC service via the
        `InsertMany` method of the `InsertManagementStub`. The responses from
        the service are yielded one by one.

        Example usage:

        .. code-block:: python

            import clappform
            from clappform.proto.clappform.data.v1 import insert_pb2

            # Create an instance of the Data class
            d = clappform.Data(token="your_token", location="your_location")

            # Create an iterator of InsertRequest
            request_iterator = iter([
                insert_pb2.InsertRequest(
                    # Fill in the request details
                ),
                # Add more requests as needed
            ])

            # Iterate over the responses
            for response in d.insert_many(request_iterator):
                print(response)

        .. note::
            Ensure that the `clappform.proto.clappform.data.v1.insert_pb2`
            module is imported and available in your code to use the
            `InsertRequest` and `InsertResponse` classes.
        """
        yield from self.insert_stub.InsertMany(
            request_iterator,
            **self._default_kwargs(),
        )

    def delete_many_by_oids(
        self, request: delete_pb2.DeleteRequestOids
    ) -> commons_pb2.Message:
        """
        Sends a delete request to the gRPC service to delete multiple items by
        OIDs.

        :param request: The delete request containing OIDs.
        :type request: :class:`~clappform.proto.clappform.data.v1.delete_pb2.\
DeleteRequestOids`
        :return: A message indicating the result of the delete operation.
        :rtype: :class:`~clappform.proto.clappform.data.v1.commons_pb2.Message`

        :raises grpc.RpcError: If an RPC error occurs

        This method sends a delete request to the gRPC service via the
        `DeleteManyByOids` method of the `DeleteManagementStub`. The response
        from the service indicates the result of the operation.

        Example usage:

        .. code-block:: python

            import clappform
            from clappform.proto.clappform.data.v1 import delete_pb2

            # Create an instance of the Data class
            d = clappform.Data(token="your_token", location="your_location")

            # Create a DeleteRequestOids
            request = delete_pb2.DeleteRequestOids(
                # Fill in the request details
            )

            # Send the delete request and get the response
            response = d.delete_many_by_oids(request)
            print(response)

        .. note::
            Ensure that the `clappform.proto.clappform.data.v1.delete_pb2` and
            `clappform.proto.clappform.data.v1.commons_pb2` modules are
            imported and available in your code to use the `DeleteRequestOids`
            and `Message` classes.
        """
        return self.delete_stub.DeleteManyByOids(
            request, **self._default_kwargs()
        )

    def update_replace_many(
        self, request: update_pb2.UpdateRequestByOid
    ) -> update_pb2.UpdateRequest:
        """
        Sends an update request to the gRPC service to replace multiple items.

        :param request: The update request.
        :type request: :class:`~clappform.proto.clappform.data.v1.update_pb2.\
UpdateRequestByOid`
        :return: The update request response.
        :rtype: :class:`~clappform.proto.clappform.data.v1.update_pb2.\
UpdateRequest`

        :raises grpc.RpcError: If an RPC error occurs

        This method sends an update request to the gRPC service via the
        `ReplaceMany` method of the `UpdateManagementStub`. The response from
        the service contains the updated request.

        Example usage:

        .. code-block:: python

            import clappform
            from clappform.proto.clappform.data.v1 import update_pb2

            # Create an instance of the Data class
            d = clappform.Data(token="your_token", location="your_location")

            # Create an UpdateRequestByOid
            request = update_pb2.UpdateRequestByOid(
                # Fill in the request details
            )

            # Send the update request and get the response
            response = d.update_replace_many(request)
            print(response)

        .. note::
            Ensure that the `clappform.proto.clappform.data.v1.update_pb2`
            module is imported and available in your code to use the
            `UpdateRequestByOid` and `UpdateRequest` classes.
        """
        return self.update_stub.ReplaceMany(request, **self._default_kwargs())


class Client(GrpcBase):
    """
    Client class for interfacing with various gRPC services provided by
    Clappform.

    Inherits from :class:`~clappform.GrpcBase`.

    :param token: The authentication token.
    :type token: str
    :param location: The client location (subdomain).
    :type location: str
    :param target: The target server address, defaults to
                   "data.clappform.com:50051".
    :type target: str, optional
    :param credentials_fn: A callable that returns gRPC channel credentials,
                           defaults to :py:obj:`grpc.ssl_channel_credentials`.
    :type credentials_fn: Optional[Callable[
                              [],
                              grpc.ChannelCredentials
                          ]], optional
    :param options_fn: A callable that returns gRPC channel options,
                       defaults to :func:`clappform.utils.default_options`.
    :type options_fn: Optional[Callable[
                          [],
                          :py:data:`~clappform.typedefs.GrpcChannelOptions`
                      ]], optional
    :param compression_fn: A callable that returns gRPC compression options,
                           defaults to None.
    :type compression_fn: Optional[Callable[
                              [],
                              grpc.Compression
                          ]], optional

    :ivar actionflow_stub: Stub for actionflow management.
    :vartype actionflow_stub: actionflow_pb2_grpc.ActionflowManagementStub
    :ivar collection_stub: Stub for collection management.
    :vartype collection_stub: collection_pb2_grpc.CollectionManagementStub
    :ivar query_stub: Stub for query management.
    :vartype query_stub: query_pb2_grpc.QueryManagementStub
    """

    def __init__(
        self,
        token: str,
        location: str,
        target: str = "data.clappform.com:50051",
        credentials_fn: Optional[
            Callable[[], grpc.ChannelCredentials]
        ] = grpc.ssl_channel_credentials,
        options_fn: Optional[
            Callable[[], GrpcChannelOptions]
        ] = default_options,
        compression_fn: Optional[Callable[[], grpc.Compression]] = None,
    ) -> None:
        """
        Initializes the Client class.

        :param token: The authentication token.
        :type token: str
        :param location: The client location (subdomain).
        :type location: str
        :param target: The target server address, defaults to
                       "data.clappform.com:50051".
        :type target: str, optional
        :param credentials_fn: A callable that returns gRPC channel
                               credentials, defaults to
                               :py:obj:`grpc.ssl_channel_credentials`.
        :type credentials_fn: Optional[Callable[
                                  [],
                                  grpc.ChannelCredentials
                              ]], optional
        :param options_fn: A callable that returns gRPC channel options,
                           defaults to :func:`clappform.utils.default_options`.
        :type options_fn: Optional[Callable[
                              [],
                              :py:data:`~clappform.typedefs.GrpcChannelOptions`
                          ]], optional
        :param compression_fn: A callable that returns gRPC compression
                               options, defaults to None.
        :type compression_fn: Optional[Callable[
                                  [],
                                  grpc.Compression
                              ]], optional
        """
        super().__init__(
            target,
            token,
            location,
            credentials_fn=credentials_fn,
            options_fn=options_fn,
            compression_fn=compression_fn,
        )
        self.actionflow_stub = actionflow_pb2_grpc.ActionflowManagementStub(
            self.channel
        )
        self.collection_stub = collection_pb2_grpc.CollectionManagementStub(
            self.channel
        )
        self.query_stub = query_pb2_grpc.QueryManagementStub(self.channel)

    def actionflow_start(
        self, request: actionflow_pb2.StartActionflow
    ) -> actionflow_pb2.StartActionflowResponse:
        """
        Starts an actionflow using the gRPC service.

        :param request: The start actionflow request.
        :type request: :class:`~clappform.proto.clappform.client.v1.\
actionflow_pb2.StartActionflow`
        :return: The response for starting an actionflow.
        :rtype: :class:`~clappform.proto.clappform.client.v1.actionflow_pb2.\
StartActionflowResponse`

        :raises grpc.RpcError: If an RPC error occurs

        Example:
            .. code-block:: python

                import clappform
                from clappform.proto.clappform.data.v1 import actionflow_pb2

                # Create an instance of the Data class
                c = clappform.Client(token="your-token", location="your-locati\
on")

                # Create an StartActionflow
                request = actionflow_pb2.StartActionflow(...)

                # Send the start request and get the response
                response = c.actionflow_start(request)
                print(response)

        .. note::
            Ensure that the
            `clappform.proto.clappform.client.v1.actionflow_pb2` module is
            imported and available in your code to use the
            `StartActionflow` and `StartActionflowResponse` classes.
        """
        return self.actionflow_stub.Start(request, **self._default_kwargs())

    def collection_get(
        self, request: commons_pb2.Read
    ) -> collection_pb2.Collection:
        """
        Gets a collection using the gRPC service.

        :param request: The read request for the collection.
        :type request: :class:`~clappform.proto.clappform.v1.commons_pb2.Read`
        :return: The collection response.
        :rtype: :class:`~clappform.proto.clappform.client.v1.collection_pb2.\
Collection`

        :raises grpc.RpcError: If an RPC error occurs

        Example:
            .. code-block:: python

                import clappform
                from clappform.proto.clappform.v1 import commons_pb2

                # Create an instance of the Data class
                c = clappform.Client(token="your-token", location="your-locati\
on")

                # Create a Read
                request = commons_pb2.Read(...)

                # Send the read request and get the response
                response = c.collection_get(request)
                print(response)

        .. note::
            Ensure that the
            `clappform.proto.clappform.client.v1.collection_pb2` and
            `clappform.proto.clappform.v1.commons_pb2` module is imported and
            available in your code to use the `Read` and `Collection` classes.
        """
        return self.collection_stub.Get(request, **self._default_kwargs())

    def query_get(
        self,
        request: commons_pb2.Read,
    ) -> query_pb2.Query:
        """
        Gets a query using the gRPC service.

        :param request: The read request for the query.
        :type request: :class:`~clappform.proto.clappform.v1.commons_pb2.Read`
        :return: The query response.
        :rtype: :class:`~clappform.proto.clappform.client.v1.query_pb2.Query`

        :raises grpc.RpcError: If an RPC error occurs

        Example:
            .. code-block:: python

                import clappform
                from clappform.proto.clappform.v1 import commons_pb2

                # Create an instance of the Data class
                c = clappform.Client(token="your-token", location="your-locati\
on")

                # Create a Read
                request = commons_pb2.Read(...)

                # Send the read request and get the response
                response = c.query_get(request)
                print(response)

        :note:
            Ensure that the
            `clappform.proto.clappform.client.v1.query_pb2` and
            `clappform.proto.clappform.v1.commons_pb2` module is imported and
            available in your code to use the `Read` and `Query` classes.
        """
        return self.query_stub.Get(request, **self._default_kwargs())
