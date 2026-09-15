class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class UserNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            code="USER_NOT_FOUND",
            message="User not found",
            status_code=404,
        )


class UserAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            code="USER_ALREADY_EXISTS",
            message="User already exists",
            status_code=409,
        )


class WorkspaceNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            code="WORKSPACE_NOT_FOUND",
            message="Workspace not found",
            status_code=404,
        )


class WorkspaceAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            code="WORKSPACE_ALREADY_EXISTS",
            message="Workspace already exists",
            status_code=409,
        )


class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__("INVALID_CREDENTIALS", "Invalid email or password", 401)


class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__("INVALID_TOKEN", "Invalid or expired token", 401)


class InactiveUserError(AppException):
    def __init__(self):
        super().__init__("INACTIVE_USER", "User account is inactive", 403)


class WorkspaceForbiddenError(AppException):
    def __init__(self):
        super().__init__("WORKSPACE_FORBIDDEN", "Insufficient workspace role", 403)
