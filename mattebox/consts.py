API = "http://app01.luz01.feromedia.tv"

# MatteBOX ID for NanguTV authentication.
PLATFORM_ID = "8a5eaad0e39a83621c25f20b0a10d721"

# NanguTV Client ID and Client Secret.
# Probably your ISP but tested only with this single client.
CLIENT_ID = "feromedia-mobile"
CLIENT_SECRET = "4SbnLL2BdBmbQ94qdPa2N0kF7Xv4fJzo"


class security_values:
    """Values to send in HTTP headers to avoid consequences of usings this kind
    unofficial library.
    """

    user_agent = "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
    app_version = "Android#3.5.32.9-release"
    device_density = "568"
    device_name = "SAMSUNG SM-G960U"
