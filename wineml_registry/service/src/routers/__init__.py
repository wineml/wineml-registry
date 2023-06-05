from .public.generic import router as public_generic
from .user.registry import router as user_registry

all_routers = [
    # admin routers
    # approvers routers
    # user routers
    # public routers
    public_generic,
    user_registry,
]
