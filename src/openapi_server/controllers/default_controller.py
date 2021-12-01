import connexion
import six
from openapi_server import util
from openapi_server.models.error import Error
from openapi_server.models.package import Package
from openapi_server.models.package_history_entry import PackageHistoryEntry
from openapi_server.models.package_metadata import PackageMetadata
from openapi_server.models.package_query import PackageQuery
from openapi_server.models.package_rating import PackageRating
from query_handler.operations.create_operation import CreateOperation
from query_handler.operations.delete_operation import DeleteOperation
from query_handler.operations.read_operation import ReadOperation
from query_handler.operations.update_operation import UpdateOperation
from query_handler.queries.package_query import PackageQuery as PackageQueryDb


def package_by_name_delete(name):
    """Delete all versions of this package.

   

    :param name: 
    :type name: str

    :rtype: None
    """
    return 'do some magic!'


def package_by_name_get(name):
    """package_by_name_get

    Return the history of this package (all versions).

    :param name: 
    :type name: str

    :rtype: List[PackageHistoryEntry]
    """
    return 'do some magic!'


def package_create():
    """package_create

    :rtype: PackageMetadata
    """
    if connexion.request.is_json:
        package = Package.from_dict(connexion.request.get_json())
        query = PackageQueryDb(CreateOperation(), package)
        response: Package = query.execute()
        return response.metadata
    else:
        return None


def package_delete(id_):
    """Delete this version of the package.

    :param id: Package ID
    :type id: str

    :rtype: None
    """
    package = Package(PackageMetadata(id=id_))
    query = PackageQueryDb(DeleteOperation(), package)
    query.execute()
    return 'Package is deleted.'


def package_rate(id_):
    """package_rate

   

    :param id: 
    :type id: str

    :rtype: PackageRating
    """
    return 'do some magic!'


def package_retrieve(id_):
    """package_retrieve

    Return this package.

    :param id: ID of package to fetch
    :type id: str

    :rtype: Package
    """
    package = Package(PackageMetadata(id=id_))
    query = PackageQueryDb(ReadOperation(), package)
    response: Package = query.execute()
    return response


def package_update(id_):
    """Update this version of the package.

    The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents.

    :param id: 
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        package = Package.from_dict(connexion.request.get_json())
        query = PackageQueryDb(UpdateOperation(), package)
        response: Package = query.execute()
        return None, 200


def packages_list(offset=0):
    """Get packages

    Get any packages fitting the query.

    :param offset: Provide this for pagination. If not provided, returns the first page of results.
    :type offset: str

    :rtype: List[PackageMetadata]
    """
    if connexion.request.is_json:
        package_query = [PackageQuery.from_dict(d) for d in connexion.request.get_json()]
    return []


def registry_reset():
    """registry_reset
    :rtype: None
    """
    # Reset the DB
    PackageQueryDb(DeleteOperation()).execute()
    return None, 200
