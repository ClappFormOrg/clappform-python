"""
clappform.dataclasses
~~~~~~~~~~~~~~~~~~~~~

This module contains the set of Clappform's return objects.
"""
# Python Standard Library modules
from dataclasses import dataclass, field
import base64
import json
import time
import abc


@dataclass
class ApiResponse:
    """Data class to represent generic API response.

    :param int code: HTTP status code.
    :param str message: Message about the request and response.
    :param str response_id: Response Id can be used to open support ticket.
    """

    #: HTTP status code.
    code: int
    #: Message about the request and response.
    message: str
    #: Response Id can be used to open support ticket.
    response_id: str

    def __init__(self, code: int, message: str, response_id: str, **kwargs):
        self.code = code
        self.message = message
        self.response_id = response_id
        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclass
class Auth:
    """Authentication dataclass.

    :param str access_token: Bearer token to be used in a HTTP authorization header.
    :param int refresh_expiration: Integer representing the when the
        :attr:`refresh_token` is invalid.
    :param str refresh_token: Bearer token to be used get new :attr:`access_token`.
    """

    #: Bearer token to be used in a HTTP authorization header.
    access_token: str
    #: Integer representing the when the :attr:`refresh_token` is invalid.
    refresh_expiration: int
    #: Bearer token to be used get new :attr:`access_token`.
    refresh_token: str

    _expires: int

    def __init__(self, access_token: str, refresh_expiration: int, refresh_token: str):
        self.access_token = access_token
        self.refresh_expiration = refresh_expiration
        self.refresh_token = refresh_token

        token_data = json.loads(
            base64.b64decode(self.access_token.split(".")[1] + "==")
        )
        self._expires = token_data["exp"]

    def is_token_valid(self) -> bool:
        """Returns boolean answer to: is the :attr:`access_token` still valid?

        :returns: Validity of :attr:`access_token`
        :rtype: bool
        """
        if self._expires > int(time.time()) + 60:
            return True
        return False


@dataclass
class Version:
    """Version dataclass.

    :param str api: Version of the API.
    :param str web_application: Version of the Web Application.
    :param str web_server: Version of the Web Server
    """

    #: Version of the API.
    api: str = None
    #: Version of the Web Application.
    web_application: str = None
    #: Version of the Web Server
    web_server: str = None

    def one_or_all_path(self) -> str:
        return "/version"


class ResourceType(metaclass=abc.ABCMeta):
    """ResourceType is used as a base class for dataclasses.
    :class:`ResourceType <ResourceType>` contains only one abstract method. Any class
    that inherits from :class:`ResourceType <ResourceType>` is required to implement
    :meth:`path <path>`.
    """

    @staticmethod
    def bool_to_lower(boolean: bool) -> str:
        """Return a boolean string in lowercase.

        :param boolean: ``True`` or ``False`` value to convert to lowercase string.
        :type boolean: bool

        :returns: Lowercase boolean string
        :rtype: str
        """
        if not isinstance(boolean, bool):
            raise TypeError(f"boolean is not of type {bool}, got {type(boolean)}")
        return str(boolean).lower()


@dataclass
class App(ResourceType):
    """App dataclass.

    :param int collections: Number of collections this app has.
    :param str default_page: Page to view when opening app.
    :param str description: Description below app name.
    :param int groups: Nuber of groups in an app.
    :param str id: Used internally to identify app.
    :param str name: Name of the app.
    :param dict settings: Settings to configure app.
    """

    collections: int = None
    default_page: str = None
    description: str = None
    groups: int = None
    id: str = None
    _id: str = field(init=False, repr=False, default=None)
    name: str = None
    settings: dict = None
    extended: bool = field(init=True, repr=False, default=False)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        assert isinstance(value, (property, str, type(None)))
        if isinstance(value, property):
            value = self._id
        self._id = value

    def one_or_all_path(self) -> str:
        """Return the route used to retreive the App.

        :returns: App's HTTP resource path.
        :rtype: str
        """
        if self.id is not None:
            return self.one_path()
        return self.all_path()

    def one_path(self) -> str:
        extended = self.bool_to_lower(bool(self.extended))
        if self.id is None:
            raise TypeError(f"id attribute can not be {None}")
        return f"/app/{self.id}?extended={extended}"

    def all_path(self) -> str:
        extended = self.bool_to_lower(bool(self.extended))
        return f"/apps?extended={extended}"

    def create_path(self) -> str:
        return "/app"


