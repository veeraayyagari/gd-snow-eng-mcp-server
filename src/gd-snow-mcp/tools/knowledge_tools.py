
from symtable import Class

from gd_servicenow_api.tools.connections import Connections
from pydantic import BaseModel, Field
from typing import Optional

service_now_client= Connections.get_connection()

class ListArticlesParams(BaseModel):
        """Parameters for listing knowledge articles."""
        limit: int = Field(10, description="Maximum number of articles to return")
        offset: int = Field(0, description="Offset for pagination")
        knowledge_base: Optional[str] = Field(None, description="Filter by knowledge base")
        category: Optional[str] = Field('None', description="Filter by category")
        query: Optional[str] = Field(None, description="Search query for articles")
        workflow_state: Optional[str] = Field(None, description="Filter by workflow state")

class ListKnowledgeBasesParams(BaseModel):
        """Parameters for listing knowledge bases."""
        limit: int = Field(10, description="Maximum number of knowledge bases to return")
        offset: int = Field(0, description="Offset for pagination")
        active: Optional[bool] = Field(None, description="Filter by active status")
        query: Optional[str] = Field(None, description="Search query for knowledge bases")

class ArticleResponse(BaseModel):
        """Response from article operations."""
        success: bool = Field(..., description="Whether the operation was successful")
        message: str = Field(..., description="Message describing the result")
        article_id: Optional[str] = Field(None, description="ID of the affected article")
        article_title: Optional[str] = Field(None, description="Title of the affected article")
        workflow_state: Optional[str] = Field(None, description="Current workflow state of the article")

class GetArticleParams(BaseModel):
        """Parameters for getting a knowledge article."""
        article_id: str = Field(default='f59cc01b93bbe250c8b9fc83a803d645', description="ID of the article to get")

class KNOWLEDGE_TOOLS:
        def get_article():
            params: dict = GetArticleParams()
            result = service_now_client.get_article(params.article_id);
            print(result)

        def list_articles():
            params: dict[str,any] = ListArticlesParams(limit=5, offset=0, knowledge_base='e15c06f09f30020034c6b6a0942e7076', category='8127e6349f30020034c6b6a0942e70cb', query='CWE-1434', workflow_state='published')
            result = service_now_client.list_articles(params);
            print(result)

        def list_knowledge_bases():
            params: dict[str,any] = ListKnowledgeBasesParams(limit=5,offset=0,active='True',query='Vulnerabilities')
            result = service_now_client.list_knowledge_bases(params)
            print(result)

KNOWLEDGE_TOOLS.list_articles()
KNOWLEDGE_TOOLS.list_knowledge_bases()
#
# class ListKnowledgeBasesParams(BaseModel):
#     """Parameters for listing knowledge bases."""
#
#     limit: int = Field(10, description="Maximum number of knowledge bases to return")
#     offset: int = Field(0, description="Offset for pagination")
#     active: Optional[bool] = Field(None, description="Filter by active status")
#     query: Optional[str] = Field(None, description="Search query for knowledge bases")
#

#
# class ListArticlesParams(BaseModel):
#     """Parameters for listing knowledge articles."""
#
#     limit: int = Field(10, description="Maximum number of articles to return")
#     offset: int = Field(0, description="Offset for pagination")
#     knowledge_base: Optional[str] = Field(None, description="Filter by knowledge base")
#     category: Optional[str] = Field(None, description="Filter by category")
#     query: Optional[str] = Field(None, description="Search query for articles")
#     workflow_state: Optional[str] = Field(None, description="Filter by workflow state")
#



