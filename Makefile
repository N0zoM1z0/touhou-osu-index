.PHONY: build check test validate import-seeds audit-sources hydrate clean

build:
	python3 -m touhou_osu build

check: test validate

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 -m touhou_osu validate

import-seeds:
	python3 -m touhou_osu import-seeds --write

audit-sources:
	python3 -m touhou_osu audit-sources

hydrate:
	python3 -m touhou_osu hydrate --write

clean:
	python3 -m touhou_osu clean
