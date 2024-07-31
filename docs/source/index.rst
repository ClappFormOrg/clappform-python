Getting Started with clappform
==============================

This guide will help you get started with using the `clappform` package to insert, aggregate, and delete data.

Prerequisites
-------------

Ensure you have `clappform` installed. If not, you can install it using pip:

.. code-block:: bash

    pip install clappform

Basic Usage
-----------

Here is a basic example demonstrating how to use `clappform` for inserting, aggregating, and deleting data.

.. code-block:: python

    import json

    import clappform
    from clappform.proto.clappform.data.v1 import aggregate_pb2
    from clappform.proto.clappform.data.v1 import insert_pb2, delete_pb2

    # Replace these with your actual token and location
    token = "your_token"
    location = "your_location"
    collection = "your_collection"

    # Initialize the Data object
    d = clappform.Data(token, location)

    # Function to generate insert requests
    def insert_request_iterator(iterations: int):
        for i in range(iterations):
            yield insert_pb2.InsertRequest(
                data=json.dumps([{"data": f"iteration:{i}"}]).encode("utf-8"),
                collection=collection,
            )

    # Insert data
    for idx, i in enumerate(d.insert_many(insert_request_iterator(100))):
        print(f"Inserted: {idx}")

    # Aggregate data
    oids: list[str] = []
    for i in d.aggregate(aggregate_pb2.AggregateStreamRequest(pipeline=b"[]", collection=collection)):
        oids = [x["_id"] for x in json.loads(i.data)]
        break

    # Delete data by object IDs
    req = delete_pb2.DeleteRequestOids(oids=oids, collection=collection)
    resp = d.delete_many_by_oids(req)

    print(resp.message)

Explanation
-----------

1. **Initialization**:
   - The `Data` object from `clappform` is initialized with a token and location.

2. **Insert Data**:
   - The `insert_request_iterator` function generates `InsertRequest` objects containing data to be inserted.
   - The `insert_many` method is used to insert multiple records, and the progress is printed.

3. **Aggregate Data**:
   - The `aggregate` method is used to fetch data from the collection using an empty pipeline.
   - Object IDs are extracted from the first result set.

4. **Delete Data**:
   - A `DeleteRequestOids` object is created with the object IDs to be deleted.
   - The `delete_many_by_oids` method is used to delete the records, and the result message is printed.

Next Steps
----------

- Explore the `clappform` documentation for more advanced usage and features.
- Experiment with different pipelines and queries for aggregation.
- Implement error handling and logging for a robust application.

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   clappform
   clappform.utils
   clappform.typedefs
