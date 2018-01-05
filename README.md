# Pager Pull

This project views pagerduty as an extention of the notifyd system and ties pagerduty into it for a broader range of notification options.

**Pager Pull**: Starts a long pull and uses notify-send to trigger a local alert
**Pager Push**: Emulates the notify-send cli tool but pushes the notification to pagerduty for broader notification

## Install

This isn't published to pip yet. First, clone the repo. Then use pip, you can optionally add the `--editable` flag for local development.
```
sudo pip install ./
```

## Example Pager-Pull Use

You can add it to your `.xinit` with the following assuming you've added your token to disk.
```
pager-pull -i 30 -p $(cat /tmp/pagerduty-token) &
```

You can also use a password manager like [lastpass](https://github.com/lastpass/lastpass-cli)
```
pager-pull -i 30 -p $(lpass show -xG pagerduty-token --field user[password]) &
```

For convenience
```
Usage: pager-pull [OPTIONS]

  Pager Pull: A simple app to long-pull from pagerduty and trigger a system
  notifier like notify-send.

Options:
  -p, --password TEXT  Pagerduty token optionally $PAGER_TOKEN
  -i, --interval TEXT  Pull interval, 15s default
  -n, --notifier TEXT  Notification application, default: notify-send
  --help               Show this message and exit.
```

## Example Pager-Push Use
