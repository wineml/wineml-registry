from .public.generic import router as public_generic
from .user.registry import router as user_registry
from .user.db import router as user_db

all_routers = [
    # admin routers
    # approvers routers
    # user routers
    user_registry,
    user_db,
    # public routers
    public_generic,
]
