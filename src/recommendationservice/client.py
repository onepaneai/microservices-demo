#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import grpc
import demo_pb2
import demo_pb2_grpc

from opencensus.trace.tracer import Tracer

import os
from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
)
from azure.monitor.opentelemetry.exporter import (AzureMonitorTraceExporter, ApplicationInsightsSampler)


from logger import getJSONLogger
logger = getJSONLogger('recommendationservice-server')

if __name__ == "__main__":
    # get port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "8080"

    try:
  
  
        exporter = AzureMonitorTraceExporter(connection_string=os.environ.get('APPINSIGHT_CONNECTION_STRING', ''))
        resource = Resource(attributes={
            "service.name": "recommendationservice"
        })
        sampler = ApplicationInsightsSampler(0.1)
        trace.set_tracer_provider(TracerProvider(resource=resource, sampler=sampler))
        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(exporter)
        )

        grpc_client_instrumentor = GrpcInstrumentorClient()
        grpc_client_instrumentor.instrument()
    except Exception as e:
        logger.warning(e)
    # set up server stub
    
    channel = grpc.insecure_channel('localhost:'+port)
    # channel = grpc.intercept_channel(channel, tracer_interceptor)
    stub = demo_pb2_grpc.RecommendationServiceStub(channel)
    # form request
    request = demo_pb2.ListRecommendationsRequest(user_id="test", product_ids=["test"])
    # make call to server
    response = stub.ListRecommendations(request)
    logger.info(response)
