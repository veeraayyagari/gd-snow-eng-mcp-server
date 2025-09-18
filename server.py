#server.py
import sys
import os
from boto3 import client
from jsonrpcserver import serve
from mcp import SamplingMessage
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP()

from gd_servicenow_api.tools.knowledge_tools import KNOWLEDGE_TOOLS
from gd_servicenow_api.tools.get_incidents_tools import GetIncident as getIncident
from gd_servicenow_api.tools.update_incident_tools import UpdateIncident as updateIncident
from gd_servicenow_api.tools.get_table_data_tools import GetTableData as getTableData
from gd_servicenow_api.tools.create_change_request_tools import CreateChangeRequest as createChangeRequest
from gd_servicenow_api.create_inc_with_ci import CreateIncWithCI as createIncWithCI
from gd_servicenow_api.tools.incident_state_change_tools import IncidentStateChange as incidentStateChange

# from gd_servicenow_api.tools.knowledge_base_tools import (
#     create_category as create_kb_category_tool
# )


# @mcp.tool()
# async def list_kb_categories():
#     return    list_kb_categories_tool
@mcp.tool()
def get_kb_article():
    return {"Get Article": KNOWLEDGE_TOOLS.get_article()}


@mcp.tool()
def list_kb_articles():
    return {"list articles": KNOWLEDGE_TOOLS.list_articles()}


@mcp.tool()
def list_kb_bases():
    return {"List Knowledge Bases": KNOWLEDGE_TOOLS.list_knowledge_bases()}


# @mcp.tool()
# async def generate_content(topic: str, ctx: Context):
#     prompt = f" Write something {topic}?"
#
#     result = await ctx.session.create_message([
#         SamplingMessage(role="user", content=TextContent(text=prompt))
#     ])
# #Add a tool
# @mcp.tool()
# async def ask_user_info(ctx: Context)-> str:
#     result = await ctx.elicit(message="Please provide your information")
#     user_data = result.data
#     return f"Hello {user_data.name},{user_data.age}"

# @mcp.tool()
# def create_change_request():
#     return {
#         "change_request created": createChangeRequest.CreateChangeRequest()
#     }
# @mcp.tool()
# def create_inc_with_ci(sys_id:str):
#     """
#
#     :type sys_id: str
#     """
#     return {"incident created": createIncWithCI.CreateIncWithCI}
# @mcp.tool()
# def incident_state_change():
#     return {
#         "incident state changed": incidentStateChange
#     }
# @mcp.tool()
# def update_incident(sys_id:str):
#     return {
#         "incident updated": #updateIncident.update_incident()
#     }
#Add a resource
# @mcp.resource("file://incidents")
# async def get_recent_incidents():
#     return {
#         "Recent incidents": # getIncident.get_incident()
#     }
# @mcp.resource("file://gettableData")
# def get_table_data():
#     return {"Table Data": GetTableData}
#Add a prompt
@mcp.prompt()
async def prompt_incidents():
    """AI assisted search with smart recommendations"""
    return f"""prompt"""


def __init__(self):
    if __name__ == "__main__":
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        serve(port=8080)
        mcp.run(transport="stdio")
