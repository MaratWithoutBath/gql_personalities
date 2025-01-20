from sqlalchemy.future import select
import strawberry

from gql_personalities.DBDefinitions import (
    BaseModel,
)
from gql_personalities.DBDefinitions import GroupTypeModel, RoleTypeModel


def AsyncSessionFromInfo(info):
    # Získá asynchronní session z info
    return info.context["session"]


def UserFromInfo(info):
    # Získá uživatele z info
    return info.context["user"]


class BasePermission(strawberry.permission.BasePermission):
    # Základní třída pro oprávnění
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        # Kontrola oprávnění
        print("BasePermission", source)
        print("BasePermission", self)
        print("BasePermission", kwargs)
        return True


class GroupEditorPermission(BasePermission):
    # Oprávnění pro editaci skupiny
    message = "User is not authenticated"

    async def canEditGroup(session, group_id, user_id):
        # Kontrola, zda uživatel může editovat skupinu
        stmt = select(RoleModel).filter_by(group_id=group_id, user_id=user_id)
        dbRecords = await session.execute(stmt).scalars()
        dbRecords = [*dbRecords]  # konverze na list
        if len(dbRecords) > 0:
            return True
        else:
            return False

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        # Kontrola oprávnění pro editaci skupiny
        print("GroupEditorPermission", source)
        print("GroupEditorPermission", self)
        print("GroupEditorPermission", kwargs)
        # _ = await self.canEditGroup(session,  source.id, ...)
        print("GroupEditorPermission")
        return True


class UserEditorPermission(BasePermission):
    # Oprávnění pro editaci uživatele
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        # Kontrola oprávnění pro editaci uživatele
        print("UserEditorPermission", source)
        print("UserEditorPermission", self)
        print("UserEditorPermission", kwargs)
        return True


class UserGDPRPermission(BasePermission):
    # Oprávnění pro GDPR uživatele
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        # Kontrola oprávnění pro GDPR uživatele
        print("UserGDPRPermission", source)
        print("UserGDPRPermission", self)
        print("UserGDPRPermission", kwargs)
        return True
