# MQL Demo

Setup

Configs will be read from `$TRANSFORM_HOME` (default: `~/transform`), add
`export TRANSFORM_HOME=path/to/your/location` to set a custom home

<!-- ```sql
-- clean the "additional data" from source tables
DELETE FROM demo_small.dim_matches WHERE ds = '2020-01-01';
``` -->

```shell
mql drop_cache --im_sure  #drop any tables in the cache
```

## Inspection

Once configured, examine metrics, measures, dimensions

```shell
mql list_names metrics
mql show metrics
mql describe metric transforms
```

## Querying

References a global registry of metrics and dimensions with automatic joining. The example configs use a system table to pull values, so the queries can be slow.

### Single source, multiple local dimensions

```shell
mql query --metrics '[transforms]' --dimensions '[ds]' --cache_mode=''
mql query --metrics '[transforms]' --dimensions '[ds, is_visible]' --cache_mode=''
```
* not returning in ds order

### Constraints

```shell
mql query --metrics '[transforms]' --dimensions '[ds]' --constraint '{"ds": "2020-10-05"}' --cache_mode=''
```

### Multiple sources, multiple dimensions (Auto-joins)

```shell
mql query --metrics '[transforms, visible_transforms]' --dimensions '[ds, "bot/good_or_evil"]' --constraint '{"ds": "2020-10-05"}' --cache_mode=''
```
* this breaks

## Dynamic Caching

### Create transforms by ds rollup

Writes results to cache

```shell
mql query --metrics '[transforms]' --dimensions '[ds]' --cache_mode='w'
```

### Pull from the cache (simple extract)

Reads cache and pulls it (no writes necessary)

```shell
mql query --metrics '[transforms]' --dimensions '[ds]' --cache_mode='rw'
```

<!-- ### Simulate new data having landed in the source

```sql
INSERT INTO demo_small.dim_matches VALUES
('568980',	'2020-10-01',	'1000004',	'1000002',	10,	7),
('569001',	'2020-10-01',	'1000009',	'1000007',	6,	5),
('569022',	'2020-10-01',	'1000017',	'1000023',	4,	2),
('569043',	'2020-10-01',	'1000022',	'1000005',	4,	2),
('569064',	'2020-10-01',	'1000028',	'1000003',	1,	9),
('569085',	'2020-10-01',	'1000005',	'1000027',	3,	4),
('569106',	'2020-10-01',	'1000016',	'1000003',	7,	10),
('569127',	'2020-10-01',	'1000013',	'1000007',	9,	10),
('569148',	'2020-10-01',	'1000015',	'1000002',	7,	8),
('569169',	'2020-10-01',	'1000024',	'1000026',	2,	10);

```

### Use and Refresh the cache

Pulls from the cache AND from (filtered) source; combines and updates the cache

```shell
mql query --metrics '[home_team_wins]' --dimensions '[ds]' --cache_mode='rw'
``` -->

### Multidimensional Aggregates

```sql
mql drop_cache --im_sure #reset
```

Create multidimensional aggregate

```shell
mql query --metrics '[transforms]' --dimensions '[ds, "bot/good_or_evil"]' --cache_mode='rw'
```

Uses cached multidimensional aggregate to efficiently aggregate to a single dimension

```shell
mql query --metrics '[transforms]' --dimensions '[ds]' --cache_mode='rw'
```

## Experimental

### Integration with native SQL via table generating functions

Use native SQL functionality (e.g. window functions)

```shell
mql beta sql --query "SELECT SUM(visible_transforms) OVER (ORDER BY ds ROWS UNBOUNDED PRECEDING) AS visible_transforms_cumsum, ds FROM TRANSFORMED(visible_transforms BY ds) ORDER BY ds DESC"  --cache_mode ''
```

Custom joins

```shell
mql beta sql --query "SELECT b.visible_transforms, v.bots, v.ds FROM TRANSFORMED(visible_transforms BY ds) b JOIN TRANSFORMED(bots BY ds) v ON v.ds = b.ds"  --cache_mode 'rw'
```
