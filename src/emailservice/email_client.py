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

import grpc

import demo_pb2
import demo_pb2_grpc
from azure.monitor.opentelemetry.exporter import (AzureMonitorTraceExporter, ApplicationInsightsSampler)

from logger import getJSONLogger
logger = getJSONLogger('emailservice-client')

from opencensus.trace.tracer import Tracer
from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace.ext.grpc import client_interceptor

from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
)

try:
  
  
    exporter = AzureMonitorTraceExporter(connection_string="InstrumentationKey=b6a44f93-ffc9-442d-abda-0d2967019fb7;IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/")
    resource = Resource(attributes={
      "service.name": "emailservice"
    })
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(exporter)
    )

    grpc_client_instrumentor = GrpcInstrumentorClient()
    grpc_client_instrumentor.instrument()
except Exception as e:
    logger.warning(e)

def send_confirmation_email(email, order):
  channel = grpc.insecure_channel('0.0.0.0:8080')
  channel = grpc.intercept_channel(channel)
  stub = demo_pb2_grpc.EmailServiceStub(channel)
  try:
    response = stub.SendOrderConfirmation(demo_pb2.SendOrderConfirmationRequest(
      email = email,
      order = order
    ))
    logger.info('Request sent.')
  except grpc.RpcError as err:
    logger.error(err.details())
    logger.error('{}, {}'.format(err.code().name, err.code().value))

if __name__ == '__main__':
  logger.info('Client for email service.')