@dataclass
class Collection(ResourceType):
    """Collection dataclass."""

    app: str = None
    _app: str = field(init=False, repr=False, default=None)
    slug: str = None
    _slug: str = field(init=False, repr=False, default=None)
    database: str = None
    name: str = None
    items: int = None
    description: str = None
    is_encrypted: bool = None
    is_locked: bool = None
    is_logged: bool = None
    queries: list = None
    sources: list = None
    id: int = None
    extended: int = field(init=True, repr=False, default=0)

    @property
    def app(self) -> str:
        return self._app

    @app.setter
    def app(self, value) -> None:
        assert isinstance(value, (property, str, App, type(None)))
        if isinstance(value, property):
            # initial value not specified, use default
            value = self._app
        if isinstance(value, App):
            value = value.id
        self._app = value

    @property
    def slug(self) -> str:
        return self._slug

    @slug.setter
    def slug(self, value: str) -> None:
        assert isinstance(value, (property, str, type(None)))
        if isinstance(value, property):
            # initial value not specified, use default
            value = self._slug
        self._slug = value

    @staticmethod
    def check_extended(extended: int):
        """Check if ``extended`` is of type :class:`int` and `0` to `3`."""
        if not isinstance(extended, int):
            raise TypeError(f"extended is not of type {int}, got {type(extended)}")
        extended_range = range(4)  # API allows for 4 levels of extension.
        if extended not in extended_range:
            raise ValueError(f"extended {extended} not in {extended_range}")

    def one_or_all_path(self):
        if self.app is None and self.slug is None:
            return self.all_path()
        return self.one_path()

    def one_path(self) -> str:
        self.check_extended(self.extended)
        if self.app is None or self.slug is None:
            raise TypeError("both 'app' and 'slug' attributes can not be {None}")
        return f"/collection/{self.app}/{self.slug}?extended={self.extended}"

    def all_path(self) -> str:
        self.check_extended(self.extended)
        return f"/collections?extended={self.extended}"

    def create_path(self) -> str:
        if self.app is None:
            raise TypeError("app attribute can not be None")
        return f"/collection/{self.app}"

    def one_item_path(self, item: str) -> str:
        """Return the route used for creating and deleting items.

        :param str app: App to which collection belongs to.
        :param str collection: Collection to get from app.

        :returns: Item HTTP resource path
        :rtype: str
        """
        if self.app is None or self.slug is None:
            raise TypeError("both 'app' and 'slug' attributes can not be {None}")
        if not isinstance(item, str):
            raise TypeError(f"item arg is not of type {str}, got {type(item)}")
        return f"/item/{self.app}/{self.slug}/{item}"

    def create_item_path(self) -> str:
        if self.app is None or self.slug is None:
            raise TypeError(f"both 'app' and 'slug' attributes can not be {None}")
        return f"/item/{self.app}/{self.slug}"

    def dataframe_path(self) -> str:
        """Return the route used to retreive the Dataframe.

        :returns: Collection's Dataframe HTTP resource path
        :rtype: str
        """
        if self.app is None or self.slug is None:
            raise TypeError(f"'app' and 'slug' attributes can not be {None}")
        return f"/dataframe/{self.app}/{self.slug}"


