.PHONY: build assemble check test validate audit-pr import-seeds audit-sources hydrate clean

BASE ?= main
MODE ?= structural
SCOPE ?= changed
WORKERS ?= 4

build:
	python3 -m touhou_osu build

assemble:
	python3 -m touhou_osu assemble

check: test validate

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 -m touhou_osu validate

audit-pr:
	python3 -m touhou_osu.pr_audit --base-ref "$(BASE)" --mode "$(MODE)" --scope "$(SCOPE)" --workers "$(WORKERS)" \
		$(if $(AUDIT_DOC),--audit-doc "$(AUDIT_DOC)") \
		$(if $(EXPECTED_ADDITIONS),--expected-additions "$(EXPECTED_ADDITIONS)") \
		$(if $(filter 1 true yes,$(FORBID_EXISTING_CHANGES)),--forbid-existing-changes) \
		$(if $(filter 1 true yes,$(ALLOW_REMOVALS)),--allow-removals) \
		$(if $(filter 1 true yes,$(REQUIRE_BASE_ANCESTOR)),--require-base-ancestor) \
		$(if $(AUDIT_OUTPUT),--output "$(AUDIT_OUTPUT)")

import-seeds:
	python3 -m touhou_osu import-seeds --write

audit-sources:
	python3 -m touhou_osu audit-sources

hydrate:
	python3 -m touhou_osu hydrate --write

clean:
	python3 -m touhou_osu clean
