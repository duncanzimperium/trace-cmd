# macOS

```
brew install gnu-sed
```

Then replace all `sed -i` with `gsed -i`, otherwise you get the error (https://singhkays.com/blog/sed-error-i-expects-followed-by-text/):

```
command a expects \ followed by text
```

# Toolchain

Reference: https://developer.android.com/ndk/guides/other_build_systems

```
export NDK=~/Library/Android/sdk/ndk/25.2.9519653
export TOOLCHAIN=$NDK/toolchains/llvm/prebuilt/darwin-x86_64
export TARGET=aarch64-linux-android
export API=28
export ABI=arm64-v8a
```

We need API 28 for the `glob` function.

# Building

```
mkdir build_install
export INSTALL_PREFIX=$(pwd)/build_install
git clone https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/
cd libtraceevent
make \
    CC=$TOOLCHAIN/bin/$TARGET$API-clang \
    AR=$TOOLCHAIN/bin/llvm-ar \
    NM=$TOOLCHAIN/bin/llvm-nm \
    PKG_CONFIG=$(pwd)/../fake-pkg-config.py \
    LDCONFIG=$(pwd)/../fake-ldconfig.py
make \
    DESTDIR=$INSTALL_PREFIX/ \
    PKG_CONFIG=$(pwd)/../fake-pkg-config.py \
    LDCONFIG=$(pwd)/../fake-ldconfig.py \
    libdir_relative=lib \
    prefix=. \
    install
cd ..

git clone https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/
cd libtracefs
make \
    LPTHREAD='' \
    CC=$TOOLCHAIN/bin/$TARGET$API-clang \
    AR=$TOOLCHAIN/bin/llvm-ar \
    NM=$TOOLCHAIN/bin/llvm-nm \
    PKG_CONFIG=$(pwd)/../fake-pkg-config.py \
    LDCONFIG=$(pwd)/../fake-ldconfig.py
make \
    DESTDIR=$INSTALL_PREFIX/ \
    PKG_CONFIG=$(pwd)/../fake-pkg-config.py \
    LDCONFIG=$(pwd)/../fake-ldconfig.py \
    libdir_relative=lib \
    prefix=. \
    install
cd ..

git clone https://github.com/facebook/zstd --branch v1.5.5 --depth 1
cmake -B zstd/build-android -S zstd/build/cmake -DCMAKE_TOOLCHAIN_FILE=$NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI=$ABI -DANDROID_PLATFORM=$API
cmake --build zstd/build-android --parallel
cmake --install zstd/build-android --prefix $INSTALL_PREFIX

make \
    LPTHREAD='' \
    LRT='' \
    PKG_CONFIG=$(pwd)/fake-pkg-config.sh \
    CC=$TOOLCHAIN/bin/$TARGET$API-clang \
    AR=$TOOLCHAIN/bin/llvm-ar \
    NM=$TOOLCHAIN/bin/llvm-nm \
    PKG_CONFIG=$(pwd)/fake-pkg-config.py \
    LDCONFIG=$(pwd)/fake-ldconfig.py
make \
    DESTDIR=$INSTALL_PREFIX/ \
    PKG_CONFIG=$(pwd)/fake-pkg-config.py \
    LDCONFIG=$(pwd)/fake-ldconfig.py \
    libdir_relative=lib \
    prefix=. \
    install
```