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

# executables
PANDOC                  := $(shell which pandoc)
MINIFY                  := $(shell which minify)
MINIFY_JS               := $(MINIFY)
MINIFY_CSS              := $(MINIFY)
FFMPEG                  := $(shell which ffmpeg)
PYTHON                  := $(shell which python3)
BASH                    := $(shell which bash)

# scripts and tools
CREATE_HIGHLIGHT_CSS    := tools/create-highlight-css.sh
CREATE_BLOG_INDEX       := tools/blog.py
CREATE_BLOG_INDEX_FLAGS := --update

PANDOC_VERSION          := $(shell $(PANDOC) --version | head -n 1)
PANDOC_TEMPLATE         := template.html
PANDOC_FLAGS            := --from=markdown \
						   --to=html5 \
						   --table-of-contents \
						   --lua-filter=tools/fix_links.lua \
						   --lua-filter=tools/obfuscate.lua \
						   --variable pandoc-details="$(PANDOC_VERSION)" \
						   --template="$(PANDOC_TEMPLATE)" \
						   --email-obfuscation=javascript
#--highlight-style=zenburn

FFMPEG_FLAGS            := -hide_banner \
						   -loglevel error

# find all *.md files in src/ except files called index.md in src/blog
MARKDOWN_SOURCES        := $(shell find src/ -type f \( -name "*.md" -a ! -regex "src\/blog\/.*index\.md" \))
# get index.md for each directory in src/blog does not matter if it exists or not
# 'find src/blog -type d' will give all subdirectories of AND src/blog itself.
BLOG_INDEX_SOURCES      := $(foreach blog_dir,$(shell find src/blog -type d),$(blog_dir)/index.md)
STYLE_HIGHLIGHT_SOURCE  := src/highlight.css
# 'find src/ -type f \( -name "*.css" -a ! -regex "src\/highlight\.css"' will get us all '*.css' files 
# except 'src/highlight.css' which may or may not exists, so wee add it manually.
# thats how we avoid to duplicate it in $STYLE_SOURCES
STYLE_SOURCES           := $(shell find src/ -type f \( -name "*.css" -a ! -regex "src\/highlight\.css" \)) $(STYLE_HIGHLIGHT_SOURCE)
SCRIPT_SOURCES          := $(shell find src/ -type f -name "*.js")
RESOURCE_SOURCES        := $(shell find src/ -type f \( -name "*.pdf" -o -name "*.png" \))

HTML_DESTINATIONS       := $(patsubst src/%,www/%,$(patsubst %.md,%.html,$(MARKDOWN_SOURCES) $(BLOG_INDEX_SOURCES)))
STYLE_DESTINATIONS      := $(patsubst src/%,www/%,$(STYLE_SOURCES))
SCRIPT_DESTINATIONS     := $(patsubst src/%,www/%,$(SCRIPT_SOURCES))
RESOURCE_DESTINATIONS   := $(patsubst src/%,www/%,$(RESOURCE_SOURCES))

SOURCES                 := $(MARKDOWN_SOURCES) $(STYLE_SOURCES) $(SCRIPT_SOURCES) $(RESOURCE_SOURCES)
DESTINATIONS            := $(BLOG_INDEX_SOURCES) $(HTML_DESTINATIONS) $(STYLE_DESTINATIONS) $(SCRIPT_DESTINATIONS) $(RESOURCE_DESTINATIONS)


.PHONY: all clean info

all: $(DESTINATIONS)

www/%.html: src/%.md $(PANDOC_TEMPLATE)
	mkdir -p $(dir $@)
	$(PANDOC) $(PANDOC_FLAGS) --output=$@ $<

src/blog/%/index.md: $(CREATE_BLOG_INDEX)
	$(PYTHON) $(CREATE_BLOG_INDEX) $(CREATE_BLOG_INDEX_FLAGS)

src/blog/index.md: $(CREATE_BLOG_INDEX)
	$(PYTHON) $(CREATE_BLOG_INDEX) $(CREATE_BLOG_INDEX_FLAGS)

src/highlight.css: $(CREATE_HIGHLIGHT_CSS)
	$(BASH) $(CREATE_HIGHLIGHT_CSS)

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
	rm -f $(STYLE_HIGHLIGHT_SOURCE)

info:
	@echo "MINIFY                  = $(MINIFY)"
	@echo "MINIFY_JS               = $(MINIFY_JS)"
	@echo "MINIFY_CSS              = $(MINIFY_CSS)"
	@echo "FFMPEG                  = $(FFMPEG)"
	@echo "PYTHON                  = $(PYTHON)"
	@echo "PANDOC                  = $(PANDOC)"
	@echo "BASH                    = $(BASH)"
	@echo "CREATE_HIGHLIGHT_CSS    = $(CREATE_HIGHLIGHT_CSS)"
	@echo "CREATE_BLOG_INDEX       = $(CREATE_BLOG_INDEX)"
	@echo "CREATE_BLOG_INDEX_FLAGS = $(CREATE_BLOG_INDEX_FLAGS)"
	@echo "PANDOC_VERSION          = $(PANDOC_VERSION)"
	@echo "PANDOC_TEMPLATE         = $(PANDOC_TEMPLATE)"
	@echo "PANDOC_FLAGS            = $(PANDOC_FLAGS)"
	@echo "MARKDOWN_SOURCES        = $(MARKDOWN_SOURCES)"
	@echo "BLOG_INDEX_SOURCES      = $(BLOG_INDEX_SOURCES)"
	@echo "STYLE_HIGHLIGHT_SOURCE  = $(STYLE_HIGHLIGHT_SOURCE)"
	@echo "STYLE_SOURCES           = $(STYLE_SOURCES)"
	@echo "SCRIPT_SOURCES          = $(SCRIPT_SOURCES)"
	@echo "RESOURCE_SOURCES        = $(RESOURCE_SOURCES)"
	@echo "HTML_DESTINATIONS       = $(HTML_DESTINATIONS)"
	@echo "STYLE_DESTINATIONS      = $(STYLE_DESTINATIONS)"
	@echo "SCRIPT_DESTINATIONS     = $(SCRIPT_DESTINATIONS)"
	@echo "RESOURCE_DESTINATIONS   = $(RESOURCE_DESTINATIONS)"
	@echo "SOURCES                 = $(SOURCES)"
	@echo "DESTINATIONS            = $(DESTINATIONS)"



