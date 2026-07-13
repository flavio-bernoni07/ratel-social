# Account and Person Rules

## Account field — verify live before every write

The Notion `Account` property is a **multi_select**, not free text (this drifted from the old
repo's docs once already — always confirm against the live schema with `notion-fetch` /
`notion-query-database-view` before assuming these options still exist). As of the last live check
(2026-07-13), the valid options are:

```
Linkedin Ratel, Linkedin Rob, Linkedin Giac, Linkedin Others,
X Ratel, X Rob, X Giac, X Others,
Reddit Jack
```

Writes must send an array of exact, existing option strings. Anything else either errors or fails
to render as a chip — never invent a new option string without adding it to the Notion schema
first (and that requires explicit sign-off, since it changes a database Luce and Giacomo also use).

**Reddit has only one option today: `Reddit Jack`.** There is no `Reddit Ratel` or `Reddit Rob`.
Default every Reddit draft to `Reddit Jack` unless a new option has been explicitly added to the
schema. This actually fits Reddit's anti-corporate norms — a personal account outperforms a brand
account there anyway.

### Picking LinkedIn/X accounts by angle

- Ratel main channel is the default posting channel.
- Giacomo (business/mission angle posts) → add `Linkedin Giac` / `X Giac` as a repost tag.
- Roberto (technical depth posts) → add `Linkedin Rob` / `X Rob` as a repost tag.
- Adjust based on post angle: business-heavy → Giacomo only; deep technical → Roberto only.

## Person field (Notion user IDs)

Tag the people who should be involved. Always include Flavio as author. Add founders if they're
tagged in the Account field.

```
Flavio Bernoni: 381d872b-594c-81d0-9467-0002bc30e9d6
Giacomo Nicoli: 2d8d872b-594c-8156-bfba-0002cf3a43cc
Roberto Stagi:  2c0d872b-594c-81ca-85d8-0002ac856983
Kayra Üçkılınç: 36dd872b-594c-81cf-b247-0002e54ceb0d
Berca Akbayir:  381d872b-594c-812c-93de-0002dcc8e3f0
```

Pass as a JSON array of IDs, e.g.
`["381d872b-594c-81d0-9467-0002bc30e9d6", "2d8d872b-594c-8156-bfba-0002cf3a43cc"]`.
