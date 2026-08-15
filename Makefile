.PHONY: build check test validate clean

build:
	python3 -m touhou_osu build

check: test validate

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 -m touhou_osu validate

clean:
	python3 -m touhou_osu clean
