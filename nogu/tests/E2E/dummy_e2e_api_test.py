from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from loguru import logger
from pydantic import BaseModel, Field

from nogu.tests import BaseTestCase

app = FastAPI(
    title="Dummy APP",
    description=(
        "Dummy application to show how to implement the E2E tests using FastAIP"
        " triggers."
    ),
    version="1.0.0",
)


class HelloItem(BaseModel):
    """A dummy input item for the hello world endpoint."""

    name: str
    last_name: str
    is_human: bool = Field(
        default=True,
        optional=True,
    )


@app.post("/hello/", summary="Trigger hellow world function to check if test env works")
async def trigger_hello_world(background_tasks: BackgroundTasks, item: HelloItem):
    """Triggers a 'hello world' response based on the input item.

    If the name is "adam", it simulates an internal server error to demonstrate
    error handling and test failure scenarios. Otherwise, it returns a greeting.

    Args:
        background_tasks: FastAPI's dependency for background tasks (not used in this simple example).
        item: The input data containing name, last_name, and human status.

    Returns:
        A dictionary with a greeting message if successful.

    Raises:
        HTTPException: If the name is "adam", indicating a simulated internal server error.
    """
    if item.name != "adam":
        return {
            "Greetings": (
                f"Hello {item.name}  {item.last_name}, are you human: {item.is_human} "
            )
        }
    else:
        logger.error(f"Are you a human: {item.is_human} ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger full pipeline: {item.name}",
        )


class DummyE2ETestCase(BaseTestCase):
    """A dummy end-to-end (E2E) test case.

    This test case is added to ensure that the E2E pipeline is functioning correctly.
    It tests the `/hello` endpoint of the FastAPI application.
    """

    def setUp(self) -> None:
        """Set up the test environment before each test method runs.

        Initializes a TestClient for the FastAPI application.
        """
        self.test_client = TestClient(app)

    def test_e2e_api_hello_world_return_success(self):
        """Tests the `/hello` API endpoint for a successful response.

        Sends a POST request with valid data and asserts that the status code is 200
        and the response body matches the expected success message.
        """
        request = {"name": "xxx", "last_name": "yyy"}
        response = self.test_client.post(
            "/hello", headers={"X-Token": "coneofsilence"}, json=request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"Greetings": "Hello xxx  yyy, are you human: True "}
        )

    def test_e2e_api_hello_world_return_failure(self):
        """Tests the `/hello` API endpoint for a simulated failure response.

        Sends a POST request with the name "adam" (which triggers an internal server error)
        and asserts that the status code is 500 and the response body matches the
        expected error detail.
        """
        request = {"name": "adam", "last_name": "yyy"}
        response = self.test_client.post(
            "/hello", headers={"X-Token": "coneofsilence"}, json=request
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(), {"detail": "Failed to trigger full pipeline: adam"}
        )
