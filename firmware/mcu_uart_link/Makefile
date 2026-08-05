CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2 -g

TEST := test_mcu_uart_protocol

.PHONY: all test clean

all: $(TEST)

$(TEST): test_mcu_uart_protocol.c mcu_uart_protocol.c mcu_uart_protocol.h
	$(CC) $(CFLAGS) -o $@ test_mcu_uart_protocol.c mcu_uart_protocol.c

test: $(TEST)
	./$(TEST)

clean:
	rm -f $(TEST)
