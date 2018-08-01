INSTALL ?= install
INSTALL_DIR ?= $(CURDIR)/install
BUILD_DIR   ?= $(CURDIR)/build

HEADER_FILES += $(shell find include -name *.hpp)
HEADER_FILES += $(shell find include -name *.h)

define declareInstallFile

$(INSTALL_DIR)/$(1): $(1)
	$(INSTALL) -D $(1) $$@

INSTALL_HEADERS += $(INSTALL_DIR)/$(1)

endef

HEADER_FILES += $(shell find python -name *.py)

$(foreach file, $(HEADER_FILES), $(eval $(call declareInstallFile,$(file))))


BUILD_DIR = build

CFLAGS += -std=gnu++11 -MMD -MP -O3 -g -Iinclude -fPIC

SRCS = src/jsmn.cpp src/json.cpp

OBJS = $(patsubst %.cpp,$(BUILD_DIR)/%.o,$(patsubst %.c,$(BUILD_DIR)/%.o,$(SRCS)))

-include $(OBJS:.o=.d)

$(BUILD_DIR)/%.o: %.cpp
	@mkdir -p $(basename $@)
	g++ $(CFLAGS) -o $@ -c $<

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(basename $@)
	g++ $(CFLAGS) -o $@ -c $<

$(BUILD_DIR)/libjson.a: $(OBJS)
	ar -r $@ $^

$(INSTALL_DIR)/lib/libjson.a: $(BUILD_DIR)/libjson.a
	$(INSTALL) -D $< $@

header: $(INSTALL_HEADERS)

build: $(INSTALL_DIR)/lib/libjson.a

clean:
	rm -rf $(BUILD_DIR)

all: header build
