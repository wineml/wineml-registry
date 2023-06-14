from routers.generic import router as public_generic
from routers.user import router as user_registry

all_routers = [
    # admin routers
    # approvers routers
    # user routers
    user_registry,
    # public routers
    public_generic,
]
