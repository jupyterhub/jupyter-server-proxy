import os
import tempfile
import subprocess
import getpass
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
        'title': 'Shiny',
        'icon': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'shiny.svg')
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

    return {
        'command': [
            'rsession',
            '--standalone=1',
            '--program-mode=server',
            '--log-stderr=1',
            '--session-timeout-minutes=0',
            '--user-identity=' + getpass.getuser(),
            '--www-port={port}'
        ],
        'environment': _get_rsession_env,
        'title': 'RStudio',
        'icon': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'rstudio.svg')
    }