import re

from atproto import IdResolver, models

RX_TAG = re.compile(r'#\w+')
RX_MENTION = re.compile(r'@([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?')
RX_LINK = re.compile(r'https?://[\w\-_#%&;./]+')

def find_facets(rx, text):
    res = []
    text_bytes = text.encode('UTF-8')
    for item in rx.finditer(text_bytes):
        res.append((item.start(), item.end(), item.group().decode('UTF-8')))

    return res

def pull_out_facets(text):
    facets = []
    for facet in find_facets(RX_TAG, text):
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Tag(tag=facet[2][1:])],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=facet[0], byte_end=facet[1]),
            )
        )

    resolver = IdResolver()
    for facet in find_facets(RX_MENTION, text):
        did = resolver.handle.resolve(facet[2][1:])
        if did:
            facets.append(
                models.AppBskyRichtextFacet.Main(
                    features=[models.AppBskyRichtextFacet.Mention(did=did)],
                    index=models.AppBskyRichtextFacet.ByteSlice(byte_start=facet[0], byte_end=facet[1]),
                )
            )
        else:
            print(f'handle {facet[2]} not found')

    for facet in find_facets(RX_LINK, text):
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=facet[2])],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=facet[0], byte_end=facet[1]),
            )
        )

    return facets

