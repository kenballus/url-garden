.PHONY: clean

venv:
	python3 -m venv venv
	git clone --recurse-submodules "https://github.com/jwilk/python-afl" && ./venv/bin/pip3 install ./python-afl && rm -rf ./python-afl

clean:
	rm -rf ./venv
