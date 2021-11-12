# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server import util

from openapi_server.models.package_metadata import PackageMetadata  # noqa: E501

class PackageHistoryEntry(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, date=None, package_metadata=None, action=None):  # noqa: E501
        """PackageHistoryEntry - a model defined in OpenAPI

        :param date: The date of this PackageHistoryEntry.  # noqa: E501
        :type date: datetime
        :param package_metadata: The package_metadata of this PackageHistoryEntry.  # noqa: E501
        :type package_metadata: PackageMetadata
        :param action: The action of this PackageHistoryEntry.  # noqa: E501
        :type action: str
        """
        self.openapi_types = {
            'date': datetime,
            'package_metadata': PackageMetadata,
            'action': str
        }

        self.attribute_map = {
            'date': 'Date',
            'package_metadata': 'PackageMetadata',
            'action': 'Action'
        }

        self._date = date
        self._package_metadata = package_metadata
        self._action = action

    @classmethod
    def from_dict(cls, dikt) -> 'PackageHistoryEntry':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PackageHistoryEntry of this PackageHistoryEntry.  # noqa: E501
        :rtype: PackageHistoryEntry
        """
        return util.deserialize_model(dikt, cls)

    @property
    def date(self):
        """Gets the date of this PackageHistoryEntry.

        Date of activity.  # noqa: E501

        :return: The date of this PackageHistoryEntry.
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this PackageHistoryEntry.

        Date of activity.  # noqa: E501

        :param date: The date of this PackageHistoryEntry.
        :type date: datetime
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def package_metadata(self):
        """Gets the package_metadata of this PackageHistoryEntry.


        :return: The package_metadata of this PackageHistoryEntry.
        :rtype: PackageMetadata
        """
        return self._package_metadata

    @package_metadata.setter
    def package_metadata(self, package_metadata):
        """Sets the package_metadata of this PackageHistoryEntry.


        :param package_metadata: The package_metadata of this PackageHistoryEntry.
        :type package_metadata: PackageMetadata
        """
        if package_metadata is None:
            raise ValueError("Invalid value for `package_metadata`, must not be `None`")  # noqa: E501

        self._package_metadata = package_metadata

    @property
    def action(self):
        """Gets the action of this PackageHistoryEntry.


        :return: The action of this PackageHistoryEntry.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this PackageHistoryEntry.


        :param action: The action of this PackageHistoryEntry.
        :type action: str
        """
        allowed_values = ["CREATE", "UPDATE", "DOWNLOAD", "RATE"]  # noqa: E501
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"
                .format(action, allowed_values)
            )

        self._action = action
