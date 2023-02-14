from app.schemas import RoleEnum


class RoleScope:
    role_list = [role for role in RoleEnum]

    @classmethod
    def all(cls) -> list[RoleEnum]:
        return cls.role_list.copy()

    @classmethod
    def exclude(cls, role_excluded: RoleEnum | str) -> list[RoleEnum]:
        if isinstance(role_excluded, str):
            role_excluded = RoleEnum(role_excluded)

        return [role for role in cls.role_list if role != role_excluded]
