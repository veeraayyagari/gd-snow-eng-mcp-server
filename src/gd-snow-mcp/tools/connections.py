import requests
import os
import logging

from pydantic import BaseModel, Field

import mcp
from gd_servicenow_api.auth.auth_manager import AuthManager
from gd_servicenow_api.utils.config import ServerConfig
from dotenv import load_dotenv
from gd_servicenow_api import observability_snow
load_dotenv()
class Connections(BaseModel):
 def get_connection():
    servicenow_api_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")
    logger = logging.getLogger(__name__)

    service_now_client = observability_snow.ObservabilityServiceNow(username, password, 'e78a061f7cd346388b10be87a08a5a86', '7nsw$|SMZx', servicenow_api_url)
    return service_now_client