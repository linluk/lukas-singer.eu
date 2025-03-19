#
# Makefile for lukas-singer.eu
#
# Created: 2025-03-13
# Author: Lukas Singer
# Description: Build the Website from src/**/*.md files to www/**/*.html using pandoc.
#              Copy resources (images, ...) from src/**/*.(png|jpg|...) to www/**/*.(png|jpg|...)
#              Create minified Scripts and Stylesheets from src/**/*.(css|js) to www/**/*.(css|js)
#              Cleanup www/**/*
#
#MAKEFLAGS += --jobs=$(shell nproc)

PANDOC                := $(shell which pandoc)
MINIFY                := $(shell which minify)
MINIFY_JS             := $(MINIFY)
MINIFY_CSS            := $(MINIFY)
FFMPEG                := $(shell which ffmpeg)
PYTHON                := $(shell which python3)

PANDOC_VERSION        := $(shell $(PANDOC) --version | head -n 1)
PANDOC_TEMPLATE       := template.html
PANDOC_FLAGS          := --from=markdown \
						 --to=html5 \
						 --table-of-contents \
						 --lua-filter=tools/fix_links.lua \
						 --lua-filter=tools/obfuscate.lua \
						 --highlight-style=zenburn \
						 --variable pandoc-details="$(PANDOC_VERSION)" \
						 --template="$(PANDOC_TEMPLATE)" \
						 --email-obfuscation=javascript

FFMPEG_FLAGS          := -hide_banner \
						 -loglevel error

# find all *.md files in src/ except files called index.md in src/blog
MARKDOWN_SOURCES      := $(shell find src/ -type f \( -name "*.md" -a ! -regex "src\/blog\/.*index.md" \))
# get index.md for each directory in src/blog does not matter if it exists or not
BLOG_INDEX_SOURCES    := $(foreach blog_dir,$(shell find src/blog -type d),$(blog_dir)/index.md)
STYLE_SOURCES         := $(shell find src/ -type f -name "*.css")
SCRIPT_SOURCES        := $(shell find src/ -type f -name "*.js")
RESOURCE_SOURCES      := $(shell find src/ -type f \( -name "*.pdf" -o -name "*.png" \))

HTML_DESTINATIONS     := $(patsubst src/%,www/%,$(patsubst %.md,%.html,$(MARKDOWN_SOURCES) $(BLOG_INDEX_SOURCES)))
STYLE_DESTINATIONS    := $(patsubst src/%,www/%,$(STYLE_SOURCES))
SCRIPT_DESTINATIONS   := $(patsubst src/%,www/%,$(SCRIPT_SOURCES))
RESOURCE_DESTINATIONS := $(patsubst src/%,www/%,$(RESOURCE_SOURCES))

SOURCES               := $(MARKDOWN_SOURCES) $(STYLE_SOURCES) $(SCRIPT_SOURCES) $(RESOURCE_SOURCES)
DESTINATIONS          := $(BLOG_INDEX_SOURCES) $(HTML_DESTINATIONS) $(STYLE_DESTINATIONS) $(SCRIPT_DESTINATIONS) $(RESOURCE_DESTINATIONS)

.PHONY: all clean info

all: $(DESTINATIONS)

www/%.html: src/%.md $(PANDOC_TEMPLATE)
	mkdir -p $(dir $@)
	$(PANDOC) $(PANDOC_FLAGS) --output=$@ $<

src/blog/%/index.md:
	$(PYTHON) tools/blog.py --update

src/blog/index.md:
	$(PYTHON) tools/blog.py --update

www/%.css: src/%.css
	mkdir -p $(dir $@)
	$(MINIFY_CSS) $< -o $@

www/%.js: src/%.js
	mkdir -p $(dir $@)
	$(MINIFY_JS) $< -o $@

www/%.png: src/%.png
	mkdir -p $(dir $@)
	$(FFMPEG) $(FFMPEG_FLAGS) -i $< -vf scale="'min(1000,iw)':-1" $@

www/%: src/%
	mkdir -p $(dir $@)
	cp $< $@

clean:
	rm -rf www/*
	rm -f $(BLOG_INDEX_SOURCES)

info:
	@echo "MINIFY                = $(MINIFY)"
	@echo "MINIFY_JS             = $(MINIFY_JS)"
	@echo "MINIFY_CSS            = $(MINIFY_CSS)"
	@echo "FFMPEG                = $(FFMPEG)"
	@echo "PYTHON                = $(PYTHON)"
	@echo "PANDOC                = $(PANDOC)"
	@echo "PANDOC_VERSION        = $(PANDOC_VERSION)"
	@echo "PANDOC_TEMPLATE       = $(PANDOC_TEMPLATE)"
	@echo "PANDOC_FLAGS          = $(PANDOC_FLAGS)"
	@echo "MARKDOWN_SOURCES      = $(MARKDOWN_SOURCES)"
	@echo "BLOG_INDEX_SOURCES    = $(BLOG_INDEX_SOURCES)"
	@echo "STYLE_SOURCES         = $(STYLE_SOURCES)"
	@echo "SCRIPT_SOURCES        = $(SCRIPT_SOURCES)"
	@echo "RESOURCE_SOURCES      = $(RESOURCE_SOURCES)"
	@echo "HTML_DESTINATIONS     = $(HTML_DESTINATIONS)"
	@echo "STYLE_DESTINATIONS    = $(STYLE_DESTINATIONS)"
	@echo "SCRIPT_DESTINATIONS   = $(SCRIPT_DESTINATIONS)"
	@echo "RESOURCE_DESTINATIONS = $(RESOURCE_DESTINATIONS)"
	@echo "SOURCES               = $(SOURCES)"
	@echo "DESTINATIONS          = $(DESTINATIONS)"



