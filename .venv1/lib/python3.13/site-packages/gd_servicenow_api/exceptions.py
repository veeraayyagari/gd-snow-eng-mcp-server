#!/usr/bin/python
# coding: utf-8

class AuthError(Exception):
    """
    Authentication error
    """
    pass


class UnauthorizedError(AuthError):
    """
    Unauthorized error
    """
    pass


class MissingParameterError(Exception):
    """
    Missing Parameter error
    """
    pass


class ParameterError(Exception):
    """
    Parameter error
    """
    pass



class DataProcessorEnvironmentAlreadyExists(Exception):
    """Exception raised when a Data Processor Environment already exists."""

    def __init__(self, name, message="Data Processor Environment already exists"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name} -> {self.message}"


class InvalidServiceNowRequest(Exception):
    """Exception raised for invalid ServiceNow Request. Raised when the response is not 200 or 201 depending on the use case"""

    def __init__(
        self,
        request,
        response,
        response_code=None,
        message="Invalid Request/Unexpected Response",
    ):
        self.request = request
        self.response = response
        self.response_code = response_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Request: {self.request}  Response: {self.response}   Response Code {self.response_code}  -> {self.message}"

class TableAlreadyExists(Exception):
    """Exception raised when a table already exists."""

    def __init__(self, name, message="Table already exists"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name} -> {self.message}"

class InvalidTableName(Exception):
    """Exception raised for invalid table names."""

    def __init__(self, name, message="Invalid table name"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name} -> {self.message}"

class InvalidPublicCloudAccount(Exception):
    """Exception raised for invalid Public Cloud Account."""

    def __init__(self, name, message="Invalid Public Cloud Account"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name} -> {self.message}"


class DataProcessorAlreadyExists(Exception):
    """Exception raised when a Data Processor already exists."""

    def __init__(self, name, message="Data Processor already exists"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name} -> {self.message}"