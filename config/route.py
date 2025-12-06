# config/route.py

from fastapi import APIRouter, Depends
from app.Controllers.Home.HomeController import HomeController
from app.Controllers.Main.MainController import MainController
from app.Controllers.Auth.LoginController import LoginController
from app.Controllers.Auth.RegisterController import RegisterController
from app.Controllers.Auth.ResetPasswordController import ResetPasswordController
from app.Controllers.Auth.ForgotPasswordController import ForgotPasswordController
from app.Middleware.auth import auth_redirect
from app.Middleware.not_auth import not_auth_redirect
from app.Controllers.Test.TestController import TestController

router = APIRouter()


# Маршруты (перенаправляем авторизованных на /main)
auth_router = APIRouter(dependencies=[Depends(auth_redirect)])

auth_router.get("/test", tags=["view"])(TestController.index) 
auth_router.get("/", tags=["view"])(HomeController.index)
auth_router.get("/register", tags=["view"])(RegisterController.register)
auth_router.get("/login", tags=["view"])(LoginController.login)
auth_router.get("/forgot/password", tags=["view"])(ForgotPasswordController.forgotPassword)
auth_router.get("/password/reset/{token}", tags=["view"])(ResetPasswordController.resetPassword)

auth_router.post("/site/register",)(RegisterController.siteRegister)
auth_router.post("/auth/login")(LoginController.authLogin)
auth_router.post("/password/email")(ForgotPasswordController.passwordEmail)
auth_router.post("/password/change")(ResetPasswordController.passwordСhange)

# Маршруты (перенаправляем не авторизованных на /)
not_auth_router = APIRouter(dependencies=[Depends(not_auth_redirect)])

not_auth_router.get("/main", tags=["view"])(MainController.main)
not_auth_router.get("/logout")(LoginController.logout)

# Регистрируем обе группы
router.include_router(auth_router)
router.include_router(not_auth_router)