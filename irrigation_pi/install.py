"""Install commands."""

# ruff: noqa: D205, D301, D400

from pathlib import Path
from shutil import chown

import click
from click import Context

from irrigation_pi.constants import (
    APPLICATION_CONFIGURATION_PATH,
    APPLICATION_USER,
    APPLICATION_USER_GROUP,
    BACKEND_PATH,
    DATABASE_PATH,
    DEBIAN_GPIO_PACKAGES,
    HOST,
    NGINX_CONFIG_ACTIVATION_PATH,
    NGINX_CONFIG_PATH,
    NGINX_DEFAULT_CONFIG_ACTIVATION_PATH,
    PORT,
    SYSTEMD_CONFIG_PATH,
    VIRTUAL_ENVIRONMENT_PATH,
    WIFI_HOTSPOT_CONNECTION_NAME,
)
from irrigation_pi.utils import (
    activate_virtual_environment,
    create_application_configuration,
    create_nginx_config,
    create_systemd_config,
    run_subprocess,
)


@click.command(name="all")
@click.pass_context
def install_all(ctx: Context):
    """Install everything necessary to run the application on Raspberry Pi.
    \f
    :return:
    """
    ctx.forward(install_debian_packages)
    ctx.forward(install_application_configuration)
    ctx.forward(install_database)
    ctx.forward(install_systemd_configuration)
    ctx.forward(install_nginx)


@click.command(name="debian-packages")
def install_debian_packages():
    """Install Debian packages.
    \f
    :return:
    """
    click.echo("Updating Debian package sources...")
    run_subprocess(["sudo", "apt", "update"])

    click.echo("Installing Debian packages...")
    run_subprocess(
        [
            "sudo",
            "apt",
            "install",
            *DEBIAN_GPIO_PACKAGES,
            "--no-install-recommends",
            "-y",
        ]
    )


@click.command(name="config")
def install_application_configuration():
    """Install irrigation-pi application configuration.
    \f
    :return:
    """
    click.echo("Installing irrigation-pi application configuration...")
    config: str = create_application_configuration()

    with open(APPLICATION_CONFIGURATION_PATH, "w") as file:
        file.write(config)


@click.command(name="database")
def install_database():
    """Install backend database.
    \f
    :return:
    """
    click.echo("Installing database...")
    env: dict = activate_virtual_environment(VIRTUAL_ENVIRONMENT_PATH)
    run_subprocess(["alembic", "upgrade", "head"], cwd=BACKEND_PATH, env=env)
    chown(DATABASE_PATH, APPLICATION_USER, APPLICATION_USER_GROUP)


@click.command(name="systemd-config")
def install_systemd_configuration():
    """Install systemd configuration to run backend application with Uvicorn.

    Generate a service definition file for backend application and install it
    in the appropriate place and fire up the service.

    See:
    https://systemd.io/
    https://wiki.debian.org/systemd
    https://wiki.debian.org/systemd/Services
    \f
    :return:
    """
    click.echo("Installing Systemd configuration...")
    systemd_config: str = create_systemd_config(
        APPLICATION_USER, VIRTUAL_ENVIRONMENT_PATH, BACKEND_PATH
    )

    with open(SYSTEMD_CONFIG_PATH, "w") as file:
        file.write(systemd_config)

    # Enable irrigation-pi service, so it boots on startup
    run_subprocess(["sudo", "systemctl", "enable", "irrigation-pi"])

    # And start the service immediately
    run_subprocess(["sudo", "systemctl", "start", "irrigation-pi"])


@click.command(name="nginx")
def install_nginx():
    """Install nginx and it's configuration.

    See: https://nginx.org/en/docs/
    \f
    :return:
    """
    click.echo("Updating Debian package sources...")
    run_subprocess(["sudo", "apt", "update"])

    click.echo("Installing nginx Debian package...")
    run_subprocess(["sudo", "apt", "install", "nginx", "--no-install-recommends", "-y"])

    # Create nginx config
    click.echo("Installing nginx configuration...")
    server_root_path: Path = (
        Path(__file__).parent.parent.resolve() / "frontend" / "www" / "browser"
    )
    nginx_config: str = create_nginx_config(HOST, PORT, server_root_path)

    with open(NGINX_CONFIG_PATH, "w") as file:
        file.write(nginx_config)

    # Activate nginx config
    NGINX_CONFIG_ACTIVATION_PATH.symlink_to(NGINX_CONFIG_PATH)

    # Deactivate nginx default config if it exists
    NGINX_DEFAULT_CONFIG_ACTIVATION_PATH.unlink(missing_ok=True)

    # Reload nginx config
    run_subprocess(["sudo", "systemctl", "reload", "nginx"])


@click.command(name="caddy")
def install_caddy():
    """Install caddy and it's configuration.

    See: https://caddyserver.com/docs/
    \f
    :return:
    """
    click.echo("Updating Debian package sources...")
    run_subprocess(["sudo", "apt", "update"])

    click.echo("Installing caddy Debian package...")
    run_subprocess(["sudo", "apt", "install", "caddy", "--no-install-recommends", "-y"])


@click.command(name="wifi-hotspot")
@click.option(
    "--interface-name",
    default="wlan0",
    help="Name of the 802-11-wireless interface, i.e. wlan0.",
)
@click.option("--ssid", default="Irrigation-Pi", help="SSID of Wi-Fi Hotspot.")
@click.password_option(
    required=True,
    help="Password for Wi-Fi Hotspot, minimum length 8 characters.",
)
@click.option(
    "--autoconnect",
    default="on",
    type=click.Choice(["on", "off"], case_sensitive=False),
    help="Wi-Fi Hotspot autoconnect.",
)
@click.option(
    "--autoconnect-priority", default="100", help="Wi-Fi Hotspot autoconnect-priority."
)
def install_wifi_hotspot(
    interface_name: str,
    ssid: str,
    password: str,
    autoconnect: str,
    autoconnect_priority: str,
):
    """Install Wi-Fi hotspot using NetworkManager.

    For more details see: https://networkmanager.dev/docs/api/latest/
    \f
    :return:
    """
    click.echo("Installing Wi-Fi hotspot...")

    # Configure Wi-Fi hotspot with NetworkManager
    run_subprocess(
        [
            "sudo",
            "nmcli",
            "connection",
            "add",
            "con-name",
            WIFI_HOTSPOT_CONNECTION_NAME,
            "type",
            "wifi",
            "ifname",
            interface_name,
            "wifi.mode",
            "ap",
            "wifi.ssid",
            ssid,
            "wifi-sec.key-mgmt",
            "wpa-psk",
            "wifi-sec.psk",
            password,
            "ipv4.method",
            "shared",
            "connection.autoconnect",
            autoconnect,
            "connection.autoconnect-priority",
            autoconnect_priority,
        ]
    )
