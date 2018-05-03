echo $PATH
sleep 5

#cd ~/Documents/projects/micropython/micropython-ciy/toolchain/esp-open-sdk/
rm -rf micropython


git clone --recursive https://github.com/micropython/micropython.git
cd micropython/

git submodule update --init

cp -r ~/Documents/projects/micropython/micropython-ciy/testmodules/* ~/Documents/projects/micropython/micropython-ciy/toolchain/esp-open-sdk/micropython/ports/esp8266/modules/

#ls ~/Documents/projects/micropython/micropython-ciy/toolchain/esp-open-sdk/micropython/ports/esp8266/modules/

make -C mpy-cross

cd ~/Documents/projects/micropython/micropython-ciy/toolchain/esp-open-sdk/micropython/ports/esp8266/

make axtls
make

ls ~/Documents/projects/micropython/micropython-ciy/toolchain/esp-open-sdk/micropython/ports/esp8266/build/firmware-combined.bin

cp ~/Documents/projects/micropython/micropython-ciy/toolchain/esp-open-sdk/micropython/ports/esp8266/build/firmware-combined.bin ~/Documents/projects/micropython/micropython-ciy/buildedfirmwares
