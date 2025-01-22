# bskyposter

NOTE: Future interface.  As of now, just run the bskyposter on the
commandline in the foreground)


On Instagram, I used a service called "Later" to create scheduled posts.  E.g.
when I had a collection of images from one concert, and I'd planned to post 10
images from that, 3 times every day, I could easily do that.

But since the Bluesky API is so easy and openly available, I decided to create
my own app that can schedule posting for me, so here we are.

The app uses a mailer like concept, with a daemon watching the queue and
posting everything that's due, in combination with a tool to schedule, list or
remove queued posts.

As of now, this thing is not yet multi-user, so it can't run as a system wide
daemon yet, but it's in the works.

## Synopsis

```console
# Start the service
systemctl start bskyposter

# ...or enable it for start at boot
systemctl enable --now bskyposter

# Create a post
bskyqueue post --at 2026-01-01-00:00 happy-new-year.txt image-1.png image-2.jpg, ...

# Check queued jobs
bskyqueue ls [-v]

# Delete a queued job
bskyqueue rm 2026-01-01-00:00
```

## Usage

FIXME

## Installation

In the future, this will go on pypi.org

```console
pip install git+https://github.com/dickerdackel/bskyposter
```

## Support / Contributing

Issues can be opened on [Github](https://github.com/dickerdackel/bskyposter/issues)

## License

This software is provided under the MIT license.

See LICENSE file for details.