@dataclass
class Query(ResourceType):
    """Query dataclass."""

    app: str = None
    _app: str = field(init=False, repr=False, default=None)
    collection: str = None
    _collection: str = field(init=False, repr=False, default=None)
    data_source: str = None
    export: bool = None
    id: int = None
    name: str = None
    query: list = None
    slug: str = None
    source_query: str = None
    modules: list = None
    primary: bool = None
    settings: dict = None

    @property
    def app(self) -> str:
        return self._app

    @app.setter
    def app(self, value) -> None:
        assert isinstance(value, (property, str, App, type(None)))
        if isinstance(value, property):
            # initial value not specified, use default
            value = self._app
        if isinstance(value, App):
            value = value.id
        self._app = value

    @property
    def collection(self) -> str:
        return self._collection

    @collection.setter
    def collection(self, value: str) -> None:
        assert isinstance(value, (property, str, Collection, type(None)))
        if isinstance(value, property):
            # initial value not specified, use default
            value = self._collection
        if isinstance(value, Collection):
            self._app = value.app
            value = value.slug
        self._collection = value

    def one_or_all_path(self) -> str:
        if self.slug is None:
            return self.all_path()
        return self.one_path()

    def one_path(self) -> str:
        """Return the route used to retreive the Query.

        :returns: Query HTTP resource path
        :rtype: str
        """
        if not isinstance(self.slug, str):
            raise TypeError(
                f"slug attribute is not of type {str}, got {type(self.slug)}"
            )
        return f"/query/{self.slug}"

    def all_path(self) -> str:
        """Return the route used to retreive the Query.

        :returns: Query HTTP resource path
        :rtype: str
        """
        return "/queries"

    def create_path(self) -> str:
        return "/query"

    def source_path(self) -> str:
        """Return the route used to source the Query.

        :returns: Source Query API route
        :rtype: str
        """
        if not isinstance(self.slug, str):
            raise TypeError(
                f"slug attribute is not of type {str}, got {type(self.slug)}"
            )
        return f"/source_query/{self.slug}"


@dataclass
class Actionflow(ResourceType):
    """Actionflow dataclass."""

    id: int = None
    name: str = None
    settings: dict = None
    cronjobs: list = None
    tasks: list = None

    def one_or_all_path(self) -> str:
        if self.id is None:
            return self.all_path()
        return self.one_path()

    def all_path(self) -> str:
        return "/actionflows"

    def one_path(self) -> str:
        return f"/actionflow/{self.id}"

    def create_path(self) -> str:
        return "/actionflow"


@dataclass
class Questionnaire(ResourceType):
    """Questionnaire dataclass."""

    name: str = None
    id: int = None
    created_at: int = None
    active: bool = None
    created_by: dict = None
    latest_version: dict = None
    versions: list = None
    settings: dict = field(init=True, repr=False, default=None)
    extended: bool = field(init=True, repr=False, default=False)

    def one_or_all_path(self) -> str:
        if self.id is None:
            return self.all_path()
        return self.one_path()

    def all_path(self) -> str:
        extended = self.bool_to_lower(bool(self.extended))
        return f"/questionnaires?extended={extended}"

    def one_path(self) -> str:
        extended = self.bool_to_lower(bool(self.extended))
        if not isinstance(self.id, int):
            raise TypeError(f"id attribute is not of type {int}, got {type(self.id)}")
        return f"/questionnaire/{self.id}?extended={extended}"

    def create_path(self) -> str:
        return "/questionnaire"


@dataclass
class User(ResourceType):
    """User dataclass."""

    email: str = None
    extra_information: dict = None
    first_name: str = None
    last_name: str = None
    is_active: bool = None
    id: int = None
    phone: str = None
    messages: dict = None
    last_online: int = None
    permissions: list[str] = None
    roles: list[dict] = None
    extended: bool = field(init=True, repr=False, default=False)

    def one_or_all_path(self) -> str:
        if self.email is None:
            return self.all_path()
        return self.one_path()

    def all_path(self) -> str:
        extended = self.bool_to_lower(bool(self.extended))
        return f"/users?extended={extended}"

    def one_path(self) -> str:
        extended = self.bool_to_lower(bool(self.extended))
        if not isinstance(self.email, str):
            raise TypeError(
                f"email attribute is not of type {str}, got {type(self.email)}"
            )
        return f"/user/{self.email}?extended={extended}"

    def create_path(self) -> str:
        return "/user"
