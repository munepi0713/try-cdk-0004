from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    Duration,
)
from constructs import Construct

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function_asset = lambda_.Code.from_asset(path="../api/src")

        get_data_function = lambda_.Function(
            self,
            "GetDataFunction",
            function_name="GetDataFunction",
            code=function_asset,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.get_data",
            timeout=Duration.seconds(5),
        )

        create_data_function = lambda_.Function(
            self,
            "CreateDataFunction",
            function_name="CreateDataFunction",
            code=function_asset,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.create_data",
            timeout=Duration.seconds(5),
        )

        api = apigateway.RestApi(self, "Api")
        data_api = api.root.add_resource("data")
        data_api.add_method("GET", apigateway.LambdaIntegration(get_data_function))
        data_api.add_method("POST", apigateway.LambdaIntegration(create_data_function))