# async def list_categories(
#         config: ServerConfig,
#         auth_manager: AuthManager,
#         params: ListCategoriesParams,
# ) -> Dict[str, Any]:
#     """
#     List categories in a knowledge base.
#
#     Args:
#         config: Server configuration.
#         auth_manager: Authentication manager.
#         params: Parameters for listing categories.
#
#     Returns:
#         Dictionary with list of categories and metadata.
#     """
#     api_url = f"{config.api_url}/table/kb_category"
#
#     # Build query parameters
#     query_params = {
#         "sysparm_limit": params.limit,
#         "sysparm_offset": params.offset,
#         "sysparm_display_value": "all",
#     }
#
#     # Build query string
#     query_parts = []
#     if params.knowledge_base:
#         # Try different query format to ensure we match by sys_id value
#         query_parts.append(f"kb_knowledge_base.sys_id={params.knowledge_base}")
#     if params.parent_category:
#         query_parts.append(f"parent.sys_id={params.parent_category}")
#     if params.active is not None:
#         query_parts.append(f"active={str(params.active).lower()}")
#     if params.query:
#         query_parts.append(f"labelLIKE{params.query}^ORdescriptionLIKE{params.query}")
#
#     if query_parts:
#         query_string = "^".join(query_parts)
#         logger.debug(f"Constructed query string: {query_string}")
#         query_params["sysparm_query"] = query_string
#
#     # Log the query parameters for debugging
#     logger.debug(f"Listing categories with query params: {query_params}")
#
#     # Make request
#     try:
#         response = requests.get(
#             api_url,
#             params=query_params,
#             headers=auth_manager.get_headers(),
#             timeout=config.timeout,
#         )
#         response.raise_for_status()
#
#         # Get the JSON response
#         json_response = response.json()
#
#         # Safely extract the result
#         if isinstance(json_response, dict) and "result" in json_response:
#             result = json_response.get("result", [])
#         else:
#             logger.error("Unexpected response format: %s", json_response)
#             return {
#                 "success": False,
#                 "message": "Unexpected response format",
#                 "categories": [],
#                 "count": 0,
#                 "limit": params.limit,
#                 "offset": params.offset,
#             }
#
#         # Transform the results
#         categories = []
#
#         # Handle either string or list
#         if isinstance(result, list):
#             for category_item in result:
#                 if not isinstance(category_item, dict):
#                     logger.warning("Skipping non-dictionary category item: %s", category_item)
#                     continue
#
#                 # Safely extract values
#                 category_id = category_item.get("sys_id", "")
#                 title = category_item.get("label", "")
#                 description = category_item.get("description", "")
#
#                 # Extract knowledge base - handle both dictionary and string cases
#                 knowledge_base = ""
#                 kb_field = category_item.get("kb_knowledge_base")
#                 if isinstance(kb_field, dict):
#                     knowledge_base = kb_field.get("display_value", "")
#                 elif isinstance(kb_field, str):
#                     knowledge_base = kb_field
#                 # Also check if kb_knowledge_base is missing but there's a separate value field
#                 elif "kb_knowledge_base_value" in category_item:
#                     knowledge_base = category_item.get("kb_knowledge_base_value", "")
#                 elif "kb_knowledge_base.display_value" in category_item:
#                     knowledge_base = category_item.get("kb_knowledge_base.display_value", "")
#
#                 # Extract parent category - handle both dictionary and string cases
#                 parent = ""
#                 parent_field = category_item.get("parent")
#                 if isinstance(parent_field, dict):
#                     parent = parent_field.get("display_value", "")
#                 elif isinstance(parent_field, str):
#                     parent = parent_field
#                 # Also check alternative field names
#                 elif "parent_value" in category_item:
#                     parent = category_item.get("parent_value", "")
#                 elif "parent.display_value" in category_item:
#                     parent = category_item.get("parent.display_value", "")
#
#                 # Convert active to boolean - handle string or boolean types
#                 active_field = category_item.get("active")
#                 if isinstance(active_field, str):
#                     active = active_field.lower() == "true"
#                 elif isinstance(active_field, bool):
#                     active = active_field
#                 else:
#                     active = False
#
#                 created = category_item.get("sys_created_on", "")
#                 updated = category_item.get("sys_updated_on", "")
#
#                 categories.append({
#                     "id": category_id,
#                     "title": title,
#                     "description": description,
#                     "knowledge_base": knowledge_base,
#                     "parent_category": parent,
#                     "active": active,
#                     "created": created,
#                     "updated": updated,
#                 })
#
#                 # Log for debugging purposes
#                 logger.debug(f"Processed category: {title}, KB: {knowledge_base}, Parent: {parent}")
#         else:
#             logger.warning("Result is not a list: %s", result)
#         print(f"categories: {categories}")
#         return {
#             "success": True,
#             "message": f"Found {len(categories)} categories",
#             "categories": categories,
#             "count": len(categories),
#             "limit": params.limit,
#             "offset": params.offset,
#         }
#
#     except requests.RequestException as e:
#         logger.error(f"Failed to list categories: {e}")
#         return {
#             "success": False,
#             "message": f"Failed to list categories: {str(e)}",
#             "categories": [],
#             "count": 0,
#             "limit": params.limit,
#             "offset": params.offset,
#         }
