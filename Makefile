CWD    = $(CURDIR)
MODULE = metaL
# $(notdir $(CWD))

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest

WGET = wget -c --no-check-certificate

IP	 ?= 127.0.0.1
PORT ?= 19999


.PHONY: all py flask rust nim test
all: nim


flask: $(PY) $(MODULE).py $(MODULE).ini flask.ini
	IP=$(IP) PORT=$(PORT) $^
py: $(PY) $(MODULE).py $(MODULE).ini
	IP=$(IP) PORT=$(PORT) $^
test: $(PYT) test_$(MODULE).py $(MODULE).py
	$(PYT) test_$(MODULE).py


nim: ./metaL metaL.ini
	./$^
./metaL: src/metaL.nim metaL.nimble
	nimpretty $<
	nimble build


RS = src/main.rs
rust: target/debug/metal $(MODULE).ini
	IP=$(IP) PORT=$(PORT) RUST_LOG=debug $^
target/debug/metal: Cargo.toml $(RS) Makefile
	cargo build



.PHONY: install
install: debian $(PIP) js
	$(PIP) install    -r requirements.txt
	$(MAKE) requirements.txt

.PHONY: update
update: debian $(PIP)
	$(PIP) install -U    pip
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt

$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
$(PYT):
	$(PIP) install -U pytest
	$(MAKE) requirements.txt

.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@

.PHONY: debian
debian:
	sudo apt update
	sudo apt install -u `cat apt.txt`



.PHONY: js
js: static/jquery.js static/bootstrap.css static/bootstrap.js \
	static/go.js static/g6.js

JQUERY_VER = 3.5.0
static/jquery.js:
	$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js

BOOTSTRAP_VER = 3.4.1
BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css
static/bootstrap.js:
	$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js

GOJS_VER = 2.1
static/go.js:
	$(WGET) -O $@ https://unpkg.com/gojs@$(GOJS_VER)/release/go.js

G6_VER = 3.3.1
static/g6.js:
	$(WGET) -O $@ https://gw.alipayobjects.com/os/antv/pkg/_antv.g6-$(G6_VER)/dist/g6.min.js



.PHONY: master shadow release zip

MERGE  = Makefile README.md .gitignore .vscode apt.txt requirements.txt doc
MERGE += $(MODULE).py $(MODULE).ini
MERGE += flask.ini static templates
MERGE += src Cargo.toml
MERGE += $(MODULE).nimble src/$(MODULE).nim

master:
	git checkout $@
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	git checkout shadow

zip:
	git archive --format zip --output $(MODULE)_src_$(NOW)_$(REL).zip HEAD


.PHONY: doc
doc: doc/CMU-CS-95-113.pdf
doc/CMU-CS-95-113.pdf:
	$(WGET) -O $@ http://reports-archive.adm.cs.cmu.edu/anon/1995/CMU-CS-95-113.pdf
