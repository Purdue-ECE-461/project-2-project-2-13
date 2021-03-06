# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class PackageMetadata(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, version=None, id=None):  # noqa: E501
        """PackageMetadata - a model defined in OpenAPI

        :param name: The name of this PackageMetadata.  # noqa: E501
        :type name: str
        :param version: The version of this PackageMetadata.  # noqa: E501
        :type version: str
        :param id: The id of this PackageMetadata.  # noqa: E501
        :type id: str
        """
        self.openapi_types = {
            'name': str,
            'version': str,
            'id': str
        }

        self.attribute_map = {
            'name': 'Name',
            'version': 'Version',
            'id': 'ID'
        }

        self._name = name
        self._version = version
        self._id = id

    @classmethod
    def from_dict(cls, dikt) -> 'PackageMetadata':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PackageMetadata of this PackageMetadata.  # noqa: E501
        :rtype: PackageMetadata
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this PackageMetadata.

        Name of a package.  - Names should only use typical \"keyboard\" characters. - The name \"*\" is reserved. See the `/packages` API for its meaning.  # noqa: E501

        :return: The name of this PackageMetadata.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PackageMetadata.

        Name of a package.  - Names should only use typical \"keyboard\" characters. - The name \"*\" is reserved. See the `/packages` API for its meaning.  # noqa: E501

        :param name: The name of this PackageMetadata.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def version(self):
        """Gets the version of this PackageMetadata.

        Package version  # noqa: E501

        :return: The version of this PackageMetadata.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PackageMetadata.

        Package version  # noqa: E501

        :param version: The version of this PackageMetadata.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def id(self):
        """Gets the id of this PackageMetadata.


        :return: The id of this PackageMetadata.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PackageMetadata.


        :param id: The id of this PackageMetadata.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id
