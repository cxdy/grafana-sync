# grafana-migrate

welcome to my nightmare

# DISCLAIMER
please do not use this in production (or at all)

i'm an idiot (but I didn't break anything, *yet*)

## what is this

I don't know. I messed up by manually copying and modifying SQL from one Grafana database to another, so I figured I'd write something that can handle that for you (albeit slowly in big installs)

## what does it do

Connects to Grafana instance(s) and backs up all of your dashboards, teams, and folders into JSON files. That's it.

You can also backup your users, I just didn't want to do it for my purposes but could make it optional down the line perhaps. 

## what do you plan for it to do

Much more hopefully. Actual plans include:

* Being able to bring a Grafana database to a clean slate, and import back to it.
* Automatically update `datasource_uid`s on import to whatever you specify.
* Handle permissions in batch - I have code for this already, but it didn't make the cut for the first commit.

Minimal list for now, but I'm sure I'm going to run into more things that make me want to scalp myself while trying to replicate Grafana configs that are [similar but not quite that similar](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTY2azF5Z2h4Y3R6dGJwN3l6YW9yYXFxeHBuM3J0bzFmMTVkaDFhayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/uNE1fngZuYhIQ/200.webp).

## usage

bless your soul..

go ahead and copy `config-example.yaml` to `config.yaml`.

```yaml
config:
  envrionment_1:
    url: # https://url.to.your.grafana.com:3000
    token: # I used a Service Account token, but the User API (with admin) should be enough.
    dir: # Path where you want your JSON files dumped to
  envrionment_2:
    url: # https://url.to.your.other.grafana.com:3000
    token: # I used a Service Account token, but the User API (with admin) should be enough.
    dir: # Path where you want your JSON files dumped to
```

for the JSON output files, i structured my directories like this:

*as-is, this software will assume the same structure*
```console
➜  grafana-migrate git:(main) ✗ tree
.
├── README.md
├── config.yaml
├── main.py
├── out
│   ├── environment_1
│   │   ├── dashboards
│   │   ├── debug
│   │   ├── folders
│   │   └── teams
│   └── environment_2
│       ├── dashboards
│       ├── debug
│       ├── folders
│       └── teams
├── util.log
└── util.py
```

once you have all of that and your config is all good to go, all you need to do is run
```console
$ python3 main.py
```

and wait. like a while.

performance is really bad. again, don't use this.