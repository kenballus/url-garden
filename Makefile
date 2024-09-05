.PHONY: run build clean

build:
	git clone "https://github.com/AFLplusplus/AFLplusplus" && cd AFLplusplus && make -j$$(nproc)
	cd targets && for target in *; do cd "$$target" && make; cd ..; done

clean:
	rm -rf AFLplusplus
	cd targets && for target in *; do cd "$$target" && make clean; cd ..; done
