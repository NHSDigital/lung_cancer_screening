PLANTUML_FILES := as-is-data-flow.puml pilot-to-be-data-flow.puml mvp-to-be-data-flow.puml national-to-be-data-flow.puml
PNGS := $(PLANTUML_FILES:.puml=.png)

%.png: %.puml
	plantuml -tpng $<

all: $(PNGS)
