import os
import tempfile
import subprocess
import getpass
import shutil
from textwrap import dedent

def setup_shiny():
    '''Manage a Shiny instance.'''

    name = 'shiny'
    def _get_shiny_cmd(port):
        conf = dedent("""
            run_as {user};
            server {{
                listen {port};
                location / {{
                    site_dir {site_dir};
                    log_dir {site_dir}/logs;
                    directory_index on;
                }}
            }}
        """).format(
            user=getpass.getuser(),
            port=str(port),
            site_dir=os.getcwd()
        )

        f = tempfile.NamedTemporaryFile(mode='w', delete=False)
        f.write(conf)
        f.close()
        return ['shiny-server', f.name]

    return {
        'command': _get_shiny_cmd,
        'launcher_entry': {
            'title': 'Shiny',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'shiny.svg')
        }
    }

def setup_rstudio():
    def _get_rsession_env(port):
        # Detect various environment variables rsession requires to run
        # Via rstudio's src/cpp/core/r_util/REnvironmentPosix.cpp
        cmd = ['R', '--slave', '--vanilla', '-e',
                'cat(paste(R.home("home"),R.home("share"),R.home("include"),R.home("doc"),getRversion(),sep=":"))']

        r_output = subprocess.check_output(cmd)
        R_HOME, R_SHARE_DIR, R_INCLUDE_DIR, R_DOC_DIR, version = \
            r_output.decode().split(':')

        return {
            'R_DOC_DIR': R_DOC_DIR,
            'R_HOME': R_HOME,
            'R_INCLUDE_DIR': R_INCLUDE_DIR,
            'R_SHARE_DIR': R_SHARE_DIR,
            'RSTUDIO_DEFAULT_R_VERSION_HOME': R_HOME,
            'RSTUDIO_DEFAULT_R_VERSION': version,
        }

    def _get_rsession_cmd(port):
        # Other paths rsession maybe in
        other_paths = [
            # When rstudio-server deb is installed
            '/usr/lib/rstudio-server/bin/rsession',
            # When just rstudio deb is installed
            '/usr/lib/rstudio/bin/rsession',
        ]
        if shutil.which('rsession'):
            executable = 'rsession'
        else:
            for op in other_paths:
                if os.path.exists(op):
                    executable = op
                    break
            else:
                raise FileNotFoundError('Can not find rsession in PATH')

        return [
            executable,
            '--standalone=1',
            '--program-mode=server',
            '--log-stderr=1',
            '--session-timeout-minutes=0',
            '--user-identity=' + getpass.getuser(),
            '--www-port=' + str(port)
        ]

    return {
        'command': _get_rsession_cmd,
        'environment': _get_rsession_env,
        'launcher_entry': {
            'title': 'RStudio',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'rstudio.svg')
        }
    }