# python-mattebox

Unofficial Python library for MatteBOX IPTV.

## Installing

```shell
$ python -m pip install mattebox
```

## Usage

```python
>>> from mattebox import MatteBOX
>>> mbox = MatteBOX(USERNAME, PASSWORD, DEVICE_ID, SUBSCRIPTION_CODE)
```

### Examples

```python  
>>> # get list of TV channels
>>> channels = mbox.channels

>>> # get list of programs on specified channel
>>> programs = mbox.get_programs(channels[0])

>>> # get recordings
>>> recordings = mbox.recordings

>>> # get stream URL for specified program/recording
>>> stream = mbox.get_stream(programs[0])

>>> # search for TV program
>>> results = mbox.search("Masza i niedźwiedź")
```
