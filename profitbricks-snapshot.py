#!/usr/bin/env python

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

from datetime import datetime, timedelta
from profitbricks.client import ProfitBricksService

# read config
config = ConfigParser()
config.read('settings.cfg')

datacenter_id = config.get('snapshots', 'datacenter_id')
snapshot_prefix = config.get('snapshots', 'snapshot_prefix')
retention_time = config.getint('snapshots', 'retention_time')

pb = ProfitBricksService(
    username=config.get('credentials', 'username'),
    password=config.get('credentials', 'password'),
)

# timestamp for creating and deleting
now = datetime.now()

# create new snapshots from list of volumes in datacenter
volumes = pb.list_volumes(datacenter_id=datacenter_id)

for volume_item in volumes['items']:
    volume_id = volume_item['id']
    volume = pb.get_volume(datacenter_id, volume_id)

    volume_name = volume['properties']['name']
    snapshot_name = "{}-{}-{}".format(snapshot_prefix, now.strftime("%Y%m%d"), volume_name)

    print("creating snapshot: {}".format(snapshot_name))
    pb.create_snapshot(datacenter_id, volume_id, snapshot_name)

# delete old snapshots
snapshots = pb.list_snapshots()

for snapshot_item in snapshots['items']:
    snapshot_id = snapshot_item['id']
    snapshot = pb.get_snapshot(snapshot_id)

    snapshot_name = snapshot['properties']['name']
    if not snapshot_name.startswith(snapshot_prefix):
        continue

    snapshot_created = snapshot['metadata']['createdDate']
    snapshot_date = datetime.strptime(snapshot_created, "%Y-%m-%dT%H:%M:%SZ")

    if snapshot_date < now - timedelta(days=retention_time):
        print("deleting snapshot: {} (created: {})".format(snapshot_name, snapshot_created))
        pb.delete_snapshot(snapshot_id)