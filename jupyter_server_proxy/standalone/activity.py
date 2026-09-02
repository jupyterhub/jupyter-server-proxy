import json
import os
from datetime import datetime

from jupyterhub.utils import exponential_backoff, isoformat
from tornado import httpclient, ioloop
from tornado.log import app_log as log


async def notify_activity():
    """
    Regularly notify JupyterHub of activity.
    See https://github.com/jupyterhub/jupyterhub/blob/4.x/jupyterhub/singleuser/extension.py#L389
    """

    client = httpclient.AsyncHTTPClient()
    last_activity_timestamp = isoformat(datetime.utcnow())
    failure_count = 0

    activity_url = os.environ.get("JUPYTERHUB_ACTIVITY_URL")
    server_name = os.environ.get("JUPYTERHUB_SERVER_NAME")
    api_token = os.environ.get("JUPYTERHUB_API_TOKEN")

    if not (activity_url and server_name and api_token):
        log.error(
            "Could not find environment variables to send notification to JupyterHub"
        )
        return

    async def notify():
        """Send Notification, return if successful"""
        nonlocal failure_count
        log.debug(f"Notifying Hub of activity {last_activity_timestamp}")

        req = httpclient.HTTPRequest(
            url=activity_url,
            method="POST",
            headers={
                "Authorization": f"token {api_token}",
                "Content-Type": "application/json",
            },
            body=json.dumps(
                {
                    "servers": {
                        server_name: {"last_activity": last_activity_timestamp}
                    },
                    "last_activity": last_activity_timestamp,
                }
            ),
        )

        try:
            await client.fetch(req)
            return True
        except httpclient.HTTPError as e:
            failure_count += 1
            log.error(f"Error notifying Hub of activity: {e}")
            return False

    # Try sending notification for 1 minute
    await exponential_backoff(
        notify,
        fail_message="Failed to notify Hub of activity",
        start_wait=1,
        max_wait=15,
        timeout=60,
    )

    if failure_count > 0:
        log.info(f"Sent hub activity after {failure_count} retries")


def start_activity_update(interval):
    pc = ioloop.PeriodicCallback(notify_activity, 1e3 * interval, 0.1)
    pc.start()
