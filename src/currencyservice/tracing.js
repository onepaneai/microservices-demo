const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { Resource } = require('@opentelemetry/resources');

const { GrpcInstrumentation } = require('@opentelemetry/instrumentation-grpc');

const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { AzureMonitorTraceExporter, ApplicationInsightsSampler } = require("@azure/monitor-opentelemetry-exporter");

const exporter = new AzureMonitorTraceExporter({
    connectionString: "InstrumentationKey=b6a44f93-ffc9-442d-abda-0d2967019fb7;IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/"
});

const aiSampler = new ApplicationInsightsSampler(0.10);


const provider = new NodeTracerProvider({
   sampler: aiSampler,
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'currencyservice',
  }),
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

registerInstrumentations({
  instrumentations: [
    new GrpcInstrumentation()
  ],
});