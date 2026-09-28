from google.adk.cli.fast_api import get_fast_api_app
from .agent import app, memory_bank_service_builder

fast_api_app = get_fast_api_app(
    app,
    memory_bank_service_builder=memory_bank_service_builder,
)
