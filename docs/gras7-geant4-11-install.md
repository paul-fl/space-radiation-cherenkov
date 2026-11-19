# Installing Geant4 11.3 + GRAS 7 on a modern Linux machine without root

Tested November 2026 on a rolling-release Linux distribution (GCC 16, 16 cores).

Everything is in `~/software`, built from source, no sudo needed.
Order: cmake -> xerces-c -> Geant4 -> GRAS. Each needs the one before.
Pattern for each: download source -> configure with cmake -> compile -> install.

Version pairing: GRAS 7.0 needs Geant4 11.3; GRAS 6.0.1 needs Geant4 10.7.

## 1. cmake (via a Python venv, if the system package manager is unavailable)

```bash
uv venv ~/software/buildtools
uv pip install --python ~/software/buildtools cmake==3.31.10
export PATH=$HOME/software/buildtools/bin:$PATH
```

## 2. xerces-c 3.2.5 (XML reader, needed for GDML geometry files)

```bash
mkdir -p ~/software/src && cd ~/software/src
curl -LO https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.2.5.tar.gz
tar -xzf xerces-c-3.2.5.tar.gz
cmake -S xerces-c-3.2.5 -B xerces-c-3.2.5/build \
  -DCMAKE_INSTALL_PREFIX=$HOME/software/xerces-c \
  -Dtranscoder=iconv -DCMAKE_CXX_STANDARD=17
cmake --build xerces-c-3.2.5/build -j14
cmake --install xerces-c-3.2.5/build
```

`transcoder=iconv` because the default (ICU) failed to build.

## 3. Geant4 11.3.2

```bash
cd ~/software/src
curl -LO https://gitlab.cern.ch/geant4/geant4/-/archive/v11.3.2/geant4-v11.3.2.tar.gz
tar -xzf geant4-v11.3.2.tar.gz
cmake -S geant4-v11.3.2 -B geant4-build \
  -DCMAKE_INSTALL_PREFIX=$HOME/software/geant4-11.3.2 \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_BUILD_MULTITHREADED=ON \
  -DGEANT4_USE_GDML=ON -DXercesC_ROOT=$HOME/software/xerces-c \
  -DGEANT4_INSTALL_DATA=ON \
  -DGEANT4_USE_QT=OFF -DGEANT4_USE_OPENGL_X11=OFF
cmake --build geant4-build -j14
cmake --install geant4-build
```

- MULTITHREADED: uses several CPU cores.
- USE_GDML: reads geometry files (needs xerces-c).
- INSTALL_DATA: downloads the physics data tables (most of the 2.2 GB).
- QT/OPENGL OFF: no graphical viewer (simpler build; no 3D display).
- -j14: compile on 14 cores.

## 4. GRAS 7.0.0

GRAS is distributed by ESA through the ESSR repository after registration; it is not included here.
Unpacked in `~/software/gras-src/gras-07-00-00`.

```bash
source ~/software/geant4-11.3.2/bin/geant4.sh
cd ~/software/src
cmake -S ~/software/gras-src/gras-07-00-00 -B gras7-build \
  -DCMAKE_BUILD_TYPE=Release -DSTATIC_BUILD=OFF \
  -DGRAS_INSTALL_PREFIX=$HOME/software/gras-07-00-00 \
  -DGeant4_DIR=$HOME/software/geant4-11.3.2/lib/cmake/Geant4 \
  -DXercesC_ROOT=$HOME/software/xerces-c
cmake --build gras7-build -j14
cmake --install gras7-build
```

## 5. Loader: `~/software/setup-gras.sh`

```bash
source $HOME/software/geant4-11.3.2/bin/geant4.sh
source $HOME/software/gras-07-00-00/bin/gras-env.sh
export LD_LIBRARY_PATH=$HOME/software/xerces-c/lib:$LD_LIBRARY_PATH
export PATH=$HOME/software/buildtools/bin:$PATH
```

## Using it

```bash
source ~/software/setup-gras.sh
gras your_macro.in
```

## On another machine

- With sudo it is simpler: install cmake and xerces-c from the package
  manager (Ubuntu: `sudo apt install cmake libxerces-c-dev`), skip steps 1-2.
- Geant4 is the slow step (minutes on 16 cores; much longer on a laptop).
- Test: run any working GRAS macro with a small number of events.

Build logs: `~/software/src/*.log`.
