import re

from typing import NamedTuple

from atproto import IdResolver, models

RX_TAG = re.compile(r'#\w+')
RX_MENTION = re.compile(r'@([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?')
RX_LINK = re.compile(r'https?://[\w\-_#%&;./]+')


class Facet(NamedTuple):
    start: int
    end: int
    match: str


def find_facets(rx, text):
    res = []

    # Note: The bsky/atproto docs convert the utf8 string to bytes and match
    # on that, but that kills e.g. matching \w patterns.  So instead I use
    # normal string matching here, then encode the prefix to bytes and use
    # its length as start.  Same with end.  This way, I have the full utf8 rx
    # matching with the proper byte positions required by bsky.
    for item in rx.finditer(text):
        bytes_start = len(text[:item.start()].encode('utf8'))
        bytes_end = bytes_start + len(item.group().encode('utf8'))
        res.append(Facet(bytes_start, bytes_end, item.group()))

    return res

def pull_out_facets(text):
    facets = []
    for facet in find_facets(RX_TAG, text):
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Tag(tag=facet.match[1:])],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=facet.start, byte_end=facet.end),
            )
        )

    resolver = IdResolver()
    for facet in find_facets(RX_MENTION, text):
        did = resolver.handle.resolve(facet.match[1:])
        if did:
            facets.append(
                models.AppBskyRichtextFacet.Main(
                    features=[models.AppBskyRichtextFacet.Mention(did=did)],
                    index=models.AppBskyRichtextFacet.ByteSlice(byte_start=facet.start, byte_end=facet.end),
                )
            )
        else:
            print(f'handle {facet.match} not found')

    for facet in find_facets(RX_LINK, text):
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=facet.match)],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=facet.start, byte_end=facet.end),
            )
        )

    return facets
