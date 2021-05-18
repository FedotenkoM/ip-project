from ..models import RoleModel, UserModel
from password_strength import PasswordPolicy

async def is_username_unique(username):
    user = await UserModel.query.where(
        UserModel.username == username
    ).gino.first()
    if user:
        return False
    return True


async def validate_role(role_id, *args):
    role = await RoleModel.get(role_id)
    return bool(role)

def validate_password(password, *args):
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=2,  # need min. 2 uppercase letters
        numbers=2,  # need min. 2 digits
        special=2,  # need min. 2 special characters
        nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)
    return not bool(policy.test(password))

#from adsystem.core.users.utils import validate_password
#policy.test('ABcd12!@') or policy.test('ABcd12!') validate_password('password')