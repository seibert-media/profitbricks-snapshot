# profitbricks-snapshot

profitbricks-snapshot is a tool to create daily block based images of virtual machines in the [Profitbricks](https://www.profitbricks.com/) private cloud.
It also deletes snapshots that are older than a defined retention time in days.

## Installation

1. Get profitbricks-snapshot:

    ``git clone https://github.com/seibert-media/profitbricks-snapshot.git``

1. Install python requirements:

    ``pip install -r requirements.txt``

1. Create and adjust your settings:

    ``cp settings.cfg.example settings.cfg``

1. Execute profitbricks-snapshot every day via cron:

    ``crontab -e``

    ``0 3 * * * cd /path/to/profitbricks-snapshot && python profitbricks-snapshot.py``

## Settings

Example settings.cfg:

	[credentials]
	username: user@domain.com
	password: secret

	[snapshots]
	datacenter_id: abc12345a-12ab-3a4b-1a23-1ab2cd345e67
	snapshot_prefix: AUTOSNAP
	retention_time: 7
	sleep_seconds: 60

- credentials:
Username and password of your Profitbricks account.

- datacenter_id:
All volumes in this datacenter will be snapshotted.

- snapshot_prefix:
Prefix string of snapshot names. Name of snapshots from example: "AUTOSNAP-*YYYMMDD*-*VOLUMENAME*"

- retention_time:
Retention time in days. Older snapshots will be deleted.

- sleep_seconds:
Number of seconds to wait between the creation of snapshots.

## Usage

	python profitbricks-snapshot.py

## License

This project is licensed under the terms of the [MIT license](LICENSE.md).
