from fastapi import FastAPI, Request, Depends, HTTPException, status, Path
from middlewares.custom_middleware import setup_middlewares
from dependencies.common import access_denied,verify_token
from auth import auth_routes
from phone_list.staffs import staffs_routes
from phone_list.customers import customers_routes
from phone_list.assignments import assignments_routes
from phone_list.assignments_type import assignments_type_routes
from phone_list.permissions import permissions_routes
from phone_list.files_upload import files_upload_routes
from phone_list.registers import registers_routes
from phone_list.users_role import users_role_routes
# Init FastAPI
app = FastAPI(
    title="Project Name!",
)

# Configure CORS
setup_middlewares(app)


@app.get("/", dependencies=[Depends(verify_token)])
async def root_get():
    return {"message": "This should not be reachable"}


@app.post("/", dependencies=[Depends(verify_token)])
async def root_post():
    return {"message": "This should not be reachable"}


# Include the authentication routes from the auth module
app.include_router(auth_routes.router, prefix="/auth")

app.include_router(staffs_routes.router, prefix="/phone_list/staffs",dependencies=[Depends(verify_token)])
app.include_router(customers_routes.router, prefix="/phone_list/customers",dependencies=[Depends(verify_token)])
app.include_router(assignments_routes.router, prefix="/phone_list/assignments",dependencies=[Depends(verify_token)])
app.include_router(assignments_type_routes.router, prefix="/phone_list/assignments_type",dependencies=[Depends(verify_token)])
app.include_router(permissions_routes.router, prefix="/phone_list/permissions",dependencies=[Depends(verify_token)])
app.include_router(files_upload_routes.router, prefix="/phone_list/file_upload",dependencies=[Depends(verify_token)])
app.include_router(registers_routes.router, prefix="/phone_list/registers",dependencies=[Depends(verify_token)])
app.include_router(users_role_routes.router, prefix="/phone_list/users_role",dependencies=[Depends(verify_token)])

## Run
# uvicorn main:app --reload
# Note: ใส่ --reload เพิ่มเข้าไปเมื่อ Code ของเรามีการเปลี่ยนแปลงตัว Server ก็จะ Restart ให้เราโดยอัตโนมัติ