#!/usr/bin/python3

# 常见请求错误码
REQUEST_ERROR = 1000

# 认证错误码
AUTH_ERROR = 1100

# 数据库错误
DB_ERROR = 1200

# 服务器内部错误
SVR_ERROR = 1300

# 业务逻辑错误
BUSINESS_ERROR = 1400


class ErrorCode:
    REQ_ERR_ACTION = REQUEST_ERROR + 1, '无效的请求方法, 405'
    REQ_ERR_Content_Type_Lack = REQUEST_ERROR + 2, 'POST, PUT Action 请正确设置 Content_Type 请求头'

    BUSINESS_ERR_PARAMS_INVALID = BUSINESS_ERROR + 1, '无效的请求参数'
    BUSINESS_ERR_PARAMS_LACK = BUSINESS_ERROR + 2, '请求参数不完整'

    AUTH_ERR_RESOURCE = AUTH_ERROR + 1, '无资源访问权限'
    AUTH_ERR_ACCOUNT = AUTH_ERROR + 2, '账号/密码不匹配'
    AUTH_ERR_TOKEN_INVALID = AUTH_ERROR + 3, 'token 无效'
    AUTH_ERR_TOKEN_EXPIRE = AUTH_ERROR + 4, 'token 过期'
    AUTH_ERR_LOGIN_TYPE = AUTH_ERROR + 5, 'login_type与role匹配错误'

    DB_ERR_UNCONNECTED = DB_ERROR + 1, '数据库连接错误'
    DB_ERR_NO_RECORD = DB_ERROR + 2, '数据库无匹配记录'
    DB_ERR_REDIS_CONN = DB_ERROR + 3, 'REDIS 数据库连接错误'

    SVR_ERR_COMM = SVR_ERROR+0, '服务器发生错误, 请联系管理员处理'     # 1300
    SVR_ERR_REJECT = SVR_ERROR+1, '未授权的访问, 请联系管理员处理'     # 1300

