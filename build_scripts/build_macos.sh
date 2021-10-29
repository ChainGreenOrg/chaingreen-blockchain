#!/bin/bash

set -euo pipefail

pip install setuptools_scm
# The environment variable CHAINGREEN_INSTALLER_VERSION needs to be defined.
# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG.
CHAINGREEN_INSTALLER_VERSION=$(python installer-version.py)

if [ ! "$CHAINGREEN_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable CHAINGREEN_INSTALLER_VERSION set. Using 0.0.0."
	CHAINGREEN_INSTALLER_VERSION="0.0.0"
fi
echo "Chaingreen Installer Version is: $CHAINGREEN_INSTALLER_VERSION"

echo "Installing npm and electron packagers"
npm install electron-installer-dmg -g
npm install electron-packager -g
npm install electron/electron-osx-sign -g
npm install notarize-cli -g

echo "Create dist/"
sudo rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
pip install pyinstaller==4.5
SPEC_FILE=$(python -c 'import chaingreen; print(chaingreen.PYINSTALLER_SPEC_PATH)')
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi
cp -r dist/daemon ../chaingreen-blockchain-gui
cd .. || exit

echo "Running git submodule update --init --recursive."
echo ""
git submodule update --init --recursive
echo "Running git submodule update."
echo ""
git submodule update
cd chaingreen-blockchain-gui

SUBMODULE_BRANCH=$1
if [ "$SUBMODULE_BRANCH" ];
then
git fetch
	git checkout "$SUBMODULE_BRANCH"
git pull
	echo ""
	echo "Building the GUI with branch $SUBMODULE_BRANCH"
	echo ""
fi

echo "npm build"
echo "npm install"
npm install
echo "npm audit fix"
npm audit fix
echo "npm build"
npm run build
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "npm run build failed!"
	exit $LAST_EXIT_CODE
fi

# sets the version for chaingreen-blockchain in package.json
brew install jq
cp package.json package.json.orig
jq --arg VER "$CHAINGREEN_INSTALLER_VERSION" '.version=$VER' package.json > temp.json && mv temp.json package.json

electron-packager . Chaingreen --asar.unpack="**/daemon/**" --platform=darwin \
--icon=src/assets/img/Chaingreen.icns --overwrite --app-bundle-id=net.chaingreen.blockchain \
--appVersion=$CHAINGREEN_INSTALLER_VERSION
LAST_EXIT_CODE=$?

# reset the package.json to the original
mv package.json.orig package.json

if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-packager failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" == true ]; then
  electron-osx-sign Chaingreen-darwin-x64/Chaingreen.app --platform=darwin \
  --hardened-runtime=true --provisioning-profile=chiablockchain.provisionprofile \
  --entitlements=entitlements.mac.plist --entitlements-inherit=entitlements.mac.plist \
  --no-gatekeeper-assess
fi
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-osx-sign failed!"
	exit $LAST_EXIT_CODE
fi

mv Chaingreen-darwin-x64 ../build_scripts/dist/
cd ../build_scripts || exit

DMG_NAME="Chaingreen-$CHAINGREEN_INSTALLER_VERSION.dmg"
echo "Create $DMG_NAME"
mkdir final_installer
electron-installer-dmg dist/Chaingreen-darwin-x64/Chaingreen.app Chaingreen-$CHAINGREEN_INSTALLER_VERSION \
--overwrite --out final_installer
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-installer-dmg failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" == true ]; then
	echo "Notarize $DMG_NAME on ci"
	cd final_installer || exit
  notarize-cli --file=$DMG_NAME --bundle-id net.chaingreen.blockchain \
	--username "$APPLE_NOTARIZE_USERNAME" --password "$APPLE_NOTARIZE_PASSWORD"
  echo "Notarization step complete"
else
	echo "Not on ci or no secrets so skipping Notarize"
fi

# Notes on how to manually notarize
#
# Ask for username and password. password should be an app specific password.
# Generate app specific password https://support.apple.com/en-us/HT204397
# xcrun altool --notarize-app -f Chaingreen-0.1.X.dmg --primary-bundle-id net.chaingreen.blockchain -u username -p password
# xcrun altool --notarize-app; -should return REQUEST-ID, use it in next command
#
# Wait until following command return a success message".
# watch -n 20 'xcrun altool --notarization-info  {REQUEST-ID} -u username -p password'.
# It can take a while, run it every few minutes.
#
# Once that is successful, execute the following command":
# xcrun stapler staple Chaingreen-0.1.X.dmg
#
# Validate DMG:
# xcrun stapler validate Chaingreen-0.1.X.dmg
