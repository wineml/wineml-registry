from routers.generic import router as public_generic
from routers.model import router as model_route
from routers.modelversion import router as modelversion_route

all_routers = [
    public_generic,
    model_route,
    modelversion_route,
]
