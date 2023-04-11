# load the config object for traitlets based configuration
c = get_config()  # noqa


c.ServerProxy.servers = {
    "code-server": {
        "command": [
            "code-server",
            "--auth=none",
            "--disable-telemetry",
            "--bind-addr=localhost:{port}",
        ],
        "timeout": 20,
        "launcher_entry": {"title": "VS Code"},
    }
}
